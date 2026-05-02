"""Generator for the Cortex mock wiki.

Reads the page spec from outline.py, validates internal references,
and emits markdown files into the wiki root (one directory above this script).

Run from anywhere:
    python generate.py

The generator is idempotent: running it repeatedly produces identical output.
"""
from __future__ import annotations

import os.path
import re
import sys
from pathlib import Path, PurePosixPath

THIS_DIR = Path(__file__).resolve().parent
WIKI_ROOT = THIS_DIR.parent
sys.path.insert(0, str(THIS_DIR))

from outline import GLOSSARY, LINK_SENTINEL, PAGES, Page  # noqa: E402


CATEGORY_LABELS = {
    "root": "Wiki root",
    "architecture": "Architecture",
    "domain": "Domain model",
    "services": "Services",
    "frontend": "Frontend",
    "ops": "Operations",
    "process": "Process",
    "adrs": "Architectural decision records",
}

CATEGORY_ORDER = [
    "root",
    "architecture",
    "domain",
    "services",
    "frontend",
    "ops",
    "process",
    "adrs",
]


SENTINEL_LINK_RE = re.compile(
    rf"\]\({re.escape(LINK_SENTINEL)}([^)]+)\)"
)
RAW_SENTINEL_RE = re.compile(re.escape(LINK_SENTINEL) + r"([^\s)]+)")


def relative_link(from_page_path: str, to_slug: str) -> str:
    """Relative path from one page to another's slug.

    `from_page_path` is the source page's wiki-root-relative path (with
    `.md`); `to_slug` is the target's wiki-root-relative path without
    the `.md` extension. Always emits POSIX separators."""
    from_dir = PurePosixPath(from_page_path).parent
    target = PurePosixPath(to_slug)
    rel = os.path.relpath(target.as_posix(), from_dir.as_posix() or ".")
    return rel.replace("\\", "/")


def resolve_links(body: str, page_path: str) -> str:
    """Rewrite sentinel link targets in `body` to relative paths from
    the page at `page_path`."""
    def repl(match: re.Match[str]) -> str:
        slug = match.group(1)
        return f"]({relative_link(page_path, slug)})"

    return SENTINEL_LINK_RE.sub(repl, body)


def validate(pages: list[Page]) -> None:
    """Sanity-check the outline before writing anything."""
    paths_seen: dict[str, Page] = {}
    for page in pages:
        if page.path in paths_seen:
            raise ValueError(f"Duplicate page path: {page.path}")
        paths_seen[page.path] = page
        if page.category not in CATEGORY_LABELS:
            raise ValueError(
                f"Unknown category {page.category!r} on page {page.path}"
            )

    valid_slugs = {p.path.removesuffix(".md") for p in pages}
    for page in pages:
        for heading, body in page.sections:
            for match in RAW_SENTINEL_RE.finditer(body):
                slug = match.group(1)
                if slug not in valid_slugs:
                    raise ValueError(
                        f"{page.path} (section {heading!r}) links to "
                        f"missing page: {slug}"
                    )

    for term in GLOSSARY:
        if not term.strip():
            raise ValueError("Empty glossary term")


def render_frontmatter(page: Page) -> str:
    fields = {
        "title": page.title,
        "category": page.category,
        **page.frontmatter,
    }
    lines = ["---"]
    for key, value in fields.items():
        if isinstance(value, list):
            inner = ", ".join(str(v) for v in value)
            lines.append(f"{key}: [{inner}]")
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines)


def render_page(page: Page) -> str:
    parts = [render_frontmatter(page), "", f"# {page.title}", ""]
    for heading, body in page.sections:
        if heading:
            parts.append(f"## {heading}")
            parts.append("")
        parts.append(resolve_links(body.strip(), page.path))
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def render_glossary_page() -> Page:
    body_lines: list[str] = []
    for term in sorted(GLOSSARY):
        body_lines.append(f"### {term}")
        body_lines.append("")
        body_lines.append(GLOSSARY[term].strip())
        body_lines.append("")
    body = "\n".join(body_lines).rstrip()
    return Page(
        path="glossary.md",
        title="Glossary",
        category="root",
        frontmatter={"owners": "[docs-team]", "last_updated": "2026-04-15"},
        sections=[
            (
                "Purpose",
                "Canonical vocabulary for the Cortex project. Every other "
                "page in this wiki uses these terms; if a concept doesn't "
                "appear here, it doesn't exist in Cortex's domain model.",
            ),
            ("Terms", body),
        ],
    )


def render_index_page(pages: list[Page]) -> Page:
    by_category: dict[str, list[Page]] = {c: [] for c in CATEGORY_ORDER}
    for p in pages:
        if p.path == "index.md":
            continue
        by_category.setdefault(p.category, []).append(p)

    sections: list[tuple[str, str]] = [
        (
            "About this wiki",
            "Design corpus for **Cortex**, a local meeting-transcription "
            "app. This index lists every page grouped by area. Start with "
            f"[System Overview]({LINK_SENTINEL}architecture/system-overview) "
            f"if you're new, or jump to [Glossary]({LINK_SENTINEL}glossary) "
            "for canonical vocabulary.",
        )
    ]

    for category in CATEGORY_ORDER:
        items = sorted(by_category.get(category, []), key=lambda p: p.title)
        if not items:
            continue
        body_lines = []
        for p in items:
            slug = p.path.removesuffix(".md")
            body_lines.append(f"- [{p.title}]({LINK_SENTINEL}{slug})")
        sections.append((CATEGORY_LABELS[category], "\n".join(body_lines)))

    return Page(
        path="index.md",
        title="Cortex wiki",
        category="root",
        frontmatter={"owners": "[docs-team]", "last_updated": "2026-04-15"},
        sections=sections,
    )


def write_pages(pages: list[Page]) -> None:
    cleaned: set[Path] = set()
    written = 0
    for page in pages:
        target = WIKI_ROOT / page.path
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.parent not in cleaned and target.parent != WIKI_ROOT:
            cleaned.add(target.parent)
        target.write_text(render_page(page), encoding="utf-8", newline="\n")
        written += 1
    print(f"wrote {written} pages")


def check_glossary_coverage(pages: list[Page]) -> None:
    """Soft check: warn if a glossary term is never referenced."""
    all_text = "\n".join(
        body for p in pages for _, body in p.sections
    ).lower()
    orphans = [t for t in GLOSSARY if t.lower() not in all_text]
    if orphans:
        print(
            "warning: glossary terms not referenced anywhere: "
            + ", ".join(orphans)
        )


def main() -> int:
    pages = list(PAGES)
    pages.append(render_glossary_page())
    pages.append(render_index_page(pages))
    validate(pages)
    write_pages(pages)
    check_glossary_coverage(pages)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
