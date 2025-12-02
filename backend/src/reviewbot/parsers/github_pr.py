from __future__ import annotations

import re

import httpx


_PR_PATTERN = re.compile(
    r"https?://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)/pull/(?P<number>\d+)"
)


async def fetch_pr_diff(url: str, token: str | None = None) -> str:
    m = _PR_PATTERN.search(url)
    if not m:
        raise ValueError(f"Invalid GitHub PR URL: {url!r}")

    owner, repo, number = m.group("owner"), m.group("repo"), m.group("number")
    api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{number}"

    headers: dict[str, str] = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(api_url, headers=headers)
        if resp.status_code == 404:
            raise ValueError(f"PR not found: {owner}/{repo}#{number}")
        resp.raise_for_status()

        pr_data = resp.json()
        diff_url = pr_data.get("diff_url") or f"{api_url}.diff"

        diff_resp = await client.get(diff_url, headers=headers, follow_redirects=True)
        diff_resp.raise_for_status()
        return diff_resp.text
