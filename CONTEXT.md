# Math Flashcards

A local web app for practicing quant-interview-style math/CS/stats problems as LaTeX flashcards, separate from the standalone scripts in `other_tools/`.

## Language

**Card**:
A single question/answer pair, written in LaTeX, tagged with one Category, one Subtopic, and one Level.
_Avoid_: Question, flashcard (when referring to the stored record — "flashcard" is fine for the UI concept of flipping front/back)

**Category**:
One of 6 fixed top-level subjects: Mathematics, Computer Science, Probability & Statistics, Machine Learning, Economics & Finance, Brainteasers.
_Avoid_: Topic (too vague — "topic" gets used loosely for category+subtopic together in casual conversation, but the stored field is Category)

**Subtopic**:
A named grouping within a Category (e.g. "Linear Algebra" under Mathematics). Mostly a fixed list supplied up front, but extensible: adding a Card can introduce a new Subtopic via free text.
_Avoid_: Sub-category

**Level**:
A difficulty tier from 1-3 within a Subtopic. Level 1 is basic definitions/standard questions. Level 2 is applied theory and intermediate relations/properties. Levels 1-2 together form the theoretical base. Level 3 is a quant-interview-style application problem — the most important tier.
_Avoid_: Difficulty, tier

**Practice mode**:
An unlimited-length session over a filtered set of Cards (by Category/Subtopic/Level), shown in shuffled order, self-graded by flipping each card. Reshuffles and cycles back to the start once the filtered set is exhausted.

**Test mode**:
A fixed-length (N Cards) session over a filtered set of Cards, answered blind — no answers are shown until all N have been gone through, at which point every Q&A pair in that test is revealed together for review.

**Sync** _(v2)_:
A manual action, triggered from the phone, that fetches the latest Card data from this GitHub repo (via the GitHub API) into the phone's local offline copy. Distinct from git's own sync/pull — this is an in-app action for a non-git client.
