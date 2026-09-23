"""Rewrite links to directory sections (e.g. ./01-architecture/) into links to
their landing page, so navigation tables on the homepage resolve.

This is a build-time transform and does not touch the source Markdown, so the
content files stay identical to upstream for easy sync. It relies on the leaf
page having H1 titles (MkDocs derives the page title from the H1).
"""

from pathlib import Path

# directory name -> landing file name (relative to that directory)
LANDING = {
    "01-architecture": "README.md",
    "02-build": "README.md",
    "03-run": "README.md",
    "04-governance": "治理篇导读.md",
    "05-optimization": "调优篇导读.md",
    "06-case-study": "README.md",
    "07-conclusion": "第 30 章 从 Agentic Application 到 Agentic OS.md",
}


def resolve(link, base_dir, docs_dir):
    """Given a markdown link target ending in '/', return rewritten target or
    the original grandparent link if no landing page is known."""
    # strip leading ./
    t = link[2:] if link.startswith("./") else link
    if t.startswith(("http", "#", "/")) or "://" in t:
        return None
    # normalize path relative to the source file's directory
    abs_dir = (Path(base_dir) / t).resolve()
    # find a landing file: the directory's own name (for nested case dirs)
    # or a configured LANDING entry
    name = abs_dir.name
    if name in LANDING:
        landing = LANDING[name]
    else:
        # nested case-study dirs have a single .md per case (leaf); skip dirs
        landing = None
        # For 第xx章 主题 dirs, LANDING not present -> leave as is (no landing page)
    if landing is None:
        return None
    candidate = abs_dir / landing
    if candidate.exists():
        # return path relative to docs_dir, in url form
        rel = candidate.relative_to(docs_dir).as_posix()
        return rel
    return None


def on_page_markdown(markdown, *, page, config, files):
    import re

    docs_dir = Path(config["docs_dir"]).resolve()
    src_uri = page.file.src_uri
    base_dir = docs_dir / (src_uri.rsplit("/", 1)[0] if "/" in src_uri else "")

    def repl(m):
        label, target = m.group(1), m.group(2)
        if not target.endswith("/"):
            return m.group(0)
        new = resolve(target, base_dir, docs_dir)
        return f"[{label}]({new})" if new else m.group(0)

    return re.sub(r"\[([^\]]*)\]\(([^)]*)\)", repl, markdown)
