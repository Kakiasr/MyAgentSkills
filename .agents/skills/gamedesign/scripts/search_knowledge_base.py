#!/usr/bin/env python3
"""Search the bundled game-design reference PDFs.

The script prefers extracted text caches next to each PDF, for example
references/game-design.txt. If a cache is missing, it tries common Python PDF
libraries that may exist in the runtime. It prints compact keyword matches with
surrounding context.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "references"


def extract_with_pypdf(pdf_path: Path) -> str | None:
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:
        return None

    reader = PdfReader(str(pdf_path))
    pages: list[str] = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append(f"\n\n[{pdf_path.name} page {index}]\n{text}")
    return "".join(pages)


def extract_with_py_pdf2(pdf_path: Path) -> str | None:
    try:
        from PyPDF2 import PdfReader  # type: ignore
    except Exception:
        return None

    reader = PdfReader(str(pdf_path))
    pages: list[str] = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append(f"\n\n[{pdf_path.name} page {index}]\n{text}")
    return "".join(pages)


def load_text_for_pdf(pdf_path: Path) -> str:
    txt_path = pdf_path.with_suffix(".txt")
    if txt_path.exists():
        return txt_path.read_text(encoding="utf-8", errors="ignore")

    if not pdf_path.exists():
        raise SystemExit(f"Missing reference PDF: {pdf_path}")

    for extractor in (extract_with_pypdf, extract_with_py_pdf2):
        text = extractor(pdf_path)
        if text and text.strip():
            txt_path.write_text(text, encoding="utf-8")
            return text

    raise SystemExit(
        "No PDF text extractor is available. Install pypdf/PyPDF2 or extract "
        f"{pdf_path} to {txt_path}, then rerun this script."
    )


def resolve_sources(source: str) -> list[Path]:
    if source == "all":
        return sorted(REFERENCES.glob("*.pdf"))

    pdf_path = REFERENCES / source
    if pdf_path.suffix.lower() != ".pdf":
        pdf_path = pdf_path.with_suffix(".pdf")
    return [pdf_path]


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Search bundled game-design references.")
    parser.add_argument("terms", nargs="+", help="Chinese or English terms to search")
    parser.add_argument("--context", type=int, default=160, help="Characters around each match")
    parser.add_argument("--limit", type=int, default=8, help="Maximum matches per term")
    parser.add_argument(
        "--source",
        default="all",
        help="Reference PDF filename, stem, or 'all' for every PDF in references/",
    )
    args = parser.parse_args()

    sources = resolve_sources(args.source)
    if not sources:
        raise SystemExit(f"No PDFs found in {REFERENCES}")

    texts = [(source, load_text_for_pdf(source)) for source in sources]
    exit_code = 0

    for term in args.terms:
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        matches: list[tuple[Path, re.Match[str], str]] = []
        for source, text in texts:
            matches.extend((source, match, text) for match in pattern.finditer(text))

        print(f"\n## {term}: {len(matches)} match(es)")
        if not matches:
            exit_code = 1
            continue

        for source, match, text in matches[: args.limit]:
            start = max(0, match.start() - args.context)
            end = min(len(text), match.end() + args.context)
            snippet = normalize_space(text[start:end])
            print(f"- [{source.name}] {snippet}")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
