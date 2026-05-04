from __future__ import annotations

import re
from typing import Any

from .parser import Ticket

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _is_str_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(v, str) for v in value)


def validate_ticket(ticket: Ticket) -> list[str]:
    errors: list[str] = []
    fm = ticket.frontmatter

    title = fm.get("title")
    if not isinstance(title, str) or not title.strip():
        errors.append("`title` is required and must be a non-empty string")

    if "type" in fm and fm["type"] != "epic":
        errors.append(f"`type` must be exactly 'epic' (got {fm['type']!r})")

    if "weight" in fm:
        weight = fm["weight"]
        if not isinstance(weight, int) or isinstance(weight, bool) or weight < 0:
            errors.append(f"`weight` must be a non-negative integer (got {weight!r})")

    if "due_date" in fm:
        due = fm["due_date"]
        if not isinstance(due, str) or not DATE_RE.match(due):
            errors.append(f"`due_date` must be 'YYYY-MM-DD' (got {due!r})")

    if "labels" in fm and not _is_str_list(fm["labels"]):
        errors.append("`labels` must be a list of strings")

    if "assignees" in fm and not _is_str_list(fm["assignees"]):
        errors.append("`assignees` must be a list of strings")

    if "milestone" in fm and not isinstance(fm["milestone"], str):
        errors.append("`milestone` must be a string")

    if "epic" in fm:
        epic = fm["epic"]
        ok = epic == "auto" or (isinstance(epic, int) and not isinstance(epic, bool))
        if not ok:
            errors.append(f"`epic` must be 'auto' or an integer (got {epic!r})")

    return errors


def validate_pr_invariants(tickets: list[Ticket]) -> list[str]:
    errors: list[str] = []
    epic_files = [t.filename for t in tickets if t.is_epic]
    if len(epic_files) > 1:
        joined = ", ".join(epic_files)
        errors.append(
            f"At most one file with `type: epic` is allowed per PR (found {len(epic_files)}: {joined})"
        )
    return errors


def labels_for_ticket(ticket: Ticket) -> list[str]:
    """Compute the final label set the ticket would carry on GitHub.

    Adds a synthetic `weight:<N>` label when `weight` is set so the validator
    can confirm the label exists ahead of time.
    """
    labels = list(ticket.frontmatter.get("labels") or [])
    weight = ticket.frontmatter.get("weight")
    if isinstance(weight, int) and not isinstance(weight, bool):
        labels.append(f"weight:{weight}")
    return labels
