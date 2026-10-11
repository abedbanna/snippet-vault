#!/usr/bin/env python3
"""Draw the two conceptual figures for Day 3 Session 5 (automation basics with n8n) into figures/d3s5_*.png.

Everything else on the Session 5 slides is a real screenshot of n8n Cloud (figures/d3s5_shot_*.jpg, captured
11 October 2026 on the instructor's trial workspace). These two show what a screenshot cannot: how the Session 4
future-state map becomes nodes, and how items flow from node to node.
Usage: python3 tools/make_day3s5_figures.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from make_day2_figures import ORANGE, BLACK, GREY, LIGHT, RED, GREEN, box, arrow  # noqa: E402
from make_day2s4_figures import AMBER, GREEN_BG, AMBER_BG, RED_BG  # noqa: E402

FIG = pathlib.Path(__file__).resolve().parent.parent / "figures"

# Session 4 future-state step -> the n8n node that implements it in the demo (Day3_S5_Leave_Request_Demo.json)
MAPPING = [
    ("Employee fills the leave form", "trigger", "n8n Form Trigger", "Leave request form"),
    ("Look up the balance", "rule", "Google Sheets: Get row(s)", "Look up balance"),
    ("Run the policy checks", "rule", "Code (or Edit Fields)", "Run policy checks"),
    ("All checks pass?", "rule", "IF", "All checks pass?"),
    ("Record the request", "rule", "Google Sheets: Append row", "Log request / Log flagged request"),
    ("Decision card to the manager", "rule", "Gmail: Send", "Decision card to manager"),
    ("Failed checks go to HR", "rule", "Gmail: Send", "Flag to HR"),
    ("Manager decides", "human", "stays human (Day 5 builds the gate)", ""),
]
COLOURS = {"trigger": (ORANGE, "#fff4e0"), "rule": (GREEN, GREEN_BG), "human": (RED, RED_BG)}


def draw_mapping(path):
    fig, ax = plt.subplots(figsize=(13, 7.2))
    ax.set_xlim(0, 13); ax.set_ylim(0, 8.6); ax.axis("off")
    ax.text(2.9, 8.15, "Session 4: future-state step", ha="center", fontsize=13, fontweight="bold")
    ax.text(9.6, 8.15, "Session 5: n8n node", ha="center", fontsize=13, fontweight="bold")
    for i, (step, kind, node, name) in enumerate(MAPPING):
        y = 7.35 - i * 0.92
        ec, fc = COLOURS[kind]
        box(ax, 2.9, y, 4.9, 0.66, step, fc=fc, ec=ec, fs=11.5)
        human = kind == "human"
        box(ax, 9.6, y, 5.6, 0.66, node + ("" if human else f"\n“{name}”"), fc="white" if not human else LIGHT,
            ec=GREY if human else BLACK, fs=10.5, ls="--" if human else "-")
        arrow(ax, (5.4, y), (6.75, y), col=GREY if human else BLACK, ls="--" if human else "-")
    ax.text(6.5, 0.15, "Orange = trigger, green = rule-based step, red = stays with a person. One future-state step, one node (or two).",
            ha="center", fontsize=10.5, color=GREY)
    plt.tight_layout(); fig.savefig(path, dpi=160, facecolor="white"); plt.close(fig)


def draw_items(path):
    fig, ax = plt.subplots(figsize=(13, 5.6))
    ax.set_xlim(0, 13); ax.set_ylim(0, 6); ax.axis("off")
    # trigger -> 3 items -> node runs 3 times -> 3 rows
    box(ax, 1.4, 3.2, 2.2, 1.1, "Trigger\n(schedule)", fc="#fff4e0", ec=ORANGE, fs=12, bold=True)
    box(ax, 4.6, 3.2, 2.4, 1.1, "Google Sheets\nGet row(s)", fs=11.5)
    arrow(ax, (2.5, 3.2), (3.4, 3.2))
    for k, y in enumerate((4.6, 3.2, 1.8)):
        box(ax, 7.4, y, 2.0, 0.8, f"item {k + 1}\n{{Name, Amount}}", fc=LIGHT, ec=GREY, fs=10)
        arrow(ax, (5.8, 3.2), (6.4, y), col=GREY)
        box(ax, 10.6, y, 2.6, 0.8, f"Gmail: Send  (run {k + 1})", fs=10.5)
        arrow(ax, (8.4, y), (9.3, y))
    ax.text(6.5, 5.65, "Data moves as items. Each node runs once per item it receives.", ha="center", fontsize=13,
            fontweight="bold")
    ax.text(6.5, 0.55, "3 rows in the sheet = 3 items = 3 e-mails. 40 rows would mean 40 e-mails: check the output panel before you publish.",
            ha="center", fontsize=10.5, color=GREY)
    plt.tight_layout(); fig.savefig(path, dpi=160, facecolor="white"); plt.close(fig)


if __name__ == "__main__":
    draw_mapping(FIG / "d3s5_map_to_nodes.png")
    draw_items(FIG / "d3s5_items_flow.png")
    print("wrote figures/d3s5_map_to_nodes.png, figures/d3s5_items_flow.png")
