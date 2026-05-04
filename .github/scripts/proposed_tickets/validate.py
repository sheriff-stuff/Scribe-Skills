from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from .parser import Ticket, parse_directory
from .remote import GitHubClient, GitHubError
from .schema import labels_for_ticket, validate_pr_invariants, validate_ticket


def _remote_checks(
    tickets: list[Ticket], client: GitHubClient
) -> dict[str, list[str]]:
    errors: dict[str, list[str]] = {t.filename: [] for t in tickets}

    try:
        existing_labels = client.list_label_names()
    except GitHubError as e:
        for fn in errors:
            errors[fn].append(f"Could not list labels: {e}")
        return errors

    try:
        existing_milestones = client.list_milestone_titles()
    except GitHubError as e:
        for fn in errors:
            errors[fn].append(f"Could not list milestones: {e}")
        return errors

    for t in tickets:
        for label in labels_for_ticket(t):
            if label not in existing_labels:
                errors[t.filename].append(
                    f"Label {label!r} does not exist on the repo (create it first)"
                )

        milestone = t.frontmatter.get("milestone")
        if isinstance(milestone, str) and milestone not in existing_milestones:
            errors[t.filename].append(
                f"Milestone {milestone!r} is not an open milestone on the repo"
            )

        epic_ref = t.frontmatter.get("epic")
        if isinstance(epic_ref, int) and not isinstance(epic_ref, bool):
            try:
                issue = client.get_issue(epic_ref)
            except GitHubError as e:
                errors[t.filename].append(f"Could not look up epic #{epic_ref}: {e}")
            else:
                if issue is None:
                    errors[t.filename].append(
                        f"`epic: {epic_ref}` does not resolve to an existing issue"
                    )

    return errors


def run(directory: Path, *, offline: bool, client: GitHubClient | None) -> int:
    tickets, parse_errors = parse_directory(directory)

    file_errors: dict[str, list[str]] = {}
    for path, msg in parse_errors:
        file_errors.setdefault(path.name, []).append(msg)

    for t in tickets:
        for msg in validate_ticket(t):
            file_errors.setdefault(t.filename, []).append(msg)

    pr_errors = validate_pr_invariants(tickets)

    if not offline and client is not None and tickets:
        for fn, errs in _remote_checks(tickets, client).items():
            if errs:
                file_errors.setdefault(fn, []).extend(errs)

    return _emit(directory, tickets, parse_errors, file_errors, pr_errors)


def _emit(
    directory: Path,
    tickets: list[Ticket],
    parse_errors: list,
    file_errors: dict[str, list[str]],
    pr_errors: list[str],
) -> int:
    all_files = sorted(
        {t.filename for t in tickets} | {p.name for p, _ in parse_errors}
    )

    lines: list[str] = []
    lines.append(f"# Proposed tickets validation\n")
    lines.append(f"Scanned `{directory}` — {len(all_files)} file(s).\n")

    has_failures = bool(pr_errors) or any(file_errors.get(fn) for fn in all_files)

    if pr_errors:
        lines.append("## PR-wide errors\n")
        for msg in pr_errors:
            lines.append(f"- {msg}")
        lines.append("")

    if all_files:
        lines.append("## Per-file results\n")
        for fn in all_files:
            errs = file_errors.get(fn, [])
            if errs:
                lines.append(f"- ❌ `{fn}`")
                for msg in errs:
                    lines.append(f"  - {msg}")
            else:
                lines.append(f"- ✅ `{fn}`")
        lines.append("")

    if not has_failures:
        lines.append("All proposed tickets are valid.\n")

    summary = "\n".join(lines)
    print(summary)

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write(summary)

    return 1 if has_failures else 0


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate proposed-ticket markdown files")
    parser.add_argument("directory", type=Path, help="Directory containing *.md ticket files")
    parser.add_argument(
        "--offline", action="store_true", help="Skip remote (GitHub API) checks"
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv if argv is not None else sys.argv[1:])
    if not args.directory.is_dir():
        print(f"Directory not found: {args.directory}", file=sys.stderr)
        return 2

    client: GitHubClient | None = None
    if not args.offline:
        token = os.environ.get("GITHUB_TOKEN")
        repo = os.environ.get("GITHUB_REPOSITORY")
        if not token or not repo or "/" not in repo:
            print(
                "GITHUB_TOKEN and GITHUB_REPOSITORY (owner/repo) are required for remote checks. "
                "Pass --offline to skip them.",
                file=sys.stderr,
            )
            return 2
        owner, repo_name = repo.split("/", 1)
        client = GitHubClient(owner, repo_name, token)

    return run(args.directory, offline=args.offline, client=client)


if __name__ == "__main__":
    sys.exit(main())
