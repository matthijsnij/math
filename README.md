# Math Flashcards

A local Flask web app for practicing quant-interview-style math/CS/stats problems as LaTeX
flashcards. See [CONTEXT.md](CONTEXT.md) for domain vocabulary (Card, Category, Subtopic, Level,
Practice mode, Test mode) and [docs/adr/0001-yaml-file-storage-over-sqlite.md](docs/adr/0001-yaml-file-storage-over-sqlite.md)
for the storage rationale.

## Setup

```powershell
python -m venv venv
.\venv\Scripts\pip install -r requirements.txt
```

## Running

```powershell
.\venv\Scripts\python.exe run.py
```

The app serves on port 5000. It has no authentication and is not intended to be exposed to the
internet.

### Reaching it from a phone

Run it on a laptop connected to the same local network as your phone (e.g. the phone's own
mobile hotspot, tethering the laptop — no home Wi-Fi required). Find the laptop's LAN IP
(`ipconfig` on Windows, look for the IPv4 address on the hotspot's adapter), then browse to
`http://<that-ip>:5000` from the phone. The math is rendered client-side via
[KaTeX](https://katex.org/) loaded from a CDN, so the phone's browser needs a route to the
internet the first time it loads a page (offline/away-from-network phone use is out of scope for
this version — see the v2 issue).

## Data

Cards live in `data/cards.yaml`, a single git-tracked YAML file (see the ADR above). Subtopics
per category live in `data/subtopics.yaml`, seeded from [docs/other/subtopics.md](docs/other/subtopics.md)
and extended automatically when a new subtopic is entered on the Add page. KaTeX custom macros
(e.g. future `\E{}`, `\Var{}`, `\P{}`) live in `data/katex_macros.yaml`, empty by default.

## Tests

```powershell
.\venv\Scripts\python.exe -m pytest
```