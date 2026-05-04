from __future__ import annotations

from typing import Any

import requests


class GitHubError(RuntimeError):
    pass


class GitHubClient:
    def __init__(self, owner: str, repo: str, token: str):
        self.owner = owner
        self.repo = repo
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {token}",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "proposed-tickets-ci",
            }
        )

    def _url(self, path: str) -> str:
        return f"https://api.github.com/repos/{self.owner}/{self.repo}{path}"

    def _paginate(self, url: str, params: dict[str, Any] | None = None) -> list[dict]:
        out: list[dict] = []
        next_url: str | None = url
        next_params = dict(params or {})
        next_params.setdefault("per_page", 100)
        while next_url:
            resp = self.session.get(next_url, params=next_params)
            if resp.status_code >= 400:
                raise GitHubError(f"GET {next_url} failed: {resp.status_code} {resp.text}")
            out.extend(resp.json())
            next_url = resp.links.get("next", {}).get("url")
            next_params = {}
        return out

    def list_label_names(self) -> set[str]:
        labels = self._paginate(self._url("/labels"))
        return {label["name"] for label in labels}

    def list_milestone_titles(self) -> dict[str, int]:
        milestones = self._paginate(self._url("/milestones"), {"state": "open"})
        return {m["title"]: m["number"] for m in milestones}

    def get_issue(self, number: int) -> dict | None:
        resp = self.session.get(self._url(f"/issues/{number}"))
        if resp.status_code == 404:
            return None
        if resp.status_code >= 400:
            raise GitHubError(f"GET issue #{number} failed: {resp.status_code} {resp.text}")
        return resp.json()

    def find_issue_by_marker(self, marker: str) -> dict | None:
        query = f'repo:{self.owner}/{self.repo} in:body "{marker}"'
        resp = self.session.get(
            "https://api.github.com/search/issues",
            params={"q": query, "per_page": 10},
        )
        if resp.status_code >= 400:
            raise GitHubError(f"Search failed: {resp.status_code} {resp.text}")
        for item in resp.json().get("items", []):
            if marker in (item.get("body") or ""):
                return item
        return None

    def create_issue(self, payload: dict[str, Any]) -> dict:
        resp = self.session.post(self._url("/issues"), json=payload)
        if resp.status_code >= 400:
            raise GitHubError(f"Create issue failed: {resp.status_code} {resp.text}")
        return resp.json()

    def attach_subissue(self, parent_number: int, child_id: int) -> None:
        url = self._url(f"/issues/{parent_number}/sub_issues")
        resp = self.session.post(url, json={"sub_issue_id": child_id})
        if resp.status_code >= 400:
            raise GitHubError(
                f"Attach sub-issue {child_id} -> #{parent_number} failed: "
                f"{resp.status_code} {resp.text}"
            )
