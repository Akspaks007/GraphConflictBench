import asyncio
from datetime import datetime, timezone
from pathlib import Path

import pytest
import yaml

from graphconflictbench.adapters.lightrag_adapter import AdapterConfig, LightRAGAdapter
from graphconflictbench.gemini_control import GeminiControl, GeminiError, GeminiPolicy
from graphconflictbench.manifests import file_hash, write_json
from graphconflictbench.providers import model_provider

ROOT = Path(__file__).resolve().parents[2]
FIXED = datetime(2026, 11, 15, tzinfo=timezone.utc).timestamp()


@pytest.fixture
def control(tmp_path, monkeypatch):
    now = [FIXED]
    monkeypatch.setattr(GeminiControl, "clock", staticmethod(lambda: now[0]))

    async def advance(self, seconds):
        now[0] += seconds
    monkeypatch.setattr(GeminiControl, "sleep", advance)
    policy = GeminiPolicy(state_directory="state", eligibility_status="free-tier-confirmed",
                          eligibility_reference="offline-test-project-settings",
                          eligibility_checked_on="2026-11-15", quotas_reviewed=True)
    path = tmp_path / "policy.json"
    write_json(path, policy.model_dump())
    instance = GeminiControl(path)
    instance.initialize()
    instance.test_clock = now
    return instance


def test_unverified_project_is_not_assumed_free(tmp_path, monkeypatch):
    monkeypatch.setattr(GeminiControl, "clock", staticmethod(lambda: FIXED))
    path = tmp_path / "policy.json"
    write_json(path, GeminiPolicy(state_directory="state").model_dump())
    with pytest.raises(GeminiError, match="eligibility"):
        GeminiControl(path).initialize()
    assert not (tmp_path / "state").exists()


def test_deadline_and_stale_project_attestation_fail_closed(control):
    control.test_clock[0] += 8 * 86400
    with pytest.raises(GeminiError, match="stale"):
        control.require_eligibility()
    control.test_clock[0] = datetime(2026, 12, 1, tzinfo=timezone.utc).timestamp()
    with pytest.raises(GeminiError, match="routing deadline"):
        control.require_eligibility()


def test_gemini_prices_are_not_openai_prices():
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        GeminiPolicy(state_directory="state", llm_input_nanodollars_per_token=150)
    policy = GeminiPolicy(state_directory="state")
    assert policy.llm_input_nanodollars_per_token == 300
    assert policy.llm_output_nanodollars_per_token == 2500
    assert policy.embedding_nanodollars_per_token == 150


def test_quota_spacing_and_tpm_share_one_persistent_ledger(control):
    assert control.try_reserve("first", 10, "test", 30000) == 0
    wait = control.try_reserve("second", 10, "test", 30000)
    assert wait > 60
    asyncio.run(control.reserve_request("second", 10, "test", 30000))
    assert control.status()["dispatched_or_reserved_requests"] == 2
    assert control.status()["requests_in_rolling_24h"] == 2
    reloaded = GeminiControl(control.policy_file)
    assert reloaded.status()["held_nanodollars"] == 20
    assert reloaded.status()["cost_basis"] == "paid_equivalent_upper_bound_not_an_invoice"


def test_total_daily_and_budget_request_limits_are_not_refunded(control):
    # Use an independent frozen policy/ledger rather than modifying its initialized identity.
    path = control.policy_file.parent / "limited.json"
    values = control.policy.model_dump()
    values["max_requests_per_24h"] = 1
    values["state_directory"] = "limited"
    write_json(path, values)
    limited = GeminiControl(path)
    limited.initialize()
    limited.try_reserve("one", 2_000_000_000, "test", 1)
    control.test_clock[0] += 31
    with pytest.raises(GeminiError, match="24h"):
        limited.try_reserve("two", 1, "test", 1)
    control.test_clock[0] += 86400
    with pytest.raises(GeminiError, match="reservation cap"):
        limited.try_reserve("three", 1, "test", 1)


def test_missing_embedding_usage_is_retained_as_upper_bound_not_free(control):
    cost, usage = control.measured_cost("embedding", {"embedding": {}}, 100, 15000)
    assert cost == 15000 and usage["provider_usage"] is None
    assert usage["source"] == "upper_bound_no_usage_metadata"
    cost, usage = control.measured_cost("llm", {"usageMetadata": {
        "promptTokenCount": 10, "candidatesTokenCount": 2, "totalTokenCount": 12,
    }}, 100, 999999)
    assert cost == 8000
    with pytest.raises(GeminiError, match="usage"):
        control.measured_cost("llm", {}, 100, 999999)
    assert control.status()["frozen"]


@pytest.mark.parametrize("change", [
    {"embedding_dimension": 256}, {"embedding_task_type": None},
    {"llm_model": "gemini-3.5-flash-lite"}, {"embedding_model": "gemini-embedding-2"},
    {"max_retries": 2}, {"max_concurrency": 2}, {"benchmark_eligible": True},
])
def test_gemini_configuration_prevents_silent_space_or_model_changes(change):
    from pydantic import ValidationError
    config = yaml.safe_load((ROOT / "configs/architectures/lightrag-gemini.yaml").read_text())
    config.update(change)
    with pytest.raises(ValidationError):
        AdapterConfig.model_validate(config)


def test_fixture_factory_stays_fixture_and_gemini_policy_is_mandatory():
    assert model_provider({"provider": "fixture"}) is None
    with pytest.raises(GeminiError, match="frozen"):
        model_provider({"provider": "gemini"})


def test_lifetime_request_limit_is_independent_of_money_and_day(control):
    values = control.policy.model_dump()
    values.update(max_requests=1, state_directory="one-request")
    path = control.policy_file.parent / "one.json"
    write_json(path, values)
    one = GeminiControl(path)
    one.initialize()
    one.try_reserve("one", 10, "test", 1)
    control.test_clock[0] += 31
    with pytest.raises(GeminiError, match="total request limit"):
        one.try_reserve("two", 10, "test", 1)
    assert one.status()["held_nanodollars"] == 10


def test_policy_does_not_serialize_credentials(control, monkeypatch):
    import json
    key = "offline-policy-secret-29592"
    monkeypatch.setenv("GEMINI_API_KEY", key)
    content = json.loads(control.policy_file.read_text())
    content["eligibility_reference"] = key
    path = control.policy_file.parent / "credential.json"
    write_json(path, content)  # Synthetic hostile input; never a user's actual .env.
    with pytest.raises(GeminiError, match="must not contain a credential") as caught:
        GeminiControl(path)
    assert key not in str(caught.value)


@pytest.mark.parametrize("change", [
    {"tools": [{"googleSearch": {}}]},
    {"contents": [{"role": "user", "parts": [{"inlineData": {"mimeType": "image/png"}}]}]},
    {"generationConfig": {"candidateCount": 2}},
])
def test_unpriced_or_multimodal_generation_is_rejected(control, change):
    payload = {"contents": [{"role": "user", "parts": [{"text": "text"}]}],
               "generationConfig": {"candidateCount": 1, "temperature": 0, "maxOutputTokens": 1536,
                                    "thinkingConfig": {"thinkingBudget": 0, "includeThoughts": False}},
               **change}
    with pytest.raises(GeminiError):
        control.bounds("llm", payload)


def test_gemini_worker_timeout_allows_quota_waits_and_preserves_other_providers(control, tmp_path):
    config = yaml.safe_load((ROOT / "configs/architectures/lightrag-gemini.yaml").read_text())
    config.update(provider_control_file=str(control.policy_file),
                  provider_control_sha256=file_hash(control.policy_file))
    path = tmp_path / "gemini.yaml"
    path.write_text(yaml.safe_dump(config))
    adapter = LightRAGAdapter(path, "python")
    # A 180-call condition index needs at least 93 minutes of spacing alone.
    assert adapter._worker_timeout("index") > 180 * 31
    assert adapter._worker_timeout("query") > 1800
    assert adapter._worker_timeout("healthcheck") == 1800
    config.update(provider="openai")
    path = tmp_path / "openai.yaml"
    path.write_text(yaml.safe_dump(config))
    assert LightRAGAdapter(path, "python")._worker_timeout("index") == 1800
    config.update(provider="fixture")
    path = tmp_path / "fixture.yaml"
    path.write_text(yaml.safe_dump(config))
    assert LightRAGAdapter(path, "python")._worker_timeout("index") == 1800
