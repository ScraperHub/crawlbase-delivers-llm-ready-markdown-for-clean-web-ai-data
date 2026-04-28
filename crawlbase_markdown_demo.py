"""Fetch LLM-ready Markdown from a web page using Crawlbase Crawling API.

This tutorial script keeps the moving parts small:
1. Read a Crawlbase API token from the environment.
2. Request a page with format=md and md_readability=true.
3. Save the Markdown response body to a local file.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Final

import requests


CRAWLBASE_API_URL: Final = "https://api.crawlbase.com/"
DEFAULT_TARGET_URL: Final = "https://example.com/"
DEFAULT_OUTPUT_PATH: Final = Path("output/page.md")
DEFAULT_TIMEOUT_SECONDS: Final = 90


class CrawlbaseError(RuntimeError):
    """Raised when Crawlbase does not return a usable Markdown response."""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch clean Markdown from a URL using Crawlbase Crawling API.",
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_TARGET_URL,
        help=f"Page to crawl. Defaults to {DEFAULT_TARGET_URL}",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help=f"Where to save the Markdown. Defaults to {DEFAULT_OUTPUT_PATH}",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=f"Request timeout in seconds. Defaults to {DEFAULT_TIMEOUT_SECONDS}",
    )
    return parser


def fetch_markdown(url: str, token: str, timeout: int) -> requests.Response:
    """Call Crawlbase with Markdown output and readability extraction enabled."""
    try:
        response = requests.get(
            CRAWLBASE_API_URL,
            params={
                "token": token,
                "url": url,
                "format": "md",
                "md_readability": "true",
            },
            timeout=timeout,
            headers={
                "Accept": "text/markdown",
                "Accept-Encoding": "gzip",
                "User-Agent": "crawlbase-markdown-demo/1.0",
            },
        )
    except requests.RequestException as exc:
        raise CrawlbaseError(f"Request failed: {exc}") from exc

    if response.status_code != 200:
        raise CrawlbaseError(
            f"Crawlbase returned HTTP {response.status_code}: {response.text[:300]}"
        )

    pc_status = response.headers.get("pc_status")
    if pc_status and pc_status != "200":
        raise CrawlbaseError(
            f"Crawlbase pc_status={pc_status}; original_status="
            f"{response.headers.get('original_status', 'unknown')}"
        )

    content_type = response.headers.get("Content-Type", "")
    if not content_type.startswith("text/markdown"):
        raise CrawlbaseError(f"Expected Markdown but received Content-Type={content_type}")

    if not response.text.strip():
        raise CrawlbaseError("Crawlbase returned an empty Markdown body.")

    return response


def save_markdown(markdown: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")


def print_summary(response: requests.Response, output_path: Path) -> None:
    print("Markdown scrape complete")
    print(f"Resolved URL: {response.headers.get('url', 'unknown')}")
    print(f"Original status: {response.headers.get('original_status', 'unknown')}")
    print(f"Crawlbase status: {response.headers.get('pc_status', response.status_code)}")
    print(f"Content-Type: {response.headers.get('Content-Type', 'unknown')}")
    print(f"Markdown flavor: {response.headers.get('X-Markdown-Flavor', 'unknown')}")
    print(f"Saved to: {output_path}")


def main() -> int:
    args = build_parser().parse_args()
    token = os.getenv("CRAWLBASE_TOKEN")

    if not token:
        raise CrawlbaseError(
            "Missing CRAWLBASE_TOKEN. Set it as an environment variable before running."
        )

    response = fetch_markdown(url=args.url, token=token, timeout=args.timeout)
    save_markdown(response.text, args.output)
    print_summary(response, args.output)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CrawlbaseError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
