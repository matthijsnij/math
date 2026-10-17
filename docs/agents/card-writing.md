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

The whole `question`/`answer` string is LaTeX for KaTeX. There is no markdown and no HTML inside
it. To fit a phone screen, the app (`web/js/mathlayout.js`) lays it out instead of rendering one
display block: every top-level `\\` row becomes its own line, top-level `\text{...}` wraps like
normal prose, and math wraps after relations, operators, commas and `\quad`.

- Use `\text{...}` for any narrative words or sentences mixed into the math.
- Use `\begin{aligned} ... \end{aligned}` with `\\` row separators to break a derivation into
  steps; use `\quad`/`\qquad` for spacing instead of literal line breaks. Rows are shown one per
  line, left-aligned (the `&` alignment points are not kept).
- Don't hand-wrap prose with `\\` for width; the text wraps itself. A newline in the YAML is
  not a space: `\text{the}` on one line followed by `\text{mean}` on the next renders "themean".
- Matrices, `cases`, `array` and `\left...\right` groups can't wrap and scroll sideways on a
  narrow screen if wide, so keep them compact.
- In `data/cards.yaml`, prefer YAML block scalars (`question: |` / `answer: |`) over quoted strings for anything with more than a couple of backslashes.
  Double-quoted YAML strings require every backslash to be doubled (`\\\\begin` for `\begin`),
  which gets unreadable fast once `\begin{aligned}` and `\\` row separators are both involved;
  block scalars take the LaTeX as-is.
## Images (function plots, diagrams)

A Card can embed a static image via `\includegraphics[width=8cm]{graphs/<file>}` —
the path is relative to `data/` (the app is served under a sub-path, so absolute paths won't
resolve), and KaTeX's `trust` is scoped to only allow that command with a `graphs/` path. Use this when a case genuinely needs a visual (a function
plot, a geometric figure, a Venn diagram, a probability tree, a Markov chain state diagram, a
payoff diagram) rather than when the content is just as clear written out in LaTeX — most Cards
still don't need one.

- Generate the image (e.g. a small matplotlib/graphviz script) and save it under
  `data/graphs/`, named after the Card's id it belongs to (e.g. `mathematics-functions-and-graphs-4-03.png`)
  so it's obvious which Card it's for and it won't collide with another Card's image.
- Reference it from the `question` or `answer` with `\includegraphics`, same KaTeX block as the
  rest of the Card — don't add markdown or an `<img>` tag, both are unsupported (see above).
- Keep images small/cropped to what the question needs; `width=`/`height=` in the
  `\includegraphics` options controls render size, the file itself should still be reasonably
  sized.
- **Always specify both `width=` and `height=`**, matching the image's real aspect ratio (e.g. a
  5x4in figure needs an 8cm/6.4cm or similar 1.25:1 pair). If `height` is omitted, KaTeX defaults
  it to a tiny `0.9em`, squashing the image to an invisible sliver. Verify the rendered size in a
  real browser (practice session, not just that an `<img>` tag exists) before considering the Card
  done.
## Other practices

- **Category/Subtopic/Level must be valid**: Category from the fixed list in `cardlib/categories.py`,
  Level 1-4. Subtopic can be new text, but check `data/subtopics.yaml` first — reuse an existing
  Subtopic name rather than creating a near-duplicate (e.g. "Eigenvalues" vs "Eigenvalues and
  Eigenvectors").
- **Self-contained answers**: the answer shouldn't assume the reader has another Card or an
  external reference open — restate any fact it depends on in one line rather than citing it.
- **No duplicate ids**: ids follow `category-subtopic-level-NN` and sequential
  (`cardlib/slugs.py` has `slugify`) — pick the next free `NN` by hand when editing `data/cards.yaml`.
- **Batch review before adding**: when proposing several Cards at once, list them for review first
  rather than writing straight into `data/cards.yaml`, so duplicate cases (see above) get caught
  before they're stored. Show only the question of each Card at this stage — the question is what
  determines coverage and duplication, which is all the review is judging. The answer still gets
  written to `data/cards.yaml` and must be correct, it's just not part of what's shown for approval.

## Generating Cards for a Subtopic

Whether a Subtopic has no Cards yet or already has some Levels filled in, generate all its missing
Levels together rather than one Level at a time — a new Level's Cards need to be checked against
every other Level for the same Subtopic to avoid restating a case with different numbers (see "one
case per card" above), which only works if every Level is visible at once.

0. **List what's already there.** Read the existing Cards for the Subtopic (all Levels, not just
   the ones you're about to add) so the outline and the cross-Level dedup check in step 3 both
   have the full picture. If the Subtopic is brand new, this step is empty.
1. **Draft an outline first, not Cards**, covering only the missing Levels. List the distinct
   cases/techniques to cover per Level. The count per Level is not a target to fill — it's
   whatever number of genuinely distinct cases that Level of that specific Subtopic actually
   supports. Derive it by first listing every case/technique/edge case you can think of for that
   Level, then keeping only the ones that are truly distinct (per "one case per card" above), and
   using however many survive — don't pad with near-duplicates to hit a round number, and don't
   cut a genuinely distinct case just to stay low. Keep Level 3 and Level 4 cases
   qualitatively distinct, not just same-content-different-count (see Level definitions in
   `CONTEXT.md`): a Level 3 case is deep theoretical content — a proof, an edge case, a
   derivation — valuable to know but not phrased as an interview prompt, even if the underlying
   fact is one an interviewer could ask about. A Level 4 case is phrased and solved as an actual
   quant-interview application question. When a classic problem (e.g. Monty Hall, a named
   paradox) could fit either, put it at Level 4, not Level 3. Post the outline for approval before
   writing any LaTeX: it's much cheaper to fix scope at this stage than after Cards are drafted.
   Flag any Level 3-4 case that has more than one reasonable solution method here too, so the
   method can be picked before drafting (see "Multiple solution methods" above). Also flag any
   case that needs an image (see "Images" above) so that's agreed before drafting too.
2. **Draft the Cards** for the approved outline, following the depth/formatting/macro rules above.
   For any case flagged as needing an image, generate it now and save it under
   `data/graphs/` before writing the Card's `\includegraphics` reference.
3. **Batch-review the drafted Cards** as a single set, against each other and against the existing
   Cards from step 0, before anything is written to `data/cards.yaml` — this is the pass that
   catches cross-Level duplicates. Show only the question of each Card here (see "Batch review
   before adding" above) — the answer is still written and must be correct, it's just not needed
   to judge coverage/duplication.
4. **Write and validate**: add the approved Cards, then run `tests/test_cards_data.py`
   (`.\venv\Scripts\python.exe -m pytest tests/test_cards_data.py`) to check ids, Category/Level
   validity, and Subtopic registration across the whole file.

Keep the outline in the conversation only — don't save it as a file. Once Cards exist,
`data/cards.yaml` is the record; a separate persisted outline would just be one more thing that
can drift out of sync with it.

Multiple Subtopics can be run through this pipeline back-to-back in one session, but don't merge
two Subtopics' review gates into one — a review batch that's too large is where a duplicate case
or a gap in a derivation slips through unnoticed.
