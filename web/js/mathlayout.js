// Pure layout of a card's LaTeX string into wrap-friendly lines of chunks (no DOM, no KaTeX).
//
// A card is authored as one display block: rows separated by top-level `\\`, optionally inside
// `\begin{aligned}`. Rendered as one KaTeX block, nothing can wrap, so on a phone long rows are
// cut off. Instead each top-level row becomes its own line (a row that just continues a sentence
// joins the previous line), and each line is split into chunks:
//   { kind: "math", tex }        math between text runs, rendered as one inline KaTeX span
//   { kind: "text", cmd, tex }   one word of a top-level \text{...} (cmd: "text", "textbf", ...)
//   { kind: "space" }            a word space, and a place the line may wrap
//   { kind: "break" }            a place the line may wrap inside math (after `,` or `\quad`)
// Only *top-level* structure is split: anything inside braces, \left...\right or another
// environment (pmatrix, cases, array, nested in braces) is left as one piece of math.

const TEXT_CMDS = new Set(["text", "textbf", "textit", "textrm", "textsf", "texttt", "textnormal"]);
const BREAK_AFTER = new Set(["quad", "qquad"]);
const CMD = /\\([a-zA-Z]+|[\s\S])/y;
const ENV_NAME = /\s*\{([^}]*)\}/y;

const isGap = (chunk) => chunk.kind === "space" || chunk.kind === "break";

// Index just past the balanced {...} group that opens at s[i].
function groupEnd(s, i) {
  let depth = 0;
  for (; i < s.length; i++) {
    const c = s[i];
    if (c === "\\") i++;
    else if (c === "{") depth++;
    else if (c === "}" && --depth === 0) return i + 1;
  }
  return s.length;
}

// Split a \text body into word chunks at spaces outside braces and inline $...$.
function textChunks(cmd, body) {
  const out = [];
  let word = "";
  let braces = 0;
  let inMath = false;
  const flush = () => {
    if (word) out.push({ kind: "text", cmd, tex: word });
    word = "";
  };
  for (let i = 0; i < body.length; i++) {
    const c = body[i];
    if (c === "\\") {
      word += body.slice(i, i + 2);
      i++;
      continue;
    }
    if (c === "$") inMath = !inMath;
    else if (c === "{") braces++;
    else if (c === "}") braces--;
    if (/\s/.test(c) && braces === 0 && !inMath) {
      flush();
      out.push({ kind: "space" });
      continue;
    }
    word += c;
  }
  flush();
  return out;
}

// Collapse runs of gaps (a space wins over a break), drop gaps at either end, and pad math
// chunks that touch text with `{}` so a leading/trailing relation or operator keeps its spacing.
function tidy(chunks) {
  const out = [];
  for (const chunk of chunks) {
    if (isGap(chunk) && (out.length === 0 || isGap(out.at(-1)))) {
      if (chunk.kind === "space" && out.length) out[out.length - 1] = chunk;
      continue;
    }
    out.push(chunk);
  }
  while (out.length && isGap(out.at(-1))) out.pop();
  const textNear = (from, step) => {
    for (let j = from; j >= 0 && j < out.length; j += step) {
      if (out[j].kind !== "space") return out[j].kind === "text";
    }
    return false;
  };
  return out.map((chunk, i) => {
    if (chunk.kind !== "math") return chunk;
    const tex = `${textNear(i - 1, -1) ? "{}" : ""}${chunk.tex}${textNear(i + 1, 1) ? "{}" : ""}`;
    return { kind: "math", tex };
  });
}

export function layoutLines(text) {
  const lines = [];
  let chunks = [];
  let math = "";
  let braces = 0;
  let brackets = 0; // open ( and [ on this line: \text inside E[V | \text{buy}] stays math
  let lefts = 0;
  const envs = []; // open environments; true = a top-level `aligned` that is being flattened
  const topLevel = () => braces === 0 && lefts === 0 && envs.every(Boolean);
  const flushMath = () => {
    // Keep the space of a trailing control space (`x\ `) that trim() would cut to a bare `\`.
    const tex = math.trim().replace(/(^|[^\\])(\\\\)*\\$/, "$& ");
    if (tex) chunks.push({ kind: "math", tex });
    math = "";
  };
  const breakMath = () => {
    flushMath();
    chunks.push({ kind: "break" });
  };
  const breakLine = () => {
    flushMath();
    const line = tidy(chunks);
    const prev = lines.at(-1)?.at(-1);
    // A row break in the middle of a sentence was only the author's hand-wrapping for a wide
    // screen: continue the previous line so the prose re-wraps to the card width.
    if (line[0]?.kind === "text" && prev?.kind === "text" && !/[.:;?!]$/.test(prev.tex)) {
      lines.at(-1).push({ kind: "space" }, ...line);
    } else if (line.length) {
      lines.push(line);
    }
    chunks = [];
    brackets = 0;
  };

  for (let i = 0; i < text.length;) {
    const c = text[i];
    if (c !== "\\") {
      i++;
      if (c === "{") braces++;
      else if (c === "}") braces--;
      else if ((c === "(" || c === "[") && topLevel()) brackets++;
      else if ((c === ")" || c === "]") && topLevel()) brackets--;
      if (c === "&" && topLevel()) continue; // alignment points are dropped when flattened
      math += c;
      if (c === "," && topLevel()) {
        math += "\\,"; // the thin space KaTeX would put after the comma
        breakMath();
      }
      continue;
    }
    CMD.lastIndex = i;
    const [raw, name] = CMD.exec(text);
    i += raw.length;

    if (name === "\\" && topLevel()) {
      breakLine();
      const spacing = /^\[[^\]]*\]/.exec(text.slice(i)); // optional \\[4pt]
      if (spacing) i += spacing[0].length;
    } else if (name === "begin" || name === "end") {
      ENV_NAME.lastIndex = i;
      const env = ENV_NAME.exec(text);
      const envRaw = env ? env[0] : "";
      i += envRaw.length;
      if (name === "begin") {
        const flatten = env?.[1] === "aligned" && topLevel();
        envs.push(flatten);
        if (flatten) breakLine();
        else math += raw + envRaw;
      } else if (envs.pop()) {
        breakLine();
      } else {
        math += raw + envRaw;
      }
    } else if (TEXT_CMDS.has(name) && text[i] === "{" && topLevel() && !/[\^_]\s*$/.test(math)
      && (brackets <= 0 || /\s/.test(text.slice(i + 1, groupEnd(text, i) - 1).trim()))) {
      // \text used as a sub/superscript stays math, and so does a single word inside brackets
      // (E[V | \text{buy}]) so the bracket can't break; longer bracketed prose still wraps.
      const end = groupEnd(text, i);
      flushMath();
      const words = textChunks(name, text.slice(i + 1, end - 1));
      // \text{... bias}^2: the scripted last word stays math so the script attaches to it.
      if (/^\s*[\^_]/.test(text.slice(end)) && words.at(-1)?.kind === "text") {
        math = `\\${name}{${words.pop().tex}}`;
      }
      chunks.push(...words);
      i = end;
    } else if (name === "includegraphics") {
      // Its [width=..,height=..] option has commas that must not be split; at top level an
      // image always gets a line of its own.
      const arg = /^\s*(\[[^\]]*\])?\s*\{[^}]*\}/.exec(text.slice(i));
      const own = topLevel();
      if (own) breakLine();
      math += raw + (arg ? arg[0] : "");
      i += arg ? arg[0].length : 0;
      if (own) breakLine();
    } else if (name === "left" || name === "right") {
      lefts += name === "left" ? 1 : -1;
      math += raw;
      // take a plain delimiter along so \right] is not counted as a top-level bracket
      const delim = /^\s*[^\\\s]/.exec(text.slice(i));
      if (delim) {
        math += delim[0];
        i += delim[0].length;
      }
    } else {
      math += raw;
      if (BREAK_AFTER.has(name) && topLevel()) breakMath();
    }
  }
  breakLine();
  return lines;
}
