"""Builds the legal documents (Nutzungsbedingungen, Datenschutzerklärung, AVV) into HTML and PDF.

Modes:
  preview  Builds the working tree into <out>/<id>.{html,pdf}. Used on branches and PRs.
  release  Builds every `legal-*` tag into <out>/<version>/<id>.{html,pdf}, copies the
           newest one to <out>/latest/ and writes <out>/versions.json and <out>/index.html.

The documents are listed in the LEGAL_DOCUMENTS environment variable as
"id=path,id=path,..." (set in .github/workflows/publish.yml). File paths must stay
stable: every tag is built again on each release.

Each document starts with YAML front-matter: title, version (equal to the tag) and
effective (YYYY-MM-DD). Requires pandoc and xelatex.
"""

import argparse
import base64
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ASSETS = Path(__file__).resolve().parent
LOGO_PDF = REPO / "img" / "nihito-logo.pdf"  # XeLaTeX cannot embed SVG
LOGO_SVG = REPO / "img" / "nihito-logo.svg"
BASE_URL = os.environ.get(
    "LEGAL_BASE_URL", "https://nihito-io.github.io/legal/"
).rstrip("/") + "/"
TAG_PATTERN = re.compile(r"^legal-\d{4}-\d{2}-\d{2}[b-z]?$")


def fail(message: str) -> None:
    print(f"::error::{message}", file=sys.stderr)
    sys.exit(1)


def documents() -> dict[str, str]:
    raw = os.environ.get("LEGAL_DOCUMENTS", "").strip()
    if not raw:
        fail("LEGAL_DOCUMENTS is not set (expected 'id=path,id=path,...').")
    docs = {}
    for entry in raw.split(","):
        doc_id, _, path = entry.strip().partition("=")
        if not doc_id or not path:
            fail(f"Invalid LEGAL_DOCUMENTS entry: '{entry}'.")
        docs[doc_id.strip()] = path.strip()
    return docs


def run(*args: str, cwd: Path | None = None, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        args, cwd=cwd, capture_output=True, text=True, encoding="utf-8",
        env={**os.environ, **env} if env else None,
    )
    if result.returncode != 0:
        fail(f"{' '.join(args)} failed:\n{result.stderr}")
    return result.stdout


def read_meta(source: Path, tmp: Path) -> dict:
    template = tmp / "meta.tpl"
    template.write_text("$meta-json$", encoding="utf-8")
    meta = json.loads(run("pandoc", str(source), "-t", "plain", "--template", str(template)))
    for key in ("title", "version", "effective"):
        if not isinstance(meta.get(key), str) or not meta[key].strip():
            fail(f"{source}: front-matter '{key}' is missing.")
    try:
        meta["effective_date"] = date.fromisoformat(meta["effective"])
    except ValueError:
        fail(f"{source}: front-matter 'effective' must be YYYY-MM-DD, got '{meta['effective']}'.")
    return meta


def logo_html() -> str:
    """The logo as an inline data URI, so every HTML page is self-contained."""
    data = base64.b64encode(LOGO_SVG.read_bytes()).decode("ascii")
    return f'<div class="logo"><img src="data:image/svg+xml;base64,{data}" alt="nihito"></div>\n'


def build_document(source: Path, out_dir: Path, doc_id: str, meta: dict, footer: str, tmp: Path) -> None:
    effective = meta["effective_date"].strftime("%d.%m.%Y")
    subtitle = f"Version {meta['version']} · gültig ab {effective}"
    common = [str(source), "--metadata", "lang=de-CH", "--metadata", f"subtitle={subtitle}"]

    before_body = tmp / "logo.html"
    before_body.write_text(logo_html(), encoding="utf-8")
    after_body = tmp / f"{doc_id}-after.html"
    after_body.write_text(
        f'<p class="pdf-link"><a href="{doc_id}.pdf">Als PDF herunterladen</a></p>\n',
        encoding="utf-8",
    )
    run(
        "pandoc", *common,
        "--standalone",
        "--to", "html5",
        "--include-in-header", str(ASSETS / "style.html"),
        "--include-before-body", str(before_body),
        "--include-after-body", str(after_body),
        "--output", str(out_dir / f"{doc_id}.html"),
    )

    header = tmp / f"{doc_id}-header.tex"
    header.write_text(
        (ASSETS / "header.tex").read_text(encoding="utf-8")
        .replace("@LOGO@", LOGO_PDF.as_posix())
        .replace("@FOOTER@", footer),
        encoding="utf-8",
    )
    run(
        "pandoc", *common,
        "--pdf-engine", "xelatex",
        "--variable", "geometry:a4paper",
        "--variable", "geometry:margin=1in",
        "--variable", "fontsize=10pt",
        "--variable", "documentclass=article",
        "--variable", "mainfont=Teachers",
        "--variable", "colorlinks=true",
        "--include-in-header", str(header),
        "--lua-filter", str(ASSETS / "pdf-links.lua"),
        "--output", str(out_dir / f"{doc_id}.pdf"),
        cwd=tmp,
        env={"LEGAL_LINK_BASE": f"{BASE_URL}{meta['version']}/"},
    )


def build_tree(root: Path, out_dir: Path, expected_version: str | None, footer_label: str, tmp: Path) -> dict:
    """Builds all documents found under root. Returns {id: meta}."""
    out_dir.mkdir(parents=True, exist_ok=True)
    built = {}
    for doc_id, path in documents().items():
        source = root / path
        if not source.exists():
            if expected_version:
                print(f"::warning::{expected_version} has no {path}; '{doc_id}' is skipped for this version.")
                continue
            fail(f"{path} does not exist.")
        meta = read_meta(source, tmp)
        if expected_version:
            if meta["version"] != expected_version:
                fail(f"{path} in {expected_version}: front-matter version is '{meta['version']}', expected '{expected_version}'.")
            if "TODO" in source.read_text(encoding="utf-8"):
                fail(f"{path} in {expected_version} still contains a TODO.")
        else:
            if not TAG_PATTERN.match(meta["version"]):
                fail(f"{path}: front-matter version '{meta['version']}' is not of the form legal-YYYY-MM-DD.")
            if "TODO" in source.read_text(encoding="utf-8"):
                print(f"::warning file={path}::{path} contains a TODO; a release build will fail.")
        build_document(source, out_dir, doc_id, meta, f"{footer_label} | gültig ab {meta['effective_date']:%d.%m.%Y}", tmp)
        built[doc_id] = meta
        print(f"Built {doc_id} ({path}) -> {out_dir}")
    if not built:
        fail(f"No documents found in {root}.")
    return built


def legal_tags() -> list[str]:
    tags = run("git", "tag", "--list", "legal-*", cwd=REPO).split()
    invalid = [t for t in tags if not TAG_PATTERN.match(t)]
    if invalid:
        fail(f"Tags not of the form legal-YYYY-MM-DD[b]: {', '.join(invalid)}")
    # Plain string order is chronological: legal-2026-10-19 < legal-2026-10-19b < legal-2026-10-20.
    return sorted(tags)


def write_index(out: Path, versions: list[dict]) -> None:
    latest = versions[0]

    def links(version: str, docs: dict) -> str:
        return "".join(
            f'<li>{html.escape(d["title"])}: '
            f'<a href="{version}/{doc_id}.html">HTML</a> · <a href="{version}/{doc_id}.pdf">PDF</a></li>'
            for doc_id, d in docs.items()
        )

    rows = "".join(
        f'<tr><td>{html.escape(v["version"])}</td><td>{date.fromisoformat(v["effective"]):%d.%m.%Y}</td>'
        f'<td><ul>{links(v["version"], v["documents"])}</ul></td></tr>'
        for v in versions
    )
    style = (ASSETS / "style.html").read_text(encoding="utf-8")
    (out / "index.html").write_text(
        f"""<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>nihito planner – Rechtstexte</title>
{style}
</head>
<body>
{logo_html()}<h1>nihito planner – Rechtstexte</h1>
<h2>Aktuelle Fassung ({html.escape(latest["version"])})</h2>
<ul>{links("latest", latest["documents"])}</ul>
<h2>Alle Fassungen</h2>
<table>
<thead><tr><th>Version</th><th>Gültig ab</th><th>Dokumente</th></tr></thead>
<tbody>{rows}</tbody>
</table>
<p><a href="versions.json">versions.json</a></p>
</body>
</html>
""",
        encoding="utf-8",
    )


def release(out: Path, tmp: Path) -> None:
    tags = legal_tags()
    if not tags:
        fail("There is no legal-* tag yet; nothing to publish.")
    versions = []
    for tag in tags:
        worktree = tmp / "worktrees" / tag
        run("git", "worktree", "add", "--detach", str(worktree), tag, cwd=REPO)
        try:
            built = build_tree(worktree, out / tag, tag, f"Version {tag}", tmp)
        finally:
            run("git", "worktree", "remove", "--force", str(worktree), cwd=REPO)
        effective = {meta["effective"] for meta in built.values()}
        if len(effective) != 1:
            fail(f"{tag}: documents have different effective dates: {', '.join(sorted(effective))}.")
        versions.append({
            "version": tag,
            "effective": effective.pop(),
            "documents": {
                doc_id: {
                    "title": meta["title"],
                    "html": f"{BASE_URL}{tag}/{doc_id}.html",
                    "pdf": f"{BASE_URL}{tag}/{doc_id}.pdf",
                }
                for doc_id, meta in built.items()
            },
        })

    versions.reverse()  # newest first
    shutil.copytree(out / versions[0]["version"], out / "latest")
    (out / "versions.json").write_text(
        json.dumps({"latest": versions[0]["version"], "versions": versions}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_index(out, versions)
    print(f"Published {len(versions)} version(s); latest is {versions[0]['version']}.")


def preview(out: Path, tmp: Path) -> None:
    sha = run("git", "rev-parse", "--short", "HEAD", cwd=REPO).strip()
    build_tree(REPO, out, None, f"Entwurf ({sha})", tmp)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=["preview", "release"])
    parser.add_argument("--out", type=Path, required=True, help="output directory (must not exist)")
    args = parser.parse_args()

    out = args.out.resolve()
    if out.exists():
        fail(f"{out} already exists.")
    with tempfile.TemporaryDirectory() as tmp:
        (preview if args.mode == "preview" else release)(out, Path(tmp))


if __name__ == "__main__":
    main()
