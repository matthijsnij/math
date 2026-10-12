"""Card id slugs: category-subtopic-level-NN (see docs/agents/domain.md / CONTEXT.md)."""

from __future__ import annotations

import re


def slugify(text: str) -> str:
    slug = text.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")
