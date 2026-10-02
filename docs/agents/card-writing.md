# Card writing guidelines

How to author Card question/answer pairs for `data/cards.yaml`. See `CONTEXT.md` for the
Card/Category/Subtopic/Level vocabulary used below.

## One case per card

A Card covers exactly one specific case or technique. Don't create near-duplicate Cards that are
the same question with different numbers plugged in — if two Cards would be solved by the same
sequence of steps with different inputs, they're one Card, not two.

Before adding a Card, check: does it exercise a case/technique/edge case not already covered by an
existing Card in that Subtopic+Level? If the only difference from an existing Card is the numbers,
don't add it.

This also applies across a Subtopic's progression: a Level 2 Card shouldn't just be the Level 1
Card's formula restated with different numbers — it should apply the concept in a genuinely
different way (see Level definitions in `CONTEXT.md`).

## Answer depth

- **Level 1-2**: straightforward. A complete but concise derivation, with explanations only when really necessary.
- **Level 3-4**: a complete but concise derivation. Show every reasoning step needed to follow the
  logic from question to answer, with no gaps a reader would have to fill in themselves. Cut
  anything that isn't necessary to that specific derivation (no general background, no restating
  the theory the question is testing).
- **Multiple solution methods**: when a Level 3-4 problem has more than one reasonable method,
  don't pick one unilaterally. Present the candidate methods first and let the method be chosen
  before writing the final answer. Only the chosen method goes into the stored answer — don't
  include the rejected methods "for completeness."

## LaTeX macros

Use the macros defined in `data/katex_macros.yaml` in both question and answer instead of spelling out the longhand
(`\mathbb{E}`, `\operatorname{Var}`, etc.) wherever the notation applies.

If a Card introduces notation that will recur across other Cards (e.g. a correlation operator, a
new set), add it to `data/katex_macros.yaml` rather than writing it out longhand inline, so later
Cards can reuse it. Don't add a macro for a one-off that won't recur.

## Formatting constraints

The whole `question`/`answer` string is rendered as a single KaTeX display-math block (wrapped in
`\[ ... \]` — see `app/templates/practice_session.html`). There is no markdown and no HTML inside
it:

- Use `\text{...}` for any narrative words or sentences mixed into the math.
- Use `\begin{aligned} ... \end{aligned}` with `\\` row separators to break a derivation into
  steps; use `\quad`/`\qquad` for spacing instead of literal line breaks.
- In `data/cards.yaml`, prefer YAML block scalars (`question: |` / `answer: |`, as the Add page's
  placeholder shows) over quoted strings for anything with more than a couple of backslashes.
  Double-quoted YAML strings require every backslash to be doubled (`\\\\begin` for `\begin`),
  which gets unreadable fast once `\begin{aligned}` and `\\` row separators are both involved;
  block scalars take the LaTeX as-is.

## Other practices

- **Category/Subtopic/Level must be valid**: Category from the fixed list in `app/categories.py`,
  Level 1-4. Subtopic can be new text, but check `data/subtopics.yaml` first — reuse an existing
  Subtopic name rather than creating a near-duplicate (e.g. "Eigenvalues" vs "Eigenvalues and
  Eigenvectors").
- **Self-contained answers**: the answer shouldn't assume the reader has another Card or an
  external reference open — restate any fact it depends on in one line rather than citing it.
- **No duplicate ids**: ids follow `category-subtopic-level-NN` and auto-increment
  (`app/slugs.py`) — only relevant if hand-editing `data/cards.yaml` instead of using the Add page.
- **Batch review before adding**: when proposing several Cards at once, list them for review first
  rather than writing straight into `data/cards.yaml`, so duplicate cases (see above) get caught
  before they're stored.
