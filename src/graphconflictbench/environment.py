"""Repository-local dotenv loading and credential-safe diagnostics.

Never log the dotenv values or serialize the process environment. This module
does not create, rewrite, copy or inspect private .env files for reporting.
"""

import json
import logging
import os
import traceback
from pathlib import Path
from urllib.parse import quote

from dotenv import load_dotenv

_SECRETS = set()
_KEY_NAMES = ("GEMINI_API_KEY", "GOOGLE_API_KEY", "OPENAI_API_KEY")


def register_secret(value):
    if value:
        _SECRETS.add(value)


def secret_variants():
    secrets = _SECRETS | {os.environ[n] for n in _KEY_NAMES if os.environ.get(n)}
    return sorted({v for s in secrets for v in (s, quote(s, safe=""), json.dumps(s)[1:-1])},
                  key=len, reverse=True)


def redact(value):
    text = str(value)
    for secret in secret_variants():
        text = text.replace(secret, "[REDACTED]")
    return text


def redact_bytes(data):
    for secret in secret_variants():
        data = data.replace(secret.encode(), b"[REDACTED]")
    return data


def install_log_redaction():
    previous = logging.getLogRecordFactory()
    if getattr(previous, "_gcb_secret_safe", False):
        return

    def safe_record(*args, **kwargs):
        record = previous(*args, **kwargs)
        record.msg, record.args = redact(record.getMessage()), ()
        if record.exc_info:
            record.exc_text = redact("".join(traceback.format_exception(*record.exc_info)))
            record.exc_info = None
        if record.stack_info:
            record.stack_info = redact(record.stack_info)
        return record

    safe_record._gcb_secret_safe = True
    logging.setLogRecordFactory(safe_record)


def load_environment(dotenv_path=None):
    path = Path(dotenv_path) if dotenv_path is not None else Path(__file__).resolve().parents[2] / ".env"
    # Explicit path: never search parent directories or a worker's temporary CWD.
    load_dotenv(dotenv_path=path, override=False, interpolate=False, verbose=False)
    for name in _KEY_NAMES:
        register_secret(os.environ.get(name))
    install_log_redaction()
