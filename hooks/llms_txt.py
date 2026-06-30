"""
MkDocs hook - generates /llms.txt and /llms-full.txt for LLM navigation.

  llms.txt       Structured index of all pages with titles and URLs.
                 Follows the llms.txt convention (https://llmstxt.org).
  llms-full.txt  Full markdown content of every page concatenated,
                 for LLMs that need the complete corpus in one pass.

Both files are written to the site root after every build.

NOTE: This was created via an LLM for LLMs.
"""

import os
from mkdocs.structure.nav import Section, Link

_nav_index = []       # list of {title, url, src_path, breadcrumb}
_page_markdowns = {}  # src_path → {title, url, markdown}


# ---------------------------------------------------------------------------
# MkDocs event hooks
# ---------------------------------------------------------------------------

def on_nav(nav, config, files):
    """Walk the navigation tree and record every page in order."""
    global _nav_index, _page_markdowns
    _nav_index = []
    _page_markdowns = {}
    _walk(nav.items, _nav_index, [])


def on_page_markdown(markdown, page, config, files):
    """Capture raw markdown for each page (used by llms-full.txt)."""
    _page_markdowns[page.file.src_path] = {
        "title": page.title or page.file.src_path,
        "url": page.url,
        "markdown": markdown,
    }
    return markdown


def on_post_build(config):
    """Write llms.txt and llms-full.txt after the site is fully built."""
    site_dir = config["site_dir"]
    site_url = (config.get("site_url") or "").rstrip("/")
    site_name = config.get("site_name", "Documentation")
    site_description = config.get("site_description", "")

    # disabled for now
    #_write_llms_txt(site_dir, site_url, site_name, site_description)
    #_write_llms_full_txt(site_dir, site_url, site_name)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _walk(items, result, breadcrumb):
    """Recursively walk nav items, collecting Pages in order."""
    for item in items:
        if isinstance(item, Section):
            _walk(item.children or [], result, breadcrumb + [item.title])
        elif not isinstance(item, Link) and hasattr(item, "file") and item.file:
            result.append({
                "title": item.title or item.file.src_path,
                "url": item.url,
                "src_path": item.file.src_path,
                "breadcrumb": breadcrumb[:],
            })


def _abs_url(site_url, url):
    """Return an absolute URL if site_url is known, else root-relative."""
    clean = url.lstrip("/")
    return f"{site_url}/{clean}" if site_url else f"/{clean}"


def _write_llms_txt(site_dir, site_url, site_name, site_description):
    lines = [f"# {site_name}", ""]

    if site_description:
        lines += [f"> {site_description}", ""]

    lines += [
        "This file lists every page in the documentation.",
        "Each entry is a link you can fetch to read that page.",
        "Use llms-full.txt (linked at the bottom) to retrieve all content at once.",
        "",
    ]

    current_h2 = None

    for page in _nav_index:
        # Top-level breadcrumb element becomes the H2 section heading.
        h2 = page["breadcrumb"][0] if page["breadcrumb"] else None

        if h2 != current_h2:
            if current_h2 is not None:
                lines.append("")
            if h2:
                lines += [f"## {h2}", ""]
            current_h2 = h2

        url = _abs_url(site_url, page["url"])

        # Label shows sub-section hierarchy then page title.
        # e.g. "Garry's Mod > Command > Structure"
        parts = page["breadcrumb"][1:] + [page["title"]]
        label = " > ".join(filter(None, parts))
        lines.append(f"- [{label}]({url})")

    lines += [
        "",
        "## Optional",
        "",
        (
            f"- [llms-full.txt]({_abs_url(site_url, 'llms-full.txt')})"
            ": Full markdown content of every page in one file"
        ),
        "",
    ]

    out = os.path.join(site_dir, "llms.txt")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    print(f"  Generated llms.txt  ({len(_nav_index)} pages)")


def _write_llms_full_txt(site_dir, site_url, site_name):
    parts = [
        f"# {site_name} — Full Documentation",
        "",
        "This file contains the complete markdown source of every documentation page.",
        "Pages appear in the same order as the site navigation.",
        "",
    ]

    for page in _nav_index:
        data = _page_markdowns.get(page["src_path"])
        if not data:
            continue

        url = _abs_url(site_url, data["url"])
        divider = "─" * 72

        parts += [
            divider,
            f"# {data['title']}",
            f"> URL: {url}",
            "",
            data["markdown"],
            "",
        ]

    out = os.path.join(site_dir, "llms-full.txt")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(parts))

    print(f"  Generated llms-full.txt ({len(_page_markdowns)} pages)")
