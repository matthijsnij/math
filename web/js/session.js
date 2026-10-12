// Pure Practice / Test session logic. `rng` is injectable (defaults to Math.random).

export function shuffle(items, rng = Math.random) {
  const out = [...items];
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

// Endless shuffled cycle: reshuffles once every card has been shown.
export function createPractice(cards, rng = Math.random) {
  let queue = [];
  return {
    isEmpty: cards.length === 0,
    next() {
      if (cards.length === 0) return null;
      if (queue.length === 0) queue = shuffle(cards, rng);
      return queue.shift();
    },
  };
}

export function selectTest(cards, count, rng = Math.random) {
  const n = Math.max(1, Math.floor(Number(count)) || 1);
  if (cards.length === 0) return { cards: [], notice: null };
  if (cards.length < n) {
    return {
      cards: shuffle(cards, rng),
      notice: `Only ${cards.length} card${cards.length === 1 ? "" : "s"} matched the filters; running the test on all of them.`,
    };
  }
  return { cards: shuffle(cards, rng).slice(0, n), notice: null };
}
