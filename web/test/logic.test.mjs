import test from "node:test";
import assert from "node:assert/strict";
import { filterCards, availableSubtopics } from "../js/filters.js";
import { shuffle, createPractice, selectTest } from "../js/session.js";
import { performSync } from "../js/sync.js";

const card = (id, category, subtopic, level) => ({ id, category, subtopic, level, question: "q", answer: "a" });
const cards = [
  card("1", "Mathematics", "Limits", 1),
  card("2", "Mathematics", "Integrals", 2),
  card("3", "Computer Science", "Sorting", 1),
  card("4", "Computer Science", "Limits", 4),
  card("5", "Brainteasers", "Zebra", 3),
];
const ids = (list) => list.map((c) => c.id);
// deterministic rng
const seeded = (seed = 1) => () => ((seed = (seed * 16807) % 2147483647) - 1) / 2147483646;

test("no filters means no restriction", () => {
  assert.deepEqual(ids(filterCards(cards, {})), ["1", "2", "3", "4", "5"]);
  assert.deepEqual(ids(filterCards(cards, { categories: [], subtopics: [], levels: [] })), ["1", "2", "3", "4", "5"]);
});

test("OR within a filter, AND across filters", () => {
  assert.deepEqual(ids(filterCards(cards, { categories: ["Mathematics", "Brainteasers"] })), ["1", "2", "5"]);
  assert.deepEqual(ids(filterCards(cards, { categories: ["Mathematics", "Computer Science"], levels: [1, 4] })), ["1", "3", "4"]);
  assert.deepEqual(ids(filterCards(cards, { categories: ["Computer Science"], subtopics: ["Limits"], levels: [4] })), ["4"]);
  assert.deepEqual(ids(filterCards(cards, { categories: ["Brainteasers"], subtopics: ["Limits"] })), []);
});

test("subtopics narrow to ticked categories, sorted, deduped", () => {
  assert.deepEqual(availableSubtopics(cards, []), ["Integrals", "Limits", "Sorting", "Zebra"]);
  assert.deepEqual(availableSubtopics(cards, ["Computer Science"]), ["Limits", "Sorting"]);
  assert.deepEqual(availableSubtopics(cards, ["Mathematics", "Brainteasers"]), ["Integrals", "Limits", "Zebra"]);
});

test("shuffle keeps all items and does not mutate input", () => {
  const input = [1, 2, 3, 4, 5];
  const out = shuffle(input, seeded());
  assert.deepEqual([...out].sort(), input);
  assert.deepEqual(input, [1, 2, 3, 4, 5]);
});

test("practice shows every card once per cycle, then reshuffles and continues", () => {
  const practice = createPractice(cards, seeded(7));
  for (let cycle = 0; cycle < 3; cycle++) {
    const seen = Array.from({ length: cards.length }, () => practice.next().id);
    assert.deepEqual(seen.sort(), ["1", "2", "3", "4", "5"]);
  }
});

test("practice over an empty set", () => {
  const practice = createPractice([]);
  assert.equal(practice.isEmpty, true);
  assert.equal(practice.next(), null);
});

test("test picks N distinct cards without a notice", () => {
  const { cards: picked, notice } = selectTest(cards, 3, seeded(3));
  assert.equal(picked.length, 3);
  assert.equal(new Set(ids(picked)).size, 3);
  assert.equal(notice, null);
});

test("test with fewer matches uses all and shows the notice", () => {
  const { cards: picked, notice } = selectTest(cards, 10);
  assert.equal(picked.length, 5);
  assert.equal(notice, "Only 5 cards matched the filters; running the test on all of them.");
  assert.equal(selectTest(cards.slice(0, 1), 10).notice, "Only 1 card matched the filters; running the test on all of them.");
});

test("test count is at least 1", () => {
  assert.equal(selectTest(cards, 0).cards.length, 1);
  assert.equal(selectTest(cards, "abc").cards.length, 1);
});

// --- Sync ---
const res = (body, ok = true) => ({ ok, json: async () => body, clone() { return this; } });
function harness(files) {
  const staged = [];
  const log = [];
  const store = {
    stage: async (url) => { staged.push(url); },
    commit: async (meta) => { log.push(["commit", meta]); },
    discard: async () => { log.push(["discard"]); },
  };
  const fetchFn = async (url) => {
    if (!(url in files)) return res(null, false);
    const v = files[url];
    if (v instanceof Error) throw v;
    return res(v);
  };
  return { staged, log, store, fetchFn };
}
const good = () => ({
  "cards.json": { cards: [{ id: "1" }], macros: {}, graphs: ["graphs/a.png"] },
  "shell.json": ["./", "index.html"],
  "./": "x", "index.html": "x", "graphs/a.png": "x",
});
const fixedNow = () => new Date("2026-01-02T03:04:05Z");

test("sync commits only after every file is fetched and staged", async () => {
  const h = harness(good());
  const result = await performSync({ fetchFn: h.fetchFn, store: h.store, now: fixedNow });
  assert.equal(result.ok, true);
  assert.deepEqual(h.staged, ["cards.json", "shell.json", "./", "index.html", "graphs/a.png"]);
  assert.deepEqual(h.log, [["commit", { syncedAt: "2026-01-02T03:04:05.000Z", count: 1 }]]);
});

test("sync discards when a graph fetch fails", async () => {
  const files = good();
  delete files["graphs/a.png"];
  const h = harness(files);
  const result = await performSync({ fetchFn: h.fetchFn, store: h.store });
  assert.equal(result.ok, false);
  assert.deepEqual(h.log, [["discard"]]);
});

test("sync discards when offline (fetch throws)", async () => {
  const files = good();
  files["cards.json"] = new Error("offline");
  const h = harness(files);
  const result = await performSync({ fetchFn: h.fetchFn, store: h.store });
  assert.equal(result.ok, false);
  assert.deepEqual(h.log, [["discard"]]);
});

test("sync discards when cards.json does not parse into a bundle", async () => {
  const files = good();
  files["cards.json"] = { nope: true };
  const h = harness(files);
  const result = await performSync({ fetchFn: h.fetchFn, store: h.store });
  assert.equal(result.ok, false);
  assert.deepEqual(h.log, [["discard"]]);
});

test("sync discards when staging fails", async () => {
  const h = harness(good());
  h.store.stage = async (url) => { if (url === "index.html") throw new Error("quota"); };
  const result = await performSync({ fetchFn: h.fetchFn, store: h.store });
  assert.equal(result.ok, false);
  assert.deepEqual(h.log, [["discard"]]);
});
