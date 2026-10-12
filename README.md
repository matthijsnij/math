# Math Flashcards

Card data and data checks for quant-interview-style math/CS/stats problems as LaTeX
flashcards. (A phone PWA is planned; see the issue tracker.) See [CONTEXT.md](CONTEXT.md) for domain vocabulary (Card, Category, Subtopic, Level,
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