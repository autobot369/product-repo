"""
Claude API fallback classifier.
Called only when label and heuristic classifiers return 'unknown'.
Requires: ANTHROPIC_API_KEY environment variable.
"""

import os
import anthropic

_client = None


def _get_client():
    global _client
    if _client is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError("ANTHROPIC_API_KEY not set — cannot use Claude classifier fallback")
        _client = anthropic.Anthropic(api_key=api_key)
    return _client


PROMPT = """You are classifying Confluence pages for a product management repository.

Given this page title and the first 300 characters of its content, assign exactly one category:

- prd       → Product Requirement Document, product brief, feature definition
- abtest    → A/B test plan, experiment, hypothesis, test results
- spec      → Technical specification, design doc, RFC, system design
- skip      → Meeting notes, sprint ceremonies, personal pages, archived content

Page title: {title}
Content preview: {preview}

Reply with ONLY the category word. No explanation."""


def classify_with_claude(page: dict) -> tuple[str, str, str]:
    title = page.get("title", "")
    preview = page.get("body_storage", "")[:300]

    try:
        client = _get_client()
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=10,
            messages=[{"role": "user", "content": PROMPT.format(title=title, preview=preview)}],
        )
        category = message.content[0].text.strip().lower()
        if category not in ("prd", "abtest", "spec", "skip"):
            category = "unknown"
        return category, "claude", "Claude API classification"
    except Exception as e:
        return "unknown", "none", f"Claude fallback failed: {e}"
