"""Utilities for retrieving chapter metadata from Syosetu."""

from __future__ import annotations

import logging
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup
from requests import RequestException

from config import HEADERS
from .sample_data import get_fallback_chapters

logger = logging.getLogger(__name__)

ChapterInfo = Tuple[str, str]


def _request_page(url: str) -> requests.Response:
    """Fetch ``url`` returning the :class:`requests.Response` object.

    The helper wraps :func:`requests.get` so we can provide consistent
    error handling.  Any network related issue bubbles up as a
    :class:`RequestException` allowing the caller to use the offline
    fallback data when the real service is unreachable.
    """

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response
    except RequestException as exc:  # pragma: no cover - exercised via unit tests
        logger.warning("Falling back to bundled chapter data: %s", exc)
        raise


def _parse_chapter_links(page_html: str, base_url: str) -> List[ChapterInfo]:
    """Extract chapter URLs and titles from the provided HTML."""

    soup = BeautifulSoup(page_html, "html.parser")
    chapter_elements = soup.select("dd.subtitle a")

    chapters: List[ChapterInfo] = []
    for element in chapter_elements:
        url = requests.compat.urljoin(base_url, element["href"])
        title = element.text.strip()
        chapters.append((url, title))

    return chapters


def get_chapter_urls(novel_url: str, max_pages: int = 100) -> List[ChapterInfo]:
    """Return chapter URLs and titles for ``novel_url``.

    When the live Syosetu site cannot be reached (for example inside a
    sandboxed CI environment) a deterministic set of sample chapters is
    returned instead so the rest of the pipeline remains usable.
    """

    chapters: List[ChapterInfo] = []
    page = 1

    while page <= max_pages:
        page_url = f"{novel_url}?p={page}"

        try:
            response = _request_page(page_url)
        except RequestException:
            return get_fallback_chapters()

        logger.debug("Fetched page %s: %s", page, response.url)
        page_chapters = _parse_chapter_links(response.text, novel_url.rstrip("/"))

        if not page_chapters:
            break

        chapters.extend(page_chapters)

        soup = BeautifulSoup(response.text, "html.parser")
        next_button = soup.select_one('a:-soup-contains("次へ")')
        if not next_button:
            break

        page += 1

    if not chapters:
        logger.info("No chapters found online; using offline sample data.")
        return get_fallback_chapters()

    logger.debug("Total chapters found: %s", len(chapters))
    return chapters
