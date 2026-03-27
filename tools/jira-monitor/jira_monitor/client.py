"""
Jira + Confluence REST client.

All requests use HTTP Basic Auth (email + API token) against the
Atlassian Cloud REST APIs:
  Jira v3:       /rest/api/3/
  Confluence v1: /wiki/rest/api/
"""

import certifi
import requests
from requests.auth import HTTPBasicAuth


class AtlassianClient:
    def __init__(self, config: dict):
        self.base_url = config["atlassian"]["base_url"].rstrip("/")
        self.auth     = HTTPBasicAuth(
            config["atlassian"]["email"],
            config["atlassian"]["api_token"],
        )
        self.session = requests.Session()
        self.session.auth    = self.auth
        self.session.verify  = certifi.where()
        self.session.headers.update({"Accept": "application/json"})

    # ── Jira ─────────────────────────────────────────────────────────────────

    def jira_get(self, path: str, params: dict = None) -> dict:
        resp = self.session.get(f"{self.base_url}/rest/api/3/{path.lstrip('/')}", params=params)
        resp.raise_for_status()
        return resp.json()

    def search_issues(self, jql: str, fields: list[str], max_results: int = 100) -> list[dict]:
        """Paginate through all issues matching a JQL query."""
        issues, start = [], 0
        fields_str = ",".join(fields)
        while True:
            data = self.jira_get("search", {
                "jql":        jql,
                "fields":     fields_str,
                "startAt":    start,
                "maxResults": 50,
            })
            batch = data.get("issues", [])
            issues.extend(batch)
            if len(batch) < 50 or len(issues) >= max_results:
                break
            start += len(batch)
        return issues

    def get_active_sprint(self, board_id: int) -> dict | None:
        """Return the active sprint for a board, or None."""
        data = self.jira_get(f"board/{board_id}/sprint", {"state": "active"})
        sprints = data.get("values", [])
        return sprints[0] if sprints else None

    def get_boards(self, project_key: str) -> list[dict]:
        data = self.jira_get("board", {"projectKeyOrId": project_key})
        return data.get("values", [])

    def get_sprint_issues(self, sprint_id: int, fields: list[str]) -> list[dict]:
        return self.search_issues(
            jql=f"sprint = {sprint_id}",
            fields=fields,
        )

    def get_versions(self, project_key: str) -> list[dict]:
        return self.jira_get(f"project/{project_key}/versions") or []

    # ── Confluence ───────────────────────────────────────────────────────────

    def confluence_get_page(self, page_id: str) -> dict:
        resp = self.session.get(
            f"{self.base_url}/wiki/rest/api/content/{page_id}",
            params={"expand": "body.storage,version"},
        )
        resp.raise_for_status()
        return resp.json()

    def confluence_update_page(self, page_id: str, title: str, body: str, version: int) -> None:
        payload = {
            "id":      page_id,
            "type":    "page",
            "title":   title,
            "version": {"number": version + 1},
            "body": {
                "storage": {
                    "value":          body,
                    "representation": "storage",
                }
            },
        }
        resp = self.session.put(
            f"{self.base_url}/wiki/rest/api/content/{page_id}",
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        resp.raise_for_status()
