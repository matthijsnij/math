QuantQuest: LaTeX flashcards for quant-interview prep. `data/cards.yaml` is the single source of
truth for Cards (ADR 0001); `web/` is a read-only offline PWA that renders them with vendored
KaTeX. Use the domain vocabulary in `CONTEXT.md` (Card, Category, Subtopic, Level, Sync).

## Cards

Writing or editing a Card: follow `docs/agents/card-writing.md` (one case per Card, answer depth
by Level, macros, formatting, images).

## Rendering

- A Card is not rendered as one KaTeX block. `web/js/mathlayout.js` (pure, unit-tested in
  `web/test/mathlayout.test.mjs`) splits it into top-level rows and `\text` words so it wraps on
  a phone; `web/js/app.js` renders each chunk with `katex.render`. A layout change gets a test
  case there.
- Verify any rendering change in a real browser at phone width (390px), across all Cards, not by
  reading code: build and serve `_site` (README), drive the installed Chrome with Playwright
  (`channel="chrome"`), open Test mode with a count above the Card total and Reveal all, then
  count `.katex-error` elements and `.math-line`s whose `scrollWidth > clientWidth`. Use a fresh
  browser context each run: the service worker is cache-first, so a reused profile shows a
  stale build.

## Environment

Windows. Python runs from `.\venv` (create it per README). Node is not installed: fetch a
portable Node to run `node --test web/test/*.test.mjs`. CI runs pytest and the Node tests on
every push to `main`, then deploys to GitHub Pages; a red test blocks the deploy.

## Agent skills

- **Issue tracker**: GitHub Issues in `matthijsnij/math` via `gh`. See `docs/agents/issue-tracker.md`.
- **Triage labels**: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.
- **Domain docs**: single-context, `CONTEXT.md` + `docs/adr/`. See `docs/agents/domain.md`.
