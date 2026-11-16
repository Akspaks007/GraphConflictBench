"""Seed tiktoken's standard cache with byte-verified bundled assets.

Run after checkout if the normal OpenAI blob host cannot be reached. No TLS or
proxy policy changes are made. Asset SHA256 values are tiktoken's expected hashes.
"""

import hashlib
import os
import tempfile
from pathlib import Path

EXPECTED = {
    "cl100k_base": "223921b76ee99bde995b7ff738513eef100fb51d18c93597a113bcffe865b2a7",
    "o200k_base": "446a9538cb6c348e3516120d7c08b09f57c36495e2acfffe59a5bf8b0cfb1a2d",
}


def main():
    source = Path(__file__).resolve().parents[1] / "assets/tokenizers"
    cache = Path(
        os.environ.get(
            "TIKTOKEN_CACHE_DIR",
            os.environ.get(
                "DATA_GYM_CACHE_DIR", str(Path(tempfile.gettempdir()) / "data-gym-cache")
            ),
        )
    )
    cache.mkdir(parents=True, exist_ok=True)
    for name, expected in EXPECTED.items():
        data = (source / f"{name}.tiktoken").read_bytes()
        if hashlib.sha256(data).hexdigest() != expected:
            raise ValueError(f"tokenizer asset failed SHA256 verification: {name}")
        original_url = f"https://openaipublic.blob.core.windows.net/encodings/{name}.tiktoken"
        key = hashlib.sha1(original_url.encode()).hexdigest()
        (cache / key).write_bytes(data)
        print(f"Verified {name}: {expected}")


if __name__ == "__main__":
    main()
