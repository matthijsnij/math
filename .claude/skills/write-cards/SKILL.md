---
name: write-cards
description: "Generate Cards for a Subtopic, following the repo's card-writing workflow."
disable-model-invocation: true
argument-hint: "Subtopic name (e.g. \"Exponents and Logarithms\"), optionally with a Category"
---

Run the generation workflow in [`docs/agents/card-writing.md`](../../../docs/agents/card-writing.md)
("Generating Cards for a Subtopic") for the Subtopic named in the argument.

If the Category isn't given, look it up in `data/subtopics.yaml`.
