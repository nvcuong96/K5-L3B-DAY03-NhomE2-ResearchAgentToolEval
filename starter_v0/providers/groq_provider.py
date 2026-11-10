from __future__ import annotations

import json
import os
from typing import Any

from providers.base import ModelResponse, ToolCall


def _normalize_tools(tools: list[dict[str, Any]] | None) -> list[dict[str, Any]] | None:
    """Đảm bảo tools tuân thủ OpenAI/Groq spec format: {'type': 'function', 'function': {...}}."""
    if not tools:
        return None

    groq_tools: list[dict[str, Any]] = []
    for item in tools:
        if "type" in item and "function" in item:
            groq_tools.append(item)
        elif "function" in item:
            groq_tools.append({"type": "function", "function": item["function"]})
        else:
            groq_tools.append({"type": "function", "function": item})
    return groq_tools


def _parse_tool_calls(raw_tool_calls: Any) -> list[ToolCall]:
    """Parse và deduplicate danh sách tool_calls từ response của Groq."""
    if not raw_tool_calls:
        return []

    calls: list[ToolCall] = []
    seen: set[tuple[str, str]] = set()

    for call in raw_tool_calls:
        function = getattr(call, "function", None)
        if function is None and isinstance(call, dict):
            function = call.get("function")

        if not function:
            continue

        name = getattr(function, "name", None) or (function.get("name") if isinstance(function, dict) else None)
        raw_args = getattr(function, "arguments", None) or (function.get("arguments") if isinstance(function, dict) else None)

        if not name:
            continue

        if isinstance(raw_args, str):
            try:
                args = json.loads(raw_args)
            except json.JSONDecodeError:
                args = {"raw": raw_args}
        elif isinstance(raw_args, dict):
            args = raw_args
        else:
            args = {}

        key = (name, json.dumps(args, ensure_ascii=False, sort_keys=True))
        if key not in seen:
            seen.add(key)
            calls.append(ToolCall(name=name, args=args))

    return calls


class GroqProvider:
    """Groq API provider with normalized tool_calls output."""

    def __init__(
        self,
        *,
        api_key_env: str = "GROQ_API_KEY",
        default_model: str = "openai/gpt-oss-20b",
    ) -> None:
        self.api_key_env = api_key_env
        self.default_model = default_model

    def complete(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]] | None = None,
        *,
        model: str | None = None,
        temperature: float = 0.0,
        tool_choice: Any | None = None,
    ) -> ModelResponse:
        # Sử dụng OpenAI client có sẵn nhưng trỏ base_url về Groq
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Thiếu thư viện openai: pip install openai") from exc

        api_key = os.getenv(self.api_key_env)
        if not api_key:
            raise RuntimeError(f"Missing API key env var: {self.api_key_env}")

        # Groq endpoint tương thích chuẩn OpenAI
        client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key,
        )

        request_kwargs: dict[str, Any] = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature,
        }

        groq_tools = _normalize_tools(tools)
        if groq_tools:
            request_kwargs["tools"] = groq_tools
            if tool_choice is not None:
                request_kwargs["tool_choice"] = tool_choice

        resp = client.chat.completions.create(**request_kwargs)

        choice = resp.choices[0] if getattr(resp, "choices", None) else None
        text: str | None = None
        tool_calls: list[ToolCall] = []

        if choice and getattr(choice, "message", None):
            text = choice.message.content
            raw_calls = getattr(choice.message, "tool_calls", None)
            tool_calls = _parse_tool_calls(raw_calls)

        return ModelResponse(text=text, tool_calls=tool_calls, raw=resp)