import json
import logging
import shutil
import subprocess
from pathlib import Path

import pytest

from graphconflictbench import cli
from graphconflictbench.adapters.lightrag_adapter import LightRAGAdapter
from graphconflictbench.environment import load_environment, redact, redact_bytes, register_secret

ROOT = Path(__file__).resolve().parents[2]


def test_dotenv_loading_and_external_values_win(tmp_path, monkeypatch):
    path = tmp_path / ".env"
    path.write_text("GEMINI_API_KEY=offline-dotenv-key-1739\n")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    load_environment(path)
    import os
    assert os.environ["GEMINI_API_KEY"] == "offline-dotenv-key-1739"
    monkeypatch.setenv("GEMINI_API_KEY", "offline-external-key-1739")
    load_environment(path)
    assert os.environ["GEMINI_API_KEY"] == "offline-external-key-1739"


def test_cli_loads_dotenv_before_dispatch_and_redacts_errors(tmp_path, monkeypatch, capsys):
    key = "offline-cli-credential-7394"
    path = tmp_path / ".env"
    path.write_text("GEMINI_API_KEY=" + key + "\n")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setattr(cli, "load_environment", lambda: load_environment(path))
    monkeypatch.setattr("sys.argv", ["gcb", "validate-ontology"])

    def offline_dispatch(args):
        import os
        assert os.environ["GEMINI_API_KEY"] == key
        raise ValueError("offline failure " + key)
    monkeypatch.setattr(cli, "dispatch", offline_dispatch)
    assert cli.main() == 1
    captured = capsys.readouterr()
    assert key not in captured.out + captured.err
    assert "[REDACTED]" in captured.err


def test_native_subprocess_inherits_key_without_serializing_environment(tmp_path, monkeypatch):
    key = "offline-subprocess-credential-8321"
    monkeypatch.setenv("GEMINI_API_KEY", key)
    adapter = LightRAGAdapter(ROOT / "configs/architectures/lightrag-fixture.yaml", "unused")

    def fake_run(command, **kwargs):
        assert kwargs["env"]["GEMINI_API_KEY"] == key
        request = json.loads(Path(command[-1]).read_text())
        Path(request["response_file"]).write_text('{"status":"offline"}')
        return subprocess.CompletedProcess(command, 0)
    monkeypatch.setattr(subprocess, "run", fake_run)
    trace = tmp_path / "trace"
    assert adapter._call("healthcheck", trace)["status"] == "offline"
    assert key not in (trace / "request.json").read_text()
    assert "GEMINI_API_KEY" not in (trace / "request.json").read_text()


def test_log_messages_exception_text_and_byte_redaction(tmp_path, monkeypatch):
    key = "offline-log-key-5839+/?"
    path = tmp_path / ".env"
    path.write_text("GEMINI_API_KEY=" + key + "\n")
    monkeypatch.setenv("GEMINI_API_KEY", key)
    load_environment(path)
    log = tmp_path / "safe.log"
    handler = logging.FileHandler(log, encoding="utf-8")
    logger = logging.getLogger("gcb.offline.secret-test")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    try:
        logger.info("credential=%s", key)
        try:
            raise RuntimeError(key)
        except RuntimeError:
            logger.exception("offline exception")
    finally:
        logger.removeHandler(handler)
        handler.close()
    assert key not in log.read_text()
    assert "[REDACTED]" in log.read_text()
    register_secret(key)
    assert key not in redact(key)
    assert key.encode() not in redact_bytes(b"\xff" + key.encode())
    assert redact_bytes(b"\xff harmless binary") == b"\xff harmless binary"


def test_gitignore_excludes_all_dotenv_variants_except_example(tmp_path):
    git = shutil.which("git")
    if not git:
        pytest.skip("git is required for checking actual ignore semantics")
    subprocess.run([git, "init", "--quiet", str(tmp_path)], check=True, capture_output=True)
    (tmp_path / ".gitignore").write_bytes((ROOT / ".gitignore").read_bytes())
    result = subprocess.run([git, "-C", str(tmp_path), "check-ignore", "--no-index",
                             ".env", ".env.local", ".env.production", ".env.example"],
                            capture_output=True, text=True, check=False)
    assert set(result.stdout.splitlines()) == {".env", ".env.local", ".env.production"}
    assert "GEMINI_API_KEY=\n" in (ROOT / ".env.example").read_text()
