"""Regenerate web/icons/*.png (a ring-and-tail "Q" logo) matching web/icons/icon.svg.

Needs Pillow (not in requirements.txt; only used to regenerate icons):
    pip install pillow && python scripts/gen_icons.py
"""

from pathlib import Path

from PIL import Image, ImageDraw

ICONS = Path(__file__).resolve().parent.parent / "web" / "icons"
BG = (30, 58, 138)
FG = (255, 255, 255)
SCALE = 4  # supersample for smooth edges


def draw(size: int, ring_fraction: float, rounded: bool) -> Image.Image:
    s = size * SCALE
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if rounded:
        d.rounded_rectangle((0, 0, s, s), radius=s * 0.22, fill=BG)
    else:  # maskable: full-bleed background, logo kept inside the safe zone
        d.rectangle((0, 0, s, s), fill=BG)
    c, r = s / 2, s * ring_fraction / 2
    w = s * ring_fraction * 0.16
    d.ellipse((c - r, c - r, c + r, c + r), outline=FG, width=round(w))
    d.line((c + r * 0.25, c + r * 0.25, c + r * 0.95, c + r * 0.95), fill=FG, width=round(w))
    return img.resize((size, size), Image.LANCZOS)


if __name__ == "__main__":
    draw(192, 0.52, True).save(ICONS / "icon-192.png")
    draw(512, 0.52, True).save(ICONS / "icon-512.png")
    draw(512, 0.40, False).save(ICONS / "icon-maskable-512.png")
