import json

import yaml

from scripts.build_bundle import build_bundle, build_site


def _write(path, data):
    path.write_text(yaml.safe_dump(data), encoding="utf-8")


def _card(card_id, question="q", answer="a"):
    return dict(id=card_id, category="Mathematics", subtopic="Limits", level=1,
                question=question, answer=answer)


def test_bundle_has_cards_macros_and_graphs(tmp_path):
    data = tmp_path / "data"
    data.mkdir()
    _write(data / "cards.yaml", [
        _card("a", question=r"\includegraphics[width=8cm]{graphs/x.png}"),
        _card("b", answer=r"\includegraphics{graphs/y.png} \includegraphics{graphs/x.png}"),
        _card("c"),
    ])
    _write(data / "katex_macros.yaml", {r"\E": r"\mathbb{E}"})

    bundle = build_bundle(data)

    assert [c["id"] for c in bundle["cards"]] == ["a", "b", "c"]
    assert bundle["cards"][0]["subtopic"] == "Limits"
    assert bundle["macros"] == {r"\E": r"\mathbb{E}"}
    assert bundle["graphs"] == ["graphs/x.png", "graphs/y.png"]


def test_empty_macros_file_gives_empty_dict(tmp_path):
    data = tmp_path / "data"
    data.mkdir()
    _write(data / "cards.yaml", [_card("a")])
    (data / "katex_macros.yaml").write_text("# none\n")

    assert build_bundle(data)["macros"] == {}


def test_build_site_copies_web_graphs_and_writes_bundle(tmp_path):
    data = tmp_path / "data"
    (data / "graphs").mkdir(parents=True)
    (data / "graphs" / "x.png").write_bytes(b"png")
    _write(data / "cards.yaml", [_card("a", question=r"\includegraphics{graphs/x.png}")])
    _write(data / "katex_macros.yaml", {})
    web = tmp_path / "web"
    web.mkdir()
    (web / "index.html").write_text("hi")
    (web / "test").mkdir()
    (web / "test" / "t.test.mjs").write_text("x")
    out = tmp_path / "_site"

    build_site(data, web, out)

    assert (out / "index.html").read_text() == "hi"
    assert not (out / "test").exists()
    assert (out / "graphs" / "x.png").read_bytes() == b"png"
    assert json.loads((out / "cards.json").read_text())["graphs"] == ["graphs/x.png"]


def test_build_site_writes_shell_manifest_of_web_files(tmp_path):
    data = tmp_path / "data"
    data.mkdir()
    _write(data / "cards.yaml", [_card("a")])
    _write(data / "katex_macros.yaml", {})
    web = tmp_path / "web"
    (web / "js").mkdir(parents=True)
    (web / "index.html").write_text("hi")
    (web / "js" / "app.js").write_text("x")
    (web / "package.json").write_text("{}")
    out = tmp_path / "_site"

    build_site(data, web, out)

    shell = json.loads((out / "shell.json").read_text())
    assert shell == ["./", "index.html", "js/app.js"]
    assert not (out / "package.json").exists()
