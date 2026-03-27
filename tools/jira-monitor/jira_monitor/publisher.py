"""
Confluence publisher — prepends a new dated entry to an existing page.

Follows the same pattern as omni-researcher: most recent entry first,
prior entries preserved beneath it. Content is wrapped in Confluence
storage format (XHTML-like).
"""

from datetime import date

from .client import AtlassianClient


def prepend_entry(client: AtlassianClient, page_id: str, entry_markdown: str, scan_type: str) -> str:
    """
    Fetch `page_id`, prepend a new dated section, update the page.
    Returns the URL of the updated page.
    """
    page = client.confluence_get_page(page_id)
    title   = page["title"]
    version = page["version"]["number"]
    existing_body = page["body"]["storage"]["value"]

    today = date.today().isoformat()
    new_section = _markdown_to_storage(entry_markdown, today, scan_type)

    # Prepend new entry above existing content
    updated_body = new_section + "\n" + existing_body

    client.confluence_update_page(page_id, title, updated_body, version)

    base_url = client.base_url
    return f"{base_url}/wiki/pages/viewpage.action?pageId={page_id}"


def _markdown_to_storage(markdown: str, today: str, scan_type: str) -> str:
    """
    Wrap markdown report in minimal Confluence storage XML.
    Uses a rule + heading for separation between entries.
    """
    # Escape basic XML characters in the body
    escaped = (
        markdown
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

    # Re-allow intentional line breaks and preserve paragraph structure
    paragraphs = escaped.strip().split("\n\n")
    storage_paragraphs = "".join(f"<p>{p.replace(chr(10), '<br/>')}</p>" for p in paragraphs)

    return (
        f'<hr/>'
        f'<h2>{today} — {scan_type}</h2>'
        f'{storage_paragraphs}'
    )
