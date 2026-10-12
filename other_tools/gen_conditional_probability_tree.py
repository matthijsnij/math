"""One-off script to generate the probability tree image for
probability-statistics-conditional-probability-and-bayes-4-04.
Run: .\\venv\\Scripts\\python.exe other_tools\\gen_conditional_probability_tree.py
"""

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis("off")

node_style = dict(boxstyle="round,pad=0.3", fc="white", ec="black")


def node(x, y, text):
    ax.text(x, y, text, ha="center", va="center", bbox=node_style, fontsize=10)


def edge(x1, y1, x2, y2, label, label_dx=0.0, label_dy=0.0):
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-", lw=1.2),
    )
    ax.text((x1 + x2) / 2 + label_dx, (y1 + y2) / 2 + label_dy, label,
            ha="center", va="center", fontsize=9)


# Root
node(0.6, 4, "Start")

# Stage 1: Line
node(3, 6.5, "Line A")
node(3, 1.5, "Line B")
edge(1.1, 4, 2.6, 6.5, "0.7", label_dx=-0.15, label_dy=0.3)
edge(1.1, 4, 2.6, 1.5, "0.3", label_dx=-0.15, label_dy=-0.3)

# Stage 2: Inspection, from Line A
node(5.6, 7.5, "Pass")
node(5.6, 5.5, "Fail\n(scrapped)")
edge(3.5, 6.5, 5.1, 7.5, "0.9", label_dx=0.0, label_dy=0.25)
edge(3.5, 6.5, 5.1, 5.5, "0.1", label_dx=0.0, label_dy=-0.25)

# Stage 2: Inspection, from Line B
node(5.6, 2.5, "Pass")
node(5.6, 0.5, "Fail\n(scrapped)")
edge(3.5, 1.5, 5.1, 2.5, "0.75", label_dx=0.0, label_dy=0.25)
edge(3.5, 1.5, 5.1, 0.5, "0.25", label_dx=0.0, label_dy=-0.25)

# Stage 3: Final test, from Line A / Pass
node(8.6, 8, "Defective")
node(8.6, 7, "OK")
edge(6.1, 7.5, 8.1, 8, "0.02", label_dx=0.1, label_dy=0.2)
edge(6.1, 7.5, 8.1, 7, "0.98", label_dx=0.1, label_dy=-0.2)

# Stage 3: Final test, from Line B / Pass
node(8.6, 3, "Defective")
node(8.6, 2, "OK")
edge(6.1, 2.5, 8.1, 3, "0.06", label_dx=0.1, label_dy=0.2)
edge(6.1, 2.5, 8.1, 2, "0.94", label_dx=0.1, label_dy=-0.2)

plt.tight_layout()
plt.savefig(
    "data/graphs/probability-statistics-conditional-probability-and-bayes-4-04.png",
    dpi=150,
)
print("saved")
