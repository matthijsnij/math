import { filterCards, availableSubtopics } from "./filters.js";
import { createPractice, selectTest } from "./session.js";
import { performSync } from "./sync.js";
import { createStagingStore, fetchNoStore, readActiveMeta } from "./cachestore.js";

const CATEGORIES = [
  "Mathematics",
  "Computer Science",
  "Probability & Statistics",
  "Machine Learning",
  "Economics & Finance",
  "Brainteasers",
];
const LEVELS = [1, 2, 3, 4];

const root = document.getElementById("app");
let bundle = null; // { cards, macros, graphs } from the active cache, or null before first Sync
let meta = null; // { syncedAt, count }

// ---- helpers -------------------------------------------------------------

function h(tag, props = {}, ...children) {
  const el = document.createElement(tag);
  for (const [key, value] of Object.entries(props)) {
    if (key === "class") el.className = value;
    else if (key.startsWith("on")) el.addEventListener(key.slice(2), value);
    else el.setAttribute(key, value);
  }
  el.append(...children.flat().filter((c) => c != null));
  return el;
}

function render(...nodes) {
  root.replaceChildren(...nodes);
  window.scrollTo(0, 0);
}

const fmtDate = (iso) => new Date(iso).toLocaleString();

// Split a card string into display lines. `aligned` environments are flattened (alignment `&`
// dropped) and every top-level `\` starts a new line, so each line is plain inline math that
// can wrap to the card width instead of sitting in an unbreakable table.
function mathLines(text) {
  const flat = text.replace(/\\begin\{aligned\}|\\end\{aligned\}/g, "\\\\");
  const lines = [];
  let cur = "";
  let depth = 0;
  for (let i = 0; i < flat.length; i++) {
    const c = flat[i];
    if (c === "\\") {
      const n = flat[i + 1];
      if (n === "\\" && depth === 0) {
        lines.push(cur);
        cur = "";
        i++;
        // drop an optional vertical-spacing argument such as \[4pt]
        const m = /^\[[^\]]*\]/.exec(flat.slice(i + 1));
        if (m) i += m[0].length;
      } else {
        cur += c + (n ?? "");
        i++;
      }
      continue;
    }
    if (c === "{") depth++;
    else if (c === "}") depth--;
    if (c === "&" && depth === 0) continue;
    cur += c;
  }
  lines.push(cur);
  return lines.map((l) => l.trim()).filter(Boolean);
}

function renderMath(el, text) {
  // Inline (not display) math so long lines can wrap; \displaystyle keeps display-size fractions.
  const lines = mathLines(text).map((l) => h("div", { class: "math-line" }, `\\(\\displaystyle ${l}\\)`));
  el.replaceChildren(...lines);
  renderMathInElement(el, {
    delimiters: [{ left: "\\(", right: "\\)", display: false }],
    macros: { ...(bundle?.macros ?? {}) }, // KaTeX mutates this object, so pass a copy
    trust: (ctx) => ctx.command === "\\includegraphics" && ctx.url.startsWith("graphs/"),
    throwOnError: false,
  });
}

function mathBlock(label, text) {
  const body = h("div");
  renderMath(body, text);
  return h("div", { class: "card" }, h("div", { class: "label" }, label), body);
}

// ---- data / sync ---------------------------------------------------------

async function loadLocal() {
  meta = await readActiveMeta();
  bundle = null;
  if (!meta) return;
  try {
    const res = await fetch("cards.json");
    bundle = await res.json();
  } catch {
    bundle = null;
  }
}

async function sync() {
  const result = await performSync({ fetchFn: fetchNoStore, store: createStagingStore() });
  if (result.ok) {
    try {
      await navigator.storage?.persist?.();
    } catch {
      // best effort
    }
    const registration = await navigator.serviceWorker?.getRegistration();
    await registration?.update().catch(() => {});
    location.reload();
    return null;
  }
  console.error("Sync failed:", result.error);
  return meta
    ? `Sync failed — still using cards from ${fmtDate(meta.syncedAt)}`
    : "Sync failed — no cards on this device yet. Connect to the internet and try again.";
}

// ---- screens -------------------------------------------------------------

function syncButton(errorBox) {
  const button = h("button", { class: "btn secondary", type: "button" }, "Sync");
  button.addEventListener("click", async () => {
    button.disabled = true;
    button.textContent = "Syncing…";
    errorBox.textContent = "";
    const error = await sync();
    if (error) {
      errorBox.textContent = error;
      button.disabled = false;
      button.textContent = "Sync";
    }
  });
  return button;
}

function homeScreen(initialError = "") {
  const error = h("p", { class: "error" }, initialError);
  const syncBtn = syncButton(error);
  if (!bundle) {
    render(h("div", { class: "stack empty" },
      h("p", {}, "No cards on this device yet."),
      h("p", { class: "muted" }, "Press Sync while online to download them."),
      syncBtn, error));
    return;
  }
  render(h("div", { class: "stack" },
    h("p", { class: "muted" }, `${bundle.cards.length} cards · last synced ${fmtDate(meta.syncedAt)}`),
    h("button", { class: "btn", type: "button", onclick: () => setupScreen("practice") }, "Practice"),
    h("button", { class: "btn", type: "button", onclick: () => setupScreen("test") }, "Test"),
    syncBtn, error));
}

function checkboxGroup(legend, name, options) {
  return h("fieldset", {}, h("legend", {}, legend),
    h("div", { class: "chips" }, options.map(({ value, text }) =>
      h("label", {}, h("input", { type: "checkbox", name, value: String(value) }), text))));
}

const ticked = (container, name) =>
  [...container.querySelectorAll(`input[name="${name}"]:checked`)].map((i) => i.value);

function setupScreen(mode) {
  const categoryGroup = h("div");
  const subtopicGroup = h("div");
  const levelGroup = checkboxGroup("Level", "level", LEVELS.map((l) => ({ value: l, text: String(l) })));
  const form = h("div", { class: "stack" });

  const renderSubtopics = () => {
    const keep = new Set(ticked(subtopicGroup, "subtopic"));
    const options = availableSubtopics(bundle.cards, ticked(categoryGroup, "category"));
    subtopicGroup.replaceChildren(checkboxGroup("Subtopic", "subtopic",
      options.map((s) => ({ value: s, text: s }))));
    subtopicGroup.querySelectorAll("input").forEach((i) => { i.checked = keep.has(i.value); });
  };
  categoryGroup.append(checkboxGroup("Category", "category", CATEGORIES.map((c) => ({ value: c, text: c }))));
  categoryGroup.addEventListener("change", renderSubtopics);
  renderSubtopics();

  const count = h("input", { type: "number", min: "1", value: "10", id: "count" });
  const countRow = mode === "test"
    ? h("label", {}, "Number of cards ", count)
    : null;

  const start = () => {
    const categories = ticked(categoryGroup, "category");
    // A Subtopic ticked earlier may be hidden after narrowing; only honour visible ones.
    const visible = new Set(availableSubtopics(bundle.cards, categories));
    const subtopics = ticked(subtopicGroup, "subtopic").filter((s) => visible.has(s));
    const levels = ticked(levelGroup, "level").map(Number);
    const cards = filterCards(bundle.cards, { categories, subtopics, levels });
    if (mode === "practice") practiceScreen(cards);
    else testScreen(cards, count.value);
  };

  form.append(
    h("h2", {}, mode === "practice" ? "Practice" : "Test"),
    categoryGroup, subtopicGroup, levelGroup, ...(countRow ? [countRow] : []),
    h("div", { class: "row" },
      h("button", { class: "btn secondary", type: "button", onclick: () => homeScreen() }, "Back"),
      h("button", { class: "btn", type: "button", onclick: start }, "Start")));
  render(form);
}

const NO_MATCH = "No cards match the selected filters.";

function practiceScreen(cards) {
  const practice = createPractice(cards);
  if (practice.isEmpty) {
    render(h("div", { class: "stack" }, h("p", { class: "empty" }, NO_MATCH),
      h("button", { class: "btn secondary", type: "button", onclick: () => setupScreen("practice") }, "Back")));
    return;
  }
  const show = (card) => {
    const answerBox = h("div");
    const flip = h("button", { class: "btn", type: "button" }, "Show answer");
    flip.addEventListener("click", () => {
      answerBox.replaceChildren(mathBlock("Answer", card.answer));
      flip.disabled = true;
    });
    render(h("div", { class: "stack" },
      mathBlock(`${card.category} · ${card.subtopic} · Level ${card.level}`, card.question),
      answerBox, flip,
      h("div", { class: "row" },
        h("button", { class: "btn secondary", type: "button", onclick: () => setupScreen("practice") }, "End"),
        h("button", { class: "btn", type: "button", onclick: () => show(practice.next()) }, "Next"))));
  };
  show(practice.next());
}

function testScreen(cards, count) {
  const { cards: picked, notice } = selectTest(cards, count);
  if (picked.length === 0) {
    render(h("div", { class: "stack" }, h("p", { class: "empty" }, NO_MATCH),
      h("button", { class: "btn secondary", type: "button", onclick: () => setupScreen("test") }, "Back")));
    return;
  }
  const blind = () => render(h("div", { class: "stack" },
    notice ? h("p", { class: "notice" }, notice) : null,
    picked.map((card, i) =>
      mathBlock(`Card ${i + 1} of ${picked.length} (answer hidden)`, card.question)),
    h("button", { class: "btn", type: "button", onclick: reveal }, "Reveal all")));
  const reveal = () => render(h("div", { class: "stack" },
    picked.map((card, i) => h("div", { class: "stack" },
      mathBlock(`Card ${i + 1} of ${picked.length} · Question`, card.question),
      mathBlock("Answer", card.answer))),
    h("button", { class: "btn", type: "button", onclick: () => homeScreen() }, "Done")));
  blind();
}

// ---- boot ----------------------------------------------------------------

async function boot() {
  if ("serviceWorker" in navigator) {
    try {
      await navigator.serviceWorker.register("sw.js");
    } catch {
      // The app still works online without a service worker.
    }
  }
  await loadLocal();
  homeScreen();
  if (!meta && navigator.onLine) {
    // First run: Sync automatically so the app works offline right after install.
    const error = await sync();
    if (error) homeScreen(error);
  }
}

boot();
