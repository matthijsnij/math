// Pure card filtering. OR within a filter, AND across filters, empty = no restriction.

const passes = (selected, value) => !selected || selected.length === 0 || selected.includes(value);

export function filterCards(cards, { categories, subtopics, levels } = {}) {
  return cards.filter(
    (card) =>
      passes(categories, card.category) &&
      passes(subtopics, card.subtopic) &&
      passes(levels, card.level),
  );
}

// Subtopics that have Cards in the ticked Categories (all when none ticked), sorted.
export function availableSubtopics(cards, categories = []) {
  const inScope = filterCards(cards, { categories });
  return [...new Set(inScope.map((card) => card.subtopic))].sort((a, b) => a.localeCompare(b));
}
