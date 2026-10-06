# nihito Rechtstexte

Legal texts of the nihito planner (German), published at https://nihito-io.github.io/legal/.

| Id | Dokument | Datei |
|---|---|---|
| `terms` | Nutzungsbedingungen | [nutzungsbedingungen.md](./nutzungsbedingungen.md) |
| `privacy` | Datenschutzerklärung (with cookies, `#cookies`) | [datenschutzerklaerung.md](./datenschutzerklaerung.md) |
| `dpa` | Auftragsverarbeitungsvertrag (AVV), Anhang der Nutzungsbedingungen | [avv.md](./avv.md) |

History: [CHANGELOG.md](./CHANGELOG.md).

## Published URLs

| URL | Content |
|---|---|
| `https://nihito-io.github.io/legal/<version>/<id>.html` and `.pdf` | One version; never changes |
| `https://nihito-io.github.io/legal/latest/<id>.html` and `.pdf` | Copy of the newest version |
| `https://nihito-io.github.io/legal/versions.json` | `{"latest", "versions": [{"version", "effective", "documents": {"<id>": {"title", "html", "pdf"}}}]}`, newest first |
| `https://nihito-io.github.io/legal/` | Readable index of all versions |

## Rechtstexte veröffentlichen

A release is a git tag `legal-YYYY-MM-DD` (publication date; a second release on the same day gets the suffix `b`). One tag versions all documents together, and the tag name is the `TERMS_VERSION` that planner-platform stores when a user accepts the terms. Every tagged version stays online unchanged.

1. **Edit** the documents on a branch. Set `version` in the front-matter of **all** documents to the new tag and `effective` to the date the version takes effect. Add an entry to [CHANGELOG.md](./CHANGELOG.md).
2. **Open a PR.** The workflow builds the working tree into the artifact `rechtstexte-preview` (HTML and PDF). It warns about any `TODO` left in the texts.
3. **Legal review** of the preview. Merge the PR once approved.
4. **Tag** the merge commit on `main` and push the tag:
   ```sh
   git tag legal-2026-10-19
   git push origin legal-2026-10-19
   ```
   The workflow then builds every `legal-*` tag and deploys the site. It fails if a document's `version` differs from its tag, if a document still contains `TODO`, or if the documents of one tag have different `effective` dates.
5. **Check the URLs** above: the new version, `latest/` and `versions.json`.
6. **Set `TERMS_VERSION`** in planner-platform to the new tag and deploy it. From then on, users must accept the new version before they can keep using the planner.

Links between the documents are relative (`[AVV](dpa.html)`), so they always point to the same version: in HTML to the sibling file, in the PDF to `https://nihito-io.github.io/legal/<version>/<id>.html`.

Never move or delete a `legal-*` tag once a user may have accepted it, and don't rename the documents: each release rebuilds all tags, and the file-to-id mapping lives in `LEGAL_DOCUMENTS` in [.github/workflows/publish.yml](./.github/workflows/publish.yml). To redeploy without a new tag, run the workflow manually.

GitHub settings this relies on: Settings → Pages → Source "GitHub Actions"; Settings → Environments → `github-pages` allows tags `legal-*`.

## Building locally

Needs pandoc, xelatex with German language support (`texlive-lang-german`) and the Teachers font.

```sh
export LEGAL_DOCUMENTS="terms=nutzungsbedingungen.md,privacy=datenschutzerklaerung.md,dpa=avv.md"
python3 tools/build.py preview --out preview   # working tree
python3 tools/build.py release --out site      # all legal-* tags
```

The logo exists twice: `img/nihito-logo.pdf` for the PDFs (XeLaTeX cannot embed SVG) and `img/nihito-logo.svg` for the HTML pages.
