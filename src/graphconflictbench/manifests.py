"""Content addressing, atomic writes and exclusive job ownership."""

import hashlib
import json
import os
from contextlib import contextmanager
from pathlib import Path


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def atomic_text(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        tmp.write_text(text, encoding="utf-8")
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def write_json(path, value):
    atomic_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def write_jsonl(path, rows):
    atomic_text(
        path,
        "".join(
            canonical(x.model_dump(mode="json") if hasattr(x, "model_dump") else x) + "\n"
            for x in rows
        ),
    )


def read_jsonl(path, model=None):
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(model.model_validate_json(line) if model else json.loads(line))
    return rows


@contextmanager
def exclusive_lock(directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    lock = directory / ".job.lock"
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise RuntimeError(
            f"job already owned, or stale lock requires inspection: {lock}"
        ) from None
    try:
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        yield
    finally:
        lock.unlink(missing_ok=True)


def tree_checksums(directory, exclude=()):
    root = Path(directory)
    return {
        str(p.relative_to(root)): file_hash(p)
        for p in sorted(root.rglob("*"))
        if p.is_file() and p.name not in {".job.lock", *exclude}
    }


def verify_checksums(directory, checksums):
    root = Path(directory)
    if not checksums:
        raise ValueError("empty integrity manifest")
    for name, expected in checksums.items():
        path = root / name
        if not path.is_file() or file_hash(path) != expected:
            raise ValueError(f"checksum mismatch: {path}")
