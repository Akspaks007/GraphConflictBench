import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

import pytest

from graphconflictbench.manifests import file_hash
from graphconflictbench.models import OpenAIModels
from graphconflictbench.provider_control import ProviderControl, immutable_bytes


@pytest.fixture
def control(tmp_path):
    path = tmp_path / "policy.json"
    path.write_text(json.dumps({
        "llm_model": "gpt-4o-mini-2024-07-18", "embedding_model": "text-embedding-3-small",
        "cap_nanodollars": 100, "llm_input_nanodollars_per_token": 150,
        "llm_output_nanodollars_per_token": 600, "embedding_nanodollars_per_token": 20,
        "max_completion_tokens": 1536, "max_request_input_tokens": 128000,
        "state_directory": "control",
    }))
    instance = ProviderControl(path)
    instance.initialize()
    return instance


def test_concurrent_reservations_cannot_overdraw(control):
    def reserve(i):
        try:
            control.reserve(str(i), 30, "test")
            return True
        except RuntimeError:
            return False
    with ThreadPoolExecutor(max_workers=8) as pool:
        assert sum(pool.map(reserve, range(20))) == 3
    assert control.status()["held_nanodollars"] == 90
    assert control.status()["available_nanodollars"] == 10


def test_cross_process_shared_cap_and_crash_reservation(control):
    control.reserve("parent", 70, "test")
    code = (
        "import sys; from graphconflictbench.provider_control import ProviderControl; "
        "c=ProviderControl(sys.argv[1]); c.reserve('child',40,'test')"
    )
    child = subprocess.run([sys.executable, "-B", "-c", code, str(control.policy_file)],
                           capture_output=True, text=True)
    assert child.returncode != 0 and "spending cap" in child.stderr
    restarted = ProviderControl(control.policy_file)
    assert restarted.status()["held_nanodollars"] == 70
    with pytest.raises(FileExistsError):
        restarted.initialize()


def test_unknown_failure_holds_full_reservation_and_double_settlement_fails(control):
    control.reserve("unknown", 70, "test")
    control.uncertain("unknown", "error")
    with pytest.raises(RuntimeError, match="spending cap"):
        control.reserve("next", 31, "test")
    with pytest.raises(RuntimeError, match="settled or unknown"):
        control.settle("unknown", 0, "test")
    control.reserve("known", 30, "test")
    control.settle("known", 10, "response")
    assert control.status()["charged_nanodollars"] == 10
    assert control.status()["held_nanodollars"] == 70
    with pytest.raises(RuntimeError):
        control.settle("known", 0, "response")


def test_policy_change_and_reservation_overrun_freeze(control):
    control.reserve("one", 10, "test")
    with pytest.raises(RuntimeError, match="frozen"):
        control.settle("one", 11, "response")
    assert control.status()["frozen"]
    with pytest.raises(RuntimeError, match="frozen"):
        control.reserve("two", 1, "test")
    content = json.loads(control.policy_file.read_text())
    content["cap_nanodollars"] = 200
    control.policy_file.write_text(json.dumps(content))
    with pytest.raises(ValueError, match="identity changed"):
        ProviderControl(control.policy_file).status()


def test_actual_usage_and_fail_closed_invalid_usage(control):
    assert control.usage_cost("/v1/chat/completions", {"usage": {
        "prompt_tokens": 10, "completion_tokens": 2}}, 100, 10) == 2700
    assert control.usage_cost("/v1/embeddings", {"usage": {"prompt_tokens": 10}}, 100, 0) == 200
    with pytest.raises(RuntimeError, match="usage"):
        control.usage_cost("/v1/chat/completions", {}, 100, 10)
    assert control.status()["frozen"]


@pytest.mark.parametrize("usage", [{"prompt_tokens": 10},
                                  {"prompt_tokens": 1, "completion_tokens": 2, "total_tokens": 99},
                                  {"prompt_tokens": -1, "completion_tokens": 0},
                                  {"prompt_tokens": 1, "completion_tokens": True}])
def test_missing_completion_or_inconsistent_usage_cannot_release_reservation(control, usage):
    control.reserve("pending", 100, "test")
    with pytest.raises(RuntimeError, match="usage"):
        control.usage_cost("/v1/chat/completions", {"usage": usage}, 100, 10)
    assert control.status()["held_nanodollars"] == 100
    assert control.status()["frozen"]


@pytest.mark.parametrize("change", [
    {"stream": True}, {"n": 2}, {"model": "unpriced"}, {"max_tokens": None},
    {"tools": [{}]}, {"messages": [{"role": "user", "content": [{"image_url": "x"}]}]},
    {"max_tokens": 16384}, {"service_tier": "priority"},
])
def test_unpriced_request_options_are_rejected(control, change):
    payload = {"model": control.policy.llm_model, "messages": [{"role": "user", "content": "x"}],
               "max_tokens": 100, **change}
    with pytest.raises(ValueError):
        control.request_bound("/v1/chat/completions", payload, json.dumps(payload).encode())


def test_reservation_bounds_include_non_ascii_and_message_overhead(control):
    payload = {"model": control.policy.llm_model, "messages": [{"role": "user", "content": "你好"}],
               "max_tokens": 100}
    wire = json.dumps(payload, ensure_ascii=False).encode()
    amount, bound, output = control.request_bound("/v1/chat/completions", payload, wire)
    assert bound > len(wire) and amount == bound * 150 + output * 600
    with pytest.raises(ValueError):
        control.request_bound("/v1/embeddings", {"model": "unpriced", "input": ["x"]}, b"x")


def test_capture_is_create_once_and_live_requires_frozen_policy(tmp_path, control):
    immutable_bytes(tmp_path / "raw", b"original")
    with pytest.raises(FileExistsError):
        immutable_bytes(tmp_path / "raw", b"replacement")
    with pytest.raises(ValueError, match="frozen capture"):
        OpenAIModels({"provider": "openai"})  # No SDK import or provider connection.
    with pytest.raises(ValueError, match="checksum"):
        ProviderControl(control.policy_file, "0" * 64)
    assert len(file_hash(control.policy_file)) == 64
