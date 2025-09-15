"""Translation helpers built on top of the OpenAI API."""

from .gpt_translator import translate_text, translate_chapters

__all__ = ["translate_text", "translate_chapters"]
