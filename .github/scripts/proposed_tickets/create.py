from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Any

from .parser import Ticket, parse_directory
from .remote import GitHubClient, GitHubError
from .schema import labels_for_ticket, validate_pr_invariants, validate_ticket
from .validate import _remote_checks


def _marker(filename: str) -> str:
    return f"<!-- proposed-ticket: {filename} -->"


def _build_payload(
    ticket: Ticket, milestones: dict[str, int]
) -> dict[str, Any]:
    fm = ticket.frontmatter
    body_parts: list[str] = []
    if ticket.body.strip():
        body_parts.append(ticket.body.rstrip())

    due = fm.get("due_date")
    if isinstance(due, str):
        body_parts.append(f"\n**Due:** {due}")

    body_parts.append(f"\n{_marker(ticket.filename)}")

    payload: dict[str, Any] = {
        "title": fm["title"],
        "body": "\n".join(body_parts).strip() + "\n",
        "labels": labels_for_ticket(ticket),
    }
    assignees = fm.get("assignees")
    if isinstance(assignees, list) and assignees:
        payload["assignees"] = list(assignees)

    milestone = fm.get("milestone")
    if isinstance(milestone, str) and milestone in milestones:
        payload["milestone"] = milestones[milestone]

    return payload


def _run_validation(
    tickets: list[Ticket],
    parse_errors: list,
    client: GitHubClient,
) -> list[str]:
    errors: list[str] = []
    for path, msg in parse_errors:
        errors.append(f"{path.name}: {msg}")

    for t in tickets:
        for msg in validate_ticket(t):
            errors.append(f"{t.filename}: {msg}")

    errors.extend(validate_pr_invariants(tickets))

    if tickets:
        for fn, errs in _remote_checks(tickets, client).items():
            for msg in errs:
                errors.append(f"{fn}: {msg}")

    return errors


def _create_one(
    ticket: Ticket,
    client: GitHubClient,
    milestones: dict[str, int],
) -> dict[str, Any]:
    marker = _marker(ticket.filename)
    existing = client.find_issue_by_marker(marker)
    if existing is not None:
        return {"issue": existing, "reused": True}

    payload = _build_payload(ticket, milestones)
    issue = client.create_issue(payload)
    return {"issue": issue, "reused": False}


def run(directory: Path, client: GitHubClient) -> int:
    tickets, parse_errors = parse_directory(directory)

    if parse_errors or tickets:
        validation_errors = _run_validation(tickets, parse_errors, client)
        if validation_errors:
            _write_summary(
                "# Proposed tickets create — aborted\n\nValidation failed:\n"
                + "\n".join(f"- {e}" for e in validation_errors)
                + "\n"
            )
            return 1

    if not tickets:
        _write_summary("# Proposed tickets create\n\nNo ticket files found. Nothing to do.\n")
        return 0

    milestones = client.list_milestone_titles()

    epic_ticket = next((t for t in tickets if t.is_epic), None)
    children = [t for t in tickets if not t.is_epic]

    created: list[dict[str, Any]] = []
    failed: list[tuple[str, str]] = []
    epic_issue: dict | None = None

    if epic_ticket is not None:
        try:
            result = _create_one(epic_ticket, client, milestones)
            epic_issue = result["issue"]
            created.append({"ticket": epic_ticket, **result})
            epic_ticket.path.unlink(missing_ok=True)
        except GitHubError as e:
            failed.append((epic_ticket.filename, str(e)))
            children = []  # don't try to attach sub-issues to a non-existent epic

    for t in children:
        try:
            result = _create_one(t, client, milestones)
            child_issue = result["issue"]

            epic_ref = t.frontmatter.get("epic")
            if isinstance(epic_ref, int) and not isinstance(epic_ref, bool):
                client.attach_subissue(epic_ref, child_issue["id"])
            elif epic_ref == "auto" and epic_issue is not None:
                client.attach_subissue(epic_issue["number"], child_issue["id"])

            created.append({"ticket": t, **result})
            t.path.unlink(missing_ok=True)
        except GitHubError as e:
            failed.append((t.filename, str(e)))

    _write_summary(_format_summary(created, failed))
    return 0 if not failed else 1


def _format_summary(
    created: list[dict[str, Any]], failed: list[tuple[str, str]]
) -> str:
    lines = ["# Proposed tickets create\n"]
    if created:
        lines.append("## Created\n")
        for entry in created:
            t: Ticket = entry["ticket"]
            issue = entry["issue"]
            tag = " (existing)" if entry.get("reused") else ""
            url = issue.get("html_url", "")
            lines.append(f"- `{t.filename}` → [#{issue['number']}]({url}){tag}")
        lines.append("")
    if failed:
        lines.append("## Failed (left on disk for retry)\n")
        for fn, msg in failed:
            lines.append(f"- `{fn}` — {msg}")
        lines.append("")
    if not created and not failed:
        lines.append("Nothing to report.\n")
    return "\n".join(lines)


def _write_summary(text: str) -> None:
    print(text)
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write(text)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create GitHub issues from proposed tickets")
    parser.add_argument("directory", type=Path, help="Directory containing *.md ticket files")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv if argv is not None else sys.argv[1:])
    if not args.directory.is_dir():
        print(f"Directory not found: {args.directory}", file=sys.stderr)
        return 2

    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo or "/" not in repo:
        print("GITHUB_TOKEN and GITHUB_REPOSITORY (owner/repo) are required.", file=sys.stderr)
        return 2

    owner, repo_name = repo.split("/", 1)
    client = GitHubClient(owner, repo_name, token)
    return run(args.directory, client)


if __name__ == "__main__":
    sys.exit(main())
