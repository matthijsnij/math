"""Build the GitHub Pages site: web/ + cards.json bundle + referenced graphs."""

from __future__ import annotations

import json
import re
import shutil
import sys
from dataclasses import asdict
from pathlib import Path

import yaml

from cardlib.storage import CardStore

ROOT = Path(__file__).resolve().parent.parent
GRAPH_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{(graphs/[^}]+)\}")


def build_bundle(data_dir: Path) -> dict:
    data_dir = Path(data_dir)
    cards = CardStore(data_dir / "cards.yaml").load()
    macros = yaml.safe_load((data_dir / "katex_macros.yaml").read_text(encoding="utf-8")) or {}
    graphs = sorted({
        path for card in cards
        for path in GRAPH_RE.findall(card.question + "\n" + card.answer)
    })
    return {"cards": [asdict(card) for card in cards], "macros": macros, "graphs": graphs}


def build_site(data_dir: Path, web_dir: Path, out_dir: Path) -> None:
    data_dir, web_dir, out_dir = Path(data_dir), Path(web_dir), Path(out_dir)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    shutil.copytree(web_dir, out_dir, ignore=shutil.ignore_patterns("test", "package.json"))
    shell = ["./"] + sorted(
        path.relative_to(out_dir).as_posix() for path in out_dir.rglob("*") if path.is_file())
    (out_dir / "shell.json").write_text(json.dumps(shell), encoding="utf-8")
    bundle = build_bundle(data_dir)
    for graph in bundle["graphs"]:
        target = out_dir / graph
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(data_dir / graph, target)
    (out_dir / "cards.json").write_text(
        json.dumps(bundle, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "_site"
    build_site(ROOT / "data", ROOT / "web", out)
