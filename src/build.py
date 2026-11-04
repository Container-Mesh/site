#!/usr/bin/env python3
"""Build the public site into public/, and refuse private-product wording."""

import filecmp
import posixpath
import re
import shutil
import sys
import tempfile
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "src" / "content"
ASSETS = ROOT / "src" / "assets"
PUBLIC = ROOT / "public"

DOCS = [
    ("Overview", "/docs/", "docs/index.html"),
    ("First launch", "/docs/first-launch/", "docs/first-launch.html"),
    ("Names", "/docs/names/", "docs/names.html"),
    ("Containers", "/docs/containers/", "docs/containers.html"),
    ("Connection", "/docs/connection/", "docs/connection.html"),
    ("Settings", "/docs/settings/", "docs/settings.html"),
    ("Troubleshooting", "/docs/troubleshooting/", "docs/troubleshooting.html"),
    ("Bugs and security", "/docs/support/", "docs/support.html"),
]

REQUIRED = [
    "Enable automatic networking",
    "ContainerTunnel",
    "mesh.test",
    "www.containermesh.app",
    "www.containermesh.dev",
    "Aphelion Works",
]

# Public pages must not describe the private helper, signing, or unreleased work.
FORBIDDEN = re.compile(
    r"helper|notar|Developer ID|WireGuard|LaunchDaemon|LaunchAgent|\butun\b|\bsudo\b|"
    r"github\.com/Container-Mesh/(?:mesh|tunnel)|NET_ADMIN|\bprivileged\b|"
    r"\b(?:code[\s-]?sign|notariz\w*|unreleased)\b",
    re.IGNORECASE,
)


def parse(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("<!--") or "-->" not in text:
        raise SystemExit(f"{path} needs a title comment")
    raw, body = text[4:].split("-->", 1)
    meta = {}
    for line in raw.strip().splitlines():
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    for key in ("title", "description"):
        if key not in meta:
            raise SystemExit(f"{path} is missing {key}")
    return meta, body.strip()


def rel(from_path: str, target: str) -> str:
    """Page-relative URL, so GitHub Pages and the custom domains share one tree."""
    from_dir = from_path if from_path.endswith("/") else from_path.rsplit("/", 1)[0] + "/"
    result = posixpath.relpath(target, from_dir)
    if target.endswith("/") and not result.endswith("/"):
        result += "/"
    return "./" if result == "." else result


def rewrite_local_urls(body: str, from_path: str) -> str:
    def replace(match: re.Match[str]) -> str:
        url = match.group(2)
        if not url.startswith("/") or url.startswith("//"):
            return match.group(0)
        return f'{match.group(1)}="{rel(from_path, url)}"'

    return re.sub(r'(?<![\w-])(href|src)="([^"]*)"', replace, body)


def page(meta: dict[str, str], body: str, path: str, kind: str) -> str:
    canonical_origin = "https://www.containermesh.app" if kind == "home" else "https://www.containermesh.dev"
    canonical = canonical_origin + path
    docs_current = ' aria-current="page"' if path.startswith("/docs") else ""
    side = ""
    if kind == "doc":
        links = []
        for label, href, _source in DOCS:
            current = ' aria-current="page"' if href == path else ""
            links.append(
                f'<a data-docs-href="{href}" href="{rel(path, href)}"{current}>{escape(label)}</a>'
            )
        side = '<nav class="side" aria-label="Documentation">' + "".join(links) + "</nav>"
        body = f'<div class="doc">{side}<article class="prose">{rewrite_local_urls(body, path)}</article></div>'
    else:
        body = rewrite_local_urls(body, path)
    structured = ""
    if kind == "home":
        structured = """
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"SoftwareApplication","name":"ContainerMesh","applicationCategory":"DeveloperApplication","operatingSystem":"macOS","url":"https://www.containermesh.app/","description":"A macOS menu-bar app that discovers Docker containers and connects to them through ContainerTunnel."}
</script>"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(meta["title"])}</title>
<meta name="description" content="{escape(meta["description"])}">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="{rel(path, "/assets/favicon.png")}" type="image/png">
<link rel="apple-touch-icon" href="{rel(path, "/assets/apple-touch-icon.png")}">
<meta name="theme-color" content="#B8360B">
<meta property="og:title" content="{escape(meta["title"])}">
<meta property="og:description" content="{escape(meta["description"])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{canonical_origin}/assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="{rel(path, "/assets/site.css")}">
<script src="{rel(path, "/assets/host.js")}" defer></script>{structured}
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<header class="bar">
  <a class="brand" data-app-href="/" href="{rel(path, "/")}"><img src="{rel(path, "/assets/app-icon.png")}" width="36" height="36" alt=""><span>ContainerMesh</span></a>
  <nav aria-label="Site">
    <a data-docs-href="/docs/" href="{rel(path, "/docs/")}"{docs_current}>Documentation</a>
    <a href="https://github.com/Container-Mesh/site/issues/new?template=bug_report.yml">Report a bug</a>
  </nav>
</header>
<main id="content" class="wrap">
{body}
</main>
<footer class="site-footer">
  <p>© 2026 <a href="https://github.com/Aphelion-Works">Aphelion Works</a> · <a class="contact" href="#contact">Contact</a> · <a href="https://github.com/Container-Mesh/site/security/policy">Security reports stay private</a></p>
</footer>
</body>
</html>
"""


def not_found() -> str:
    meta = {
        "title": "Page not found",
        "description": "That ContainerMesh page is not on this site.",
    }
    body = """
<h1>That page is not here.</h1>
<p class="lede">The product home and the documentation are the two public sites.</p>
<div class="actions">
  <a class="button" data-app-href="/" href="/">Product home</a>
  <a class="button quiet" data-docs-href="/docs/" href="/docs/">Documentation</a>
</div>
"""
    return page(meta, body, "/404.html", "home").replace(
        "https://www.containermesh.app/404.html",
        "https://www.containermesh.app/",
    )


def build(destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    shutil.copytree(ASSETS, destination / "assets")
    pages = [(CONTENT / "home.html", "/", "home")]
    for _label, href, source in DOCS:
        pages.append((CONTENT / source, href, "doc"))
    written = []
    for source, href, kind in pages:
        meta, body = parse(source)
        target = destination / "index.html" if href == "/" else destination / href.strip("/") / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page(meta, body, href, kind), encoding="utf-8")
        written.append(target)
    (destination / "404.html").write_text(not_found(), encoding="utf-8")
    (destination / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: https://www.containermesh.app/sitemap.xml\n",
        encoding="utf-8",
    )
    locs = ["https://www.containermesh.app/"] + [
        "https://www.containermesh.dev" + href for _label, href, _source in DOCS
    ]
    urls = "\n".join(f"  <url><loc>{loc}</loc></url>" for loc in locs)
    (destination / "sitemap.xml").write_text(
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n"
        f"{urls}\n</urlset>\n",
        encoding="utf-8",
    )
    (destination / ".nojekyll").write_text("", encoding="utf-8")
    (destination / "_headers").write_text(
        "/*\n"
        "  X-Content-Type-Options: nosniff\n"
        "  Referrer-Policy: strict-origin-when-cross-origin\n"
        "  X-Frame-Options: DENY\n"
        "  Content-Security-Policy: default-src 'self'; style-src 'self'; img-src 'self'; script-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'\n"
        "  Permissions-Policy: camera=(), microphone=(), geolocation=()\n",
        encoding="utf-8",
    )
    blob = "\n".join(path.read_text(encoding="utf-8") for path in written)
    blob += (destination / "404.html").read_text(encoding="utf-8")
    missing = [item for item in REQUIRED if item not in blob]
    if missing:
        raise SystemExit("missing public copy: " + ", ".join(missing))
    scan_tree(destination)
    scan_sources()


def scan_tree(destination: Path) -> None:
    for path in destination.rglob("*"):
        if path.suffix.lower() in {".html", ".css", ".js", ".txt", ".xml"}:
            found = FORBIDDEN.search(path.read_text(encoding="utf-8"))
            if found:
                raise SystemExit(f"{path} contains private wording: {found.group(0)}")


def scan_sources() -> None:
    roots = [CONTENT, ROOT / "functions", ROOT / "README.md", ROOT / "SECURITY.md"]
    for root in roots:
        paths = [root] if root.is_file() else root.rglob("*")
        for path in paths:
            if path.is_file() and path.suffix.lower() in {".html", ".js", ".md", ""}:
                found = FORBIDDEN.search(path.read_text(encoding="utf-8"))
                if found:
                    raise SystemExit(f"{path} contains private wording: {found.group(0)}")


def same_tree(left: Path, right: Path) -> bool:
    comparison = filecmp.dircmp(left, right)
    if comparison.left_only or comparison.right_only or comparison.diff_files or comparison.funny_files:
        return False
    return all(same_tree(left / name, right / name) for name in comparison.common_dirs)


def main() -> None:
    check = "--check" in sys.argv
    if check:
        with tempfile.TemporaryDirectory() as tmp:
            fresh = Path(tmp) / "public"
            build(fresh)
            if not PUBLIC.exists() or not same_tree(fresh, PUBLIC):
                raise SystemExit("public/ is stale. Run python3 src/build.py")
        return
    build(PUBLIC)


if __name__ == "__main__":
    main()
