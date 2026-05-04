from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


class FrontmatterError(ValueError):
    pass


@dataclass
class Ticket:
    path: Path
    frontmatter: dict[str, Any]
    body: str

    @property
    def filename(self) -> str:
        return self.path.name

    @property
    def is_epic(self) -> bool:
        return self.frontmatter.get("type") == "epic"


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"):
        raise FrontmatterError("File does not start with '---' frontmatter delimiter")

    after_open = text.split("\n", 1)
    if len(after_open) < 2:
        raise FrontmatterError("Frontmatter is missing a closing '---'")

    rest = after_open[1]
    end_marker = "\n---"
    end_idx = rest.find(end_marker)
    if end_idx == -1:
        raise FrontmatterError("Frontmatter is missing a closing '---'")

    fm_text = rest[:end_idx]
    body = rest[end_idx + len(end_marker):]
    if body.startswith("\n"):
        body = body[1:]

    try:
        loaded = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError as e:
        raise FrontmatterError(f"Invalid YAML in frontmatter: {e}") from e

    if not isinstance(loaded, dict):
        raise FrontmatterError("Frontmatter must be a YAML mapping")

    return loaded, body


def parse_file(path: Path) -> Ticket:
    text = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    return Ticket(path=path, frontmatter=fm, body=body)


def parse_directory(directory: Path) -> tuple[list[Ticket], list[tuple[Path, str]]]:
    tickets: list[Ticket] = []
    errors: list[tuple[Path, str]] = []
    for path in sorted(directory.glob("*.md")):
        try:
            tickets.append(parse_file(path))
        except FrontmatterError as e:
            errors.append((path, str(e)))
    return tickets, errors
