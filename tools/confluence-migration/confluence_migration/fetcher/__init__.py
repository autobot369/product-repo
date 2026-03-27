"""
Fetcher — pulls all pages from configured Confluence spaces via MCP / REST API.

Writes: cache/pages.json
Schema: list of { id, title, space_key, labels, parent_id, body_storage, url }
"""

import json
from pathlib import Path

import certifi
import requests


def fetch_spaces(config: dict) -> None:
    pages = []
    parent_page_id = config.get("parent_page_id")

    if parent_page_id:
        # Scoped fetch: only descendants of a specific page
        space_key = config["spaces"][0]["key"]
        label = config.get("parent_page_label", parent_page_id)
        print(f"  Fetching descendants of page {parent_page_id} ({label}) in space {space_key}...")
        pages = _fetch_descendants(config, parent_page_id, space_key)
        print(f"    → {len(pages)} pages found")
    else:
        for space in config["spaces"]:
            print(f"  Fetching space: {space['key']} ({space['label']})...")
            space_pages = _fetch_space(config, space["key"])
            pages.extend(space_pages)
            print(f"    → {len(space_pages)} pages found")

    cache_path = Path(config["cache"]["dir"]) / "pages.json"
    with cache_path.open("w") as f:
        json.dump(pages, f, indent=2)

    print(f"  Total: {len(pages)} pages cached")


def _fetch_space(config: dict, space_key: str) -> list[dict]:
    """
    Fetch all pages in a space using Confluence REST API v1.
    Uses offset-based pagination (start parameter) until no next link is returned.
    """
    base_url = config["confluence"]["base_url"].rstrip("/")
    auth = (config["confluence"]["email"], config["confluence"]["api_token"])
    pages = []
    start = 0
    limit = 50

    while True:
        params = {
            "spaceKey": space_key,
            "expand": "body.storage,metadata.labels,ancestors",
            "limit": limit,
            "start": start,
        }

        resp = requests.get(
            f"{base_url}/wiki/rest/api/content",
            auth=auth,
            params=params,
            verify=certifi.where(),
        )
        resp.raise_for_status()
        data = resp.json()

        results = data.get("results", [])
        for page in results:
            pages.append({
                "id": page["id"],
                "title": page["title"],
                "space_key": space_key,
                "labels": [l["name"] for l in page.get("metadata", {}).get("labels", {}).get("results", [])],
                "parent_id": page["ancestors"][-1]["id"] if page.get("ancestors") else None,
                "body_storage": page.get("body", {}).get("storage", {}).get("value", ""),
                "url": f"{base_url}/wiki{page['_links']['webui']}",
            })

        # v1 API: stop when there's no "next" link or fewer results than limit
        if not data.get("_links", {}).get("next") or len(results) < limit:
            break
        start += limit

    return pages


def _fetch_descendants(config: dict, parent_id: str, space_key: str) -> list[dict]:
    """
    Fetch all descendant pages of a given parent page using the Confluence REST API.
    Uses offset-based pagination on the /descendant/page endpoint.
    """
    base_url = config["confluence"]["base_url"].rstrip("/")
    auth = (config["confluence"]["email"], config["confluence"]["api_token"])
    pages = []
    start = 0
    limit = 50

    while True:
        params = {
            "expand": "body.storage,metadata.labels,ancestors",
            "limit": limit,
            "start": start,
        }
        resp = requests.get(
            f"{base_url}/wiki/rest/api/content/{parent_id}/descendant/page",
            auth=auth,
            params=params,
            verify=certifi.where(),
        )
        resp.raise_for_status()
        data = resp.json()

        results = data.get("results", [])
        for page in results:
            pages.append({
                "id": page["id"],
                "title": page["title"],
                "space_key": space_key,
                "labels": [l["name"] for l in page.get("metadata", {}).get("labels", {}).get("results", [])],
                "parent_id": page["ancestors"][-1]["id"] if page.get("ancestors") else None,
                "body_storage": page.get("body", {}).get("storage", {}).get("value", ""),
                "url": f"{base_url}/wiki{page['_links']['webui']}",
            })

        if not data.get("_links", {}).get("next") or len(results) < limit:
            break
        start += limit

    return pages
