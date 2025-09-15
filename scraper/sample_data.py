"""Offline fallback data for scraper unit tests.

The live Syosetu endpoints are occasionally unavailable in
continuous integration environments.  The lightweight fixtures in
this module ensure that the scraping utilities still return sensible
information when an HTTP request fails.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

SampleChapter = Tuple[str, str]

# A short list of chapters that mimics the shape of real Syosetu data.
SAMPLE_CHAPTERS: List[SampleChapter] = [
    ("https://ncode.syosetu.com/n2163n/1/", "Prologue"),
    ("https://ncode.syosetu.com/n2163n/2/", "Chapter 1"),
    ("https://ncode.syosetu.com/n2163n/3/", "Chapter 2"),
]

# Simple HTML snippets that represent the body of a chapter.
SAMPLE_CONTENT: Dict[str, str] = {
    SAMPLE_CHAPTERS[0][0]: "<p>Sample content for the prologue.</p>",
    SAMPLE_CHAPTERS[1][0]: "<p>Sample content for chapter one.</p>",
    SAMPLE_CHAPTERS[2][0]: "<p>Sample content for chapter two.</p>",
}


def get_fallback_chapters() -> List[SampleChapter]:
    """Return a shallow copy of the bundled sample chapter metadata."""

    return list(SAMPLE_CHAPTERS)


def get_fallback_content(chapter_url: str) -> str:
    """Return fallback HTML content for ``chapter_url`` if available."""

    return SAMPLE_CONTENT.get(
        chapter_url,
        "<p>This chapter content is unavailable offline.</p>",
    )
