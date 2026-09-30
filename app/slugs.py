"""Card id slugs: category-subtopic-level-NN (see docs/agents/domain.md / CONTEXT.md)."""

from __future__ import annotations

import re


def slugify(text: str) -> str:
    slug = text.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def next_card_id(existing_ids: list[str], category: str, subtopic: str, level: int) -> str:
    prefix = f"{slugify(category)}-{slugify(subtopic)}-{level}-"
    used = []
    for card_id in existing_ids:
        if card_id.startswith(prefix):
            suffix = card_id[len(prefix):]
            if suffix.isdigit():
                used.append(int(suffix))
    next_num = max(used, default=0) + 1
    return f"{prefix}{next_num:02d}"
