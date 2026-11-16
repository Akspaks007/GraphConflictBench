# Tokenizer asset provenance

These byte-identical tiktoken BPE rank files were obtained from the public
niieani/gpt-tokenizer repository at commit
`785c2695acbda31ae31ef8ab6343bcd7f1dde72f`, under `data/`.
They match the expected SHA256 values in the installed official tiktoken
`tiktoken_ext.openai_public` encoding definitions:

| Asset | SHA256 |
| --- | --- |
| cl100k_base.tiktoken | 223921b76ee99bde995b7ff738513eef100fb51d18c93597a113bcffe865b2a7 |
| o200k_base.tiktoken | 446a9538cb6c348e3516120d7c08b09f57c36495e2acfffe59a5bf8b0cfb1a2d |

Canonical upstream URLs:
- https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken
- https://openaipublic.blob.core.windows.net/encodings/o200k_base.tiktoken

The canonical host was blocked by the execution environment's proxy. The mirror
was used only after verifying the complete file hashes against upstream expected
values. See third_party/tiktoken_LICENSE.txt and tokenizer_mirror_LICENSE.txt.
`scripts/cache_tokenizers.py` repeats the verification before populating the
standard tiktoken cache. No tokenizer code, TLS checks or proxy policy was changed.
