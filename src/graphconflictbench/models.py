"""Model providers. Fixture models test plumbing, never benchmark capability."""

import hashlib
import json
import os
import re

from .generator import NEGATIONS, PHRASES
from .provider_control import ProviderControl, audited_http_client

STATEMENT = re.compile(
    r"(N[0-9a-f]{20}) (is not contained in|is contained in|"
    r"is not a subregion of|is a subregion of|does not precede|precedes) "
    r"(N[0-9a-f]{20})\."
)


def parse_statements(text):
    reverse = {v: (k, True) for k, v in PHRASES.items()}
    reverse.update({v: (k, False) for k, v in NEGATIONS.items()})
    return [
        (m.group(1), *reverse[m.group(2)], m.group(3), m.group()) for m in STATEMENT.finditer(text)
    ]


async def fixture_llm(prompt, system_prompt=None, history_messages=None, **kwargs):
    # Read only the text supplied to the native model callback, never the gold KG.
    if "---Input Text---" in prompt:
        text = prompt.split("---Input Text---", 1)[1].split("---Output---", 1)[0]
        entities, relations = {}, []
        for subject, pred, positive, obj, sentence in parse_statements(text):
            entities[subject] = (
                f"entity<|#|>{subject}<|#|>other<|#|>{subject} is a fictional entity."
            )
            entities[obj] = f"entity<|#|>{obj}<|#|>other<|#|>{obj} is a fictional entity."
            relations.append(f"relation<|#|>{subject}<|#|>{obj}<|#|>{pred}<|#|>{sentence}")
        return "\n".join([*entities.values(), *relations, "<|COMPLETE|>"])
    if kwargs.get("keyword_extraction") or "high_level_keywords" in prompt:
        # Native keyword prompt contains worked examples; use only its real query.
        query = prompt.rsplit("Real Data", 1)[-1]
        ids = list(dict.fromkeys(re.findall(r"N[0-9a-f]{20}", query)))
        return json.dumps({"high_level_keywords": list(PHRASES), "low_level_keywords": ids})
    if history_messages:
        return "<|COMPLETE|>"
    # Native description summarization only: preserve input statements verbatim.
    statements = [x[-1] for x in parse_statements(prompt)]
    return " ".join(dict.fromkeys(statements)) or "Fictional registry entity."


async def fixture_embedding(texts, dimension=256, **kwargs):
    import numpy as np

    values = np.zeros((len(texts), dimension), dtype=np.float32)
    for i, text in enumerate(texts):
        for token in re.findall(r"[a-z0-9_]+", text.lower()):
            hashed = hashlib.sha256(token.encode()).digest()
            values[i, int.from_bytes(hashed[:4], "big") % dimension] += 1
        norm = np.linalg.norm(values[i])
        if norm:
            values[i] /= norm
    return values


class OpenAIModels:
    key_name = "OPENAI_API_KEY"
    base_url = "https://api.openai.com/v1"

    def __init__(self, config):
        if not config.get("provider_control_file") or not config.get("provider_control_sha256"):
            raise ValueError("real provider requires a frozen capture/spending policy")
        if config.get("max_retries", 0) != 0:
            raise ValueError("controlled provider requires max_retries=0; each retry needs accounting")
        self.control = ProviderControl(
            config["provider_control_file"], config["provider_control_sha256"]
        )
        self.control.status()  # Fail before constructing a network client if not initialized.
        policy = self.control.policy
        if (config["llm_model"] != policy.llm_model
                or config["embedding_model"] != policy.embedding_model):
            raise ValueError("configured provider models differ from priced policy")
        if policy.base_url != self.base_url:
            raise ValueError("provider origin differs from priced policy")
        if (self.key_name == "OPENAI_API_KEY"
                and os.environ.get("OPENAI_BASE_URL", policy.base_url).rstrip("/") != policy.base_url):
            raise ValueError("provider policy does not price this OPENAI_BASE_URL")
        keys = self.api_keys()
        from openai import AsyncOpenAI

        self.config = config
        self.client = AsyncOpenAI(
            api_key=keys[0], max_retries=0, timeout=120, base_url=policy.base_url,
            http_client=audited_http_client(self.control, rotating_keys=keys if len(keys) > 1 else ()),
        )
        self.usage = []

    def api_keys(self):
        api_key = os.environ.get(self.key_name)
        if not api_key:
            raise ValueError(f"{self.key_name} is required for the configured provider")
        return (api_key,)

    def completion_options(self):
        return {"max_tokens": self.control.policy.max_completion_tokens}

    async def llm(self, prompt, system_prompt=None, history_messages=None, **kwargs):
        messages = [{"role": "system", "content": system_prompt}] if system_prompt else []
        messages.extend(history_messages or [])
        messages.append({"role": "user", "content": prompt})
        response = await self.client.chat.completions.create(
            model=self.config["llm_model"],
            messages=messages,
            temperature=0,
            **self.completion_options(),
            **(
                {"response_format": {"type": "json_object"}}
                if kwargs.get("keyword_extraction")
                or kwargs.get("response_format") == {"type": "json_object"}
                else {}
            ),
        )
        self.usage.append(
            {
                "kind": "llm",
                "model": response.model,
                "tokens": response.usage.model_dump() if response.usage else None,
            }
        )
        return response.choices[0].message.content or ""

    async def embedding(self, texts, **kwargs):
        import numpy as np

        response = await self.client.embeddings.create(
            model=self.config["embedding_model"],
            input=texts,
            dimensions=self.config["embedding_dimension"],
        )
        self.usage.append(
            {
                "kind": "embedding",
                "model": response.model,
                "tokens": response.usage.model_dump() if response.usage else None,
            }
        )
        return np.asarray(
            [x.embedding for x in sorted(response.data, key=lambda x: x.index)], dtype=np.float32
        )
