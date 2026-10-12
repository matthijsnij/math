# Math Flashcards

Card data and data checks for quant-interview-style math/CS/stats problems as LaTeX
flashcards. See [CONTEXT.md](CONTEXT.md) for domain vocabulary (Card, Category, Subtopic, Level,
Practice mode, Test mode) and [docs/adr/0001-yaml-file-storage-over-sqlite.md](docs/adr/0001-yaml-file-storage-over-sqlite.md)
for the storage rationale.

## Setup

```powershell
python -m venv venv
.\venv\Scripts\pip install -r requirements.txt
```

## Data

Cards are authored by editing `data/cards.yaml` directly (a single git-tracked YAML file, see the ADR above). Card images live in `data/graphs/` and are referenced as `graphs/<file>`. Subtopics
per category live in `data/subtopics.yaml`, seeded from [docs/other/subtopics.md](docs/other/subtopics.md)
and extended automatically when a new subtopic is entered on the Add page. KaTeX custom macros
(e.g. future `\E{}`, `\Var{}`, `\P{}`) live in `data/katex_macros.yaml`, empty by default.

## Tests

```powershell
.\venv\Scripts\python.exe -m pytest
```

Optionally run the JS logic tests with Node (the portable Windows .zip from nodejs.org works,
no admin rights needed):

```powershell
node --test web/test/*.test.mjs
```

## QuantQuest app (PWA)

The phone app lives in `web/` (plain HTML/CSS/ES modules, KaTeX 0.16.11 vendored in
`web/vendor/katex/`, no npm dependencies). On every push to `main`,
[.github/workflows/deploy.yml](.github/workflows/deploy.yml) runs `pytest` and `node --test`,
builds the site with `scripts/build_bundle.py` (app + `cards.json` bundle + referenced graphs)
and deploys it to GitHub Pages at <https://matthijsnij.github.io/math/>. A failing test blocks
the deploy. One-time repo setup: Settings → Pages → Source: **GitHub Actions**.

**Install on Android:** open the URL in Chrome → "Install app" (or ⋮ → Add to home screen).
The first online visit syncs automatically, so the app then works offline.

**Sync:** the Sync button re-downloads the app files, `cards.json` and all graphs into a new
cache, bypassing the HTTP cache. Only if everything succeeds does it replace the old copy and
reload; otherwise the old copy is kept and an error is shown. Cards are only authored in this
repo; the phone is read-only.

**Preview locally:**

```powershell
.env\Scripts\python.exe -m scripts.build_bundle _site
.env\Scripts\python.exe -m http.server 8000 -d _site
```

Then open <http://localhost:8000/>. (`_site/` is git-ignored.) Regenerate the icons with
`scripts/gen_icons.py` (needs Pillow).
