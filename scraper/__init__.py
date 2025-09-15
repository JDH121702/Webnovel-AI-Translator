"""Utilities for downloading and parsing web novel chapters."""

from .novel_scraper import get_chapter_urls
from .chapter_parser import get_chapter_content

__all__ = ["get_chapter_urls", "get_chapter_content"]
