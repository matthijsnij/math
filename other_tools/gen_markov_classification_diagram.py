"""One-off script to generate the state diagram for
probability-statistics-markov-chains-2-03 (classify states: transient /
recurrent / absorbing, communicating classes {1}, {2,3}, {4}).
Run: .\\venv\\Scripts\\python.exe other_tools\\gen_markov_classification_diagram.py
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

fig, ax = plt.subplots(figsize=(6, 5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.set_aspect("equal")
ax.axis("off")

positions = {
    "1": (1.5, 6),
    "2": (6, 6),
    "3": (8.5, 3),
    "4": (1.5, 1.5),
}
radius = 0.6

for name, (x, y) in positions.items():
    ax.add_patch(Circle((x, y), radius, fc="white", ec="black", zorder=3))
    ax.text(x, y, name, ha="center", va="center", fontsize=14, zorder=4)


def edge(n1, n2, label, rad=0.0, label_offset=(0, 0.3)):
    x1, y1 = positions[n1]
    x2, y2 = positions[n2]
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        connectionstyle=f"arc3,rad={rad}",
        arrowstyle="-|>", mutation_scale=15,
        shrinkA=radius * 72, shrinkB=radius * 72,
        color="black",
    )
    ax.add_patch(arrow)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ax.text(mx + label_offset[0], my + label_offset[1], label, ha="center", fontsize=10)


def self_loop(n, label):
    x, y = positions[n]
    loop = Circle((x, y + radius + 0.35), 0.35, fc="none", ec="black")
    ax.add_patch(loop)
    arrow = FancyArrowPatch(
        (x + 0.05, y + 2 * radius + 0.05), (x + 0.1, y + 2 * radius),
        arrowstyle="-|>", mutation_scale=12, color="black",
    )
    ax.add_patch(arrow)
    ax.text(x, y + 2 * radius + 0.75, label, ha="center", fontsize=10)


edge("1", "2", "0.5", rad=0.0, label_offset=(0, 0.3))
edge("1", "4", "0.5", rad=0.0, label_offset=(-0.4, 0))
edge("2", "3", "0.5", rad=0.2, label_offset=(0.4, 0))
edge("3", "2", "0.5", rad=0.2, label_offset=(-0.1, -0.5))
self_loop("2", "0.5")
self_loop("3", "0.5")
self_loop("4", "1")

plt.tight_layout()
plt.savefig(
    "data/graphs/probability-statistics-markov-chains-2-03.png",
    dpi=150,
)
print("saved")
