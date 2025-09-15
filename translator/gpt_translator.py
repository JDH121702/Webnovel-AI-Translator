"""Translation utilities that wrap the OpenAI Chat Completions API."""

from __future__ import annotations

import os
from typing import Iterable, List, Sequence, Tuple

from dotenv import load_dotenv
import openai

load_dotenv()

# Older versions of the OpenAI package expose ``openai.ChatCompletion``
# directly.  The 1.x series switches to a client based API.  The shim
# below keeps the rest of the code (and the unit tests) working on both
# flavours without hard pinning a specific dependency version.
if not hasattr(openai, "ChatCompletion"):
    try:  # pragma: no cover - defensive compatibility path
        from openai import OpenAI as _OpenAI
    except ImportError:  # pragma: no cover - only triggered with broken installs
        _OpenAI = None

    class _ChatCompletionProxy:  # pragma: no cover - simple delegation
        def __init__(self) -> None:
            self._client = None

        def _client_instance(self):
            if self._client is None:
                if _OpenAI is None:
                    raise RuntimeError("OpenAI client is not available.")
                api_key = os.getenv("OPENAI_API_KEY")
                self._client = _OpenAI(api_key=api_key)
            return self._client

        def create(self, **kwargs):
            client = self._client_instance()
            return client.chat.completions.create(**kwargs)

    openai.ChatCompletion = _ChatCompletionProxy()  # type: ignore[attr-defined]

# Configure the API key for legacy versions of the library.
if not getattr(openai, "api_key", None):
    openai.api_key = os.getenv("OPENAI_API_KEY")

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
SYSTEM_PROMPT = (
    "You are a translator that converts text to English. Preserve the HTML "
    "tags and the original author's writing style as much as possible."
)

Message = Sequence[dict]
Chapter = Tuple[str, str]


def _build_messages(text: str) -> Message:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                "Translate the following text to English, preserving HTML tags "
                "and the original author's writing style:\n\n{text}"
            ).format(text=text),
        },
    ]


def translate_text(text: str, *, model: str | None = None) -> str:
    """Translate ``text`` to English using the configured OpenAI model."""

    if not text:
        return ""

    selected_model = model or DEFAULT_MODEL
    messages = _build_messages(text)

    response = openai.ChatCompletion.create(model=selected_model, messages=messages)
    content = response["choices"][0]["message"]["content"].strip()
    return content


def translate_chapters(chapters: Iterable[Chapter], *, model: str | None = None) -> List[Chapter]:
    """Translate each chapter ``(title, content)`` pair in ``chapters``."""

    translated: List[Chapter] = []
    for title, content in chapters:
        translated.append((title, translate_text(content, model=model)))
    return translated
