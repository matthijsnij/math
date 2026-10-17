import test from "node:test";
import assert from "node:assert/strict";
import { layoutLines } from "../js/mathlayout.js";

// Compact view of a layout: "m:" math, "t:" text word, "_" space, "|" break.
const show = (text) => layoutLines(text).map((line) => line.map((c) =>
  c.kind === "math" ? `m:${c.tex}` : c.kind === "text" ? `t:${c.tex}` : c.kind === "space" ? "_" : "|"));

test("top-level \\\\ splits lines; aligned is flattened and & dropped", () => {
  assert.deepEqual(show("\\begin{aligned} a &= b \\\\[4pt] &= c \\end{aligned}"), [["m:a = b"], ["m:= c"]]);
  assert.deepEqual(show("x \\\\ y"), [["m:x"], ["m:y"]]);
});

test("other environments, braces and \\left...\\right stay whole", () => {
  const pmatrix = "A = \\begin{pmatrix} 1 & 2 \\\\ 3 & 4 \\end{pmatrix}";
  assert.deepEqual(show(pmatrix), [[`m:${pmatrix}`]]);
  const cases = "f(x) = \\begin{cases} 0 & x<0 \\\\ 1 & x \\ge 0 \\end{cases}";
  assert.deepEqual(show(cases), [[`m:${cases}`]]);
  assert.deepEqual(show("\\left\\{ \\text{a b} \\right\\}"), [["m:\\left\\{ \\text{a b} \\right\\}"]]);
  // an aligned nested inside another construct is not flattened
  assert.deepEqual(show("\\left. \\begin{aligned} a \\\\ b \\end{aligned} \\right\\}").length, 1);
});

test("top-level \\text becomes words with spaces; touching math is padded with {}", () => {
  assert.deepEqual(show("\\text{Hence } x = 1 \\text{ always.}"),
    [["t:Hence", "_", "m:{}x = 1{}", "_", "t:always."]]);
  assert.deepEqual(show("\\textbf{Note:} y"), [["t:Note:", "m:{}y"]]);
  assert.equal(layoutLines("\\textbf{Note:} y")[0][0].cmd, "textbf");
});

test("spaces inside $...$ and braces in \\text do not split a word", () => {
  assert.deepEqual(show("\\text{if $a = b$ then {x y}}"), [["t:if", "_", "t:$a = b$", "_", "t:then", "_", "t:{x y}"]]);
});

test("\\text as a script, or carrying one, stays math", () => {
  assert.deepEqual(show("x_\\text{max}"), [["m:x_\\text{max}"]]);
  assert.deepEqual(show("\\text{the bias}^2"), [["t:the", "_", "m:{}\\text{bias}^2"]]);
});

test("a single \\text word inside brackets stays math so the bracket cannot break", () => {
  assert.deepEqual(show("E[V \\mid \\text{buy}]"), [["m:E[V \\mid \\text{buy}]"]]);
  assert.deepEqual(show("(\\text{e.g. this}) y"), [["m:({}", "t:e.g.", "_", "t:this", "m:{}) y"]]);
});

test("math may break after top-level commas and \\quad", () => {
  assert.deepEqual(show("1,2"), [["m:1,\\,", "|", "m:2"]]);
  assert.deepEqual(show("a \\quad b"), [["m:a \\quad", "|", "m:b"]]);
  assert.deepEqual(show("x^{1,2}"), [["m:x^{1,2}"]]);
});

test("a trailing control space survives trimming", () => {
  assert.deepEqual(show("\\Rightarrow\\ \\text{done}"), [["m:\\Rightarrow\\ {}", "t:done"]]);
});

test("a row break in mid-sentence joins the previous line", () => {
  assert.deepEqual(show("\\text{the mean} \\\\ \\text{salary.} \\\\ \\text{Next}"),
    [["t:the", "_", "t:mean", "_", "t:salary."], ["t:Next"]]);
  assert.deepEqual(show("\\text{Step 1:} \\\\ \\text{go}"), [["t:Step", "_", "t:1:"], ["t:go"]]);
});

test("an image gets its own line and keeps its comma-separated options", () => {
  const img = "\\includegraphics[width=8cm,height=6cm]{graphs/a.png}";
  assert.deepEqual(show(`\\text{See:}${img}\\text{done.}`), [["t:See:"], [`m:${img}`], ["t:done."]]);
});
