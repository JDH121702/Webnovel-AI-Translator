"""Command line entry point for the Webnovel AI Translator project."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Iterable, List, Tuple

from dotenv import load_dotenv

from config import BASE_URL
from epub import create_epub
from scraper import get_chapter_content, get_chapter_urls
from translator import translate_chapters

load_dotenv()

Chapter = Tuple[str, str]


def _setup_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def _collect_chapter_bodies(chapter_index: Iterable[Tuple[str, str]]) -> List[Chapter]:
    chapters: List[Chapter] = []
    for url, title in chapter_index:
        logging.debug("Fetching chapter content: %s", url)
        content = get_chapter_content(url)
        if not content:
            logging.warning("Skipping chapter '%s' (%s); no content available.", title, url)
            continue
        chapters.append((title, content))
    return chapters


def run_translation_cli(args: argparse.Namespace) -> None:
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    logging.info("Fetching chapter list from %s", args.novel_url)
    chapters = get_chapter_urls(args.novel_url, max_pages=args.max_pages)
    if args.chapter_limit is not None:
        chapters = chapters[: args.chapter_limit]

    if not chapters:
        raise SystemExit("No chapters were found for the provided novel URL.")

    logging.info("Retrieving the body for %s chapters", len(chapters))
    chapter_bodies = _collect_chapter_bodies(chapters)
    if not chapter_bodies:
        raise SystemExit("Unable to download any chapter content.")

    logging.info("Translating %s chapters", len(chapter_bodies))
    translated_chapters = translate_chapters(chapter_bodies)

    filename = args.filename
    if not filename.lower().endswith(".epub"):
        filename = f"{filename}.epub"

    logging.info("Generating EPUB: %s", output_dir / filename)
    create_epub(
        args.title,
        args.author,
        translated_chapters,
        str(output_dir),
        filename,
        args.cover_image,
    )

    logging.info("Translation complete! EPUB written to %s", output_dir / filename)


def run_gui(_: argparse.Namespace) -> None:
    from translator_gui import TranslatorApp

    app = TranslatorApp()
    app.mainloop()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging output.")

    subparsers = parser.add_subparsers(dest="command")

    gui_parser = subparsers.add_parser("gui", help="Launch the graphical user interface.")
    gui_parser.set_defaults(func=run_gui)

    translate_parser = subparsers.add_parser(
        "translate",
        help="Scrape, translate, and generate an EPUB using the command line interface.",
    )
    translate_parser.add_argument("--novel-url", default=BASE_URL, help="URL of the novel's index page.")
    translate_parser.add_argument("--title", required=True, help="Title to embed in the generated EPUB.")
    translate_parser.add_argument("--author", required=True, help="Author name to embed in the EPUB metadata.")
    translate_parser.add_argument(
        "--output-dir",
        default="./output",
        help="Directory where the EPUB file will be created.",
    )
    translate_parser.add_argument("--filename", default="novel.epub", help="Name of the generated EPUB file.")
    translate_parser.add_argument("--cover-image", default=None, help="Optional path to a cover image.")
    translate_parser.add_argument(
        "--chapter-limit",
        type=int,
        default=None,
        help="Limit the number of chapters to process.",
    )
    translate_parser.add_argument(
        "--max-pages",
        type=int,
        default=5,
        help="Maximum number of chapter listing pages to fetch.",
    )
    translate_parser.set_defaults(func=run_translation_cli)

    return parser


def main(argv: Iterable[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    _setup_logging(args.verbose)

    if getattr(args, "command", None) is None:
        args.command = "gui"
        args.func = run_gui

    args.func(args)


if __name__ == "__main__":
    main()
