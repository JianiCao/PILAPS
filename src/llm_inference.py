from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import logging
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import BitsAndBytesConfig

log = logging.getLogger(__name__)


class Backend(Enum):
    LOCAL = "local"
    OPENAI = "openai"
    GEMINI = "gemini"
    DEEPSEEK = "deepseek"
    TOGETHER = "together"


_API_BASE_URLS: dict[Backend, str] = {
    Backend.OPENAI: "https://api.openai.com/v1",
    Backend.DEEPSEEK: "https://api.deepseek.com",
    Backend.TOGETHER: "https://api.together.xyz/v1",
}


@dataclass
class InferenceConfig:
    backend: str
    model_name: str

    api_key: str | None = None
    base_url: str | None = None

    # local model
    model_path: str | None = None
    cache_dir: str = ""
    device: str = "auto"
    torch_dtype: str = "auto"
    load_in_4bit: bool = False
    load_in_8bit: bool = False

    # generation
    max_tokens: int = 1024
    temperature: float = 0.0
    top_p: float = 1.0
    extra_body: dict[str, Any] = field(default_factory=dict)


class LLMInferenceEngine:

    def __init__(self, cfg: InferenceConfig | Any) -> None:
        self.cfg = cfg
        self.backend = Backend(cfg.backend)
        self._client: Any = None
        self._model: Any = None
        self._tokenizer: Any = None

        if self.backend == Backend.LOCAL:
            self._load_local_model()
        elif self.backend == Backend.GEMINI:
            self._init_gemini_client()
        else:
            self._init_openai_compatible_client()

        log.info("Engine ready: backend=%s model=%s", self.backend.value, cfg.model_name)

    def _resolve_model_path(self) -> str:
        cache_dir = self.cfg.cache_dir.rstrip("/")
        name_slug = "--".join(self.cfg.model_name.split("/"))
        return f"{cache_dir}/models--{name_slug}"

    def _load_local_model(self) -> None:
        model_path = self._resolve_model_path()

        dtype_map = {
            "auto": "auto",
            "float16": torch.float16,
            "bfloat16": torch.bfloat16,
            "float32": torch.float32,
        }
        dtype = dtype_map.get(self.cfg.torch_dtype, "auto")

        quant_kwargs: dict[str, Any] = {}
        if self.cfg.load_in_4bit or self.cfg.load_in_8bit or "70B-Instruct" in model_path:
            quant_kwargs["quantization_config"] = BitsAndBytesConfig(
                load_in_4bit=self.cfg.load_in_4bit,
                load_in_8bit=self.cfg.load_in_8bit or "70B-Instruct" in model_path,
                llm_int8_enable_fp32_cpu_offload=True if "70B-Instruct" in model_path else False
            )

        self._tokenizer = AutoTokenizer.from_pretrained(
            model_path, trust_remote_code=True, local_files_only=True,
        )
        self._model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=dtype,
            device_map=self.cfg.device,
            trust_remote_code=True,
            local_files_only=True,
            **quant_kwargs,
        )
        self._model.eval()
        log.info("Local model loaded from %s", model_path)

    def _init_openai_compatible_client(self) -> None:
        from openai import OpenAI

        if not self.cfg.api_key:
            raise ValueError(f"api_key required for {self.backend.value} backend")

        base_url = self.cfg.base_url or _API_BASE_URLS.get(self.backend)
        self._client = OpenAI(api_key=self.cfg.api_key, base_url=base_url)

    def _init_gemini_client(self) -> None:
        from google import genai
        if not self.cfg.api_key:
            raise ValueError("api_key required for gemini backend")
        self._client = genai.Client(api_key=self.cfg.api_key)

    def infer(
        self,
        prompt: str,
        system_prompt: str | None = None,
        *,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> str:
        max_tokens = max_tokens or self.cfg.max_tokens
        temperature = temperature if temperature is not None else self.cfg.temperature

        if self.backend == Backend.LOCAL:
            return self._infer_local(prompt, system_prompt, max_tokens, temperature)
        if self.backend == Backend.GEMINI:
            return self._infer_gemini(prompt, system_prompt, max_tokens, temperature)
        return self._infer_openai_compatible(prompt, system_prompt, max_tokens, temperature)

    def _infer_local(
        self, prompt: str, system_prompt: str | None, max_tokens: int, temperature: float,
    ) -> str:
        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        chat_kwargs: dict[str, Any] = {
            "tokenize": False,
            "add_generation_prompt": True,
        }
        if "qwen" in self.cfg.model_name.lower():
            chat_kwargs["enable_thinking"] = False

        text = self._tokenizer.apply_chat_template(messages, **chat_kwargs)
        inputs = self._tokenizer(text, return_tensors="pt").to(self._model.device)

        gen_kwargs: dict[str, Any] = {"max_new_tokens": max_tokens, "do_sample": temperature > 0}
        if temperature > 0:
            gen_kwargs |= {"temperature": temperature, "top_p": self.cfg.top_p}

        with torch.inference_mode():
            output_ids = self._model.generate(**inputs, **gen_kwargs)

        new_ids = output_ids[0, inputs["input_ids"].shape[1]:]
        return self._tokenizer.decode(new_ids, skip_special_tokens=True).strip()

    def _build_messages(
        self, prompt: str, system_prompt: str | None,
    ) -> list[dict[str, str]]:
        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        return messages

    def _infer_openai_compatible(
        self, prompt: str, system_prompt: str | None, max_tokens: int, temperature: float,
    ) -> str:
        kwargs: dict[str, Any] = {
            "model": self.cfg.model_name,
            "messages": self._build_messages(prompt, system_prompt),
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        
        # Turn off thinking mode for qwen and all API models
        extra_disable_thinking = {
            "thinking": {"type": "disabled"},
        }
        kwargs["extra_body"] = {**extra_disable_thinking, **self.cfg.extra_body}

        response = self._client.chat.completions.create(**kwargs)
        return response.choices[0].message.content.strip()

    def _infer_gemini(
        self, prompt: str, system_prompt: str | None, max_tokens: int, temperature: float,
    ) -> str:
        from google.genai import types
        
        config_kwargs: dict[str, Any] = {
            "max_output_tokens": max_tokens,
            "temperature": temperature,
        }
        if system_prompt:
            config_kwargs["system_instruction"] = system_prompt
            
        if hasattr(types, "ThinkingConfig"):
            # Try to turn off thinking mode for Gemini models if available
            config_kwargs["thinking_config"] = types.ThinkingConfig(thinking_level="minimal")
            
        config = types.GenerateContentConfig(**config_kwargs)
        
        response = self._client.models.generate_content(
            model=self.cfg.model_name,
            contents=prompt,
            config=config,
        )
        return response.text.strip()
