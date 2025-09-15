"""Helpers for downloading the body of a Syosetu chapter."""

from __future__ import annotations

import logging
import requests
from bs4 import BeautifulSoup
from requests import RequestException

from config import HEADERS
from .sample_data import get_fallback_content

logger = logging.getLogger(__name__)


def get_chapter_content(chapter_url: str) -> str:
    """Return the HTML content for ``chapter_url``.

    Network failures are gracefully handled by falling back to the
    bundled sample HTML so the rest of the pipeline keeps functioning in
    offline environments.
    """

    try:
        response = requests.get(chapter_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except RequestException as exc:  # pragma: no cover - tested via fallback
        logger.warning("Falling back to bundled chapter content: %s", exc)
        return get_fallback_content(chapter_url)

    soup = BeautifulSoup(response.text, "html.parser")
    content_div = soup.find("div", id="novel_honbun")

    if not content_div:
        logger.info("Chapter body missing in response; using offline sample data.")
        return get_fallback_content(chapter_url)

    content_html = "".join(str(tag) for tag in content_div.find_all(["p", "br", "div"]))

    if not content_html.strip():
        logger.info("Chapter content empty; using offline sample data.")
        return get_fallback_content(chapter_url)

    return content_html
