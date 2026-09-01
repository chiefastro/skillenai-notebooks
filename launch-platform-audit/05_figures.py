"""Generate the three report figures from platforms.csv / network_graph.csv."""
import csv
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

# validated categorical palette (dataviz skill reference, light mode)
BLUE = "#2a78d6"
ORANGE = "#eb6834"
AQUA = "#1baf7a"
YELLOW = "#eda100"
RED = "#e34948"
GRAY = "#8a897f"
SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e4e3de"

plt.rcParams.update({
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "text.color": TEXT_PRIMARY,
    "axes.edgecolor": GRID,
    "axes.labelcolor": TEXT_SECONDARY,
    "xtick.color": TEXT_SECONDARY,
    "ytick.color": TEXT_SECONDARY,
    "font.size": 11,
    "font.family": "sans-serif",
})


def load_platforms():
    with open("platforms.csv") as f:
        return list(csv.DictReader(f))


def fig_business_models(rows):
    labels_map = {
        "destination": "Destination\n(list on their one site)",
        "submission_service": "Submission service\n(3rd party submits you elsewhere)",
        "owned_network": "Owned network\n(sells placement on sites they own)",
        "meta_list": "Meta-list\n(lists other platforms)",
        "unclear": "Unclear",
    }
    counts = Counter(r["business_model"] for r in rows)
    order = ["destination", "submission_service", "unclear", "meta_list", "owned_network"]
    order = [k for k in order if k in counts]
    values = [counts[k] for k in order]
    labels = [labels_map.get(k, k) for k in order]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    y = range(len(order))
    bars = ax.barh(list(y), values, color=BLUE, height=0.6)
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel(f"Number of platforms (n={len(rows)})")
    ax.set_title("Launch platforms by business model", fontsize=13, fontweight="bold", color=TEXT_PRIMARY, loc="left")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis="x", color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for bar, v in zip(bars, values):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2, str(v),
                 va="center", ha="left", color=TEXT_PRIMARY, fontsize=10)
    fig.text(0.02, 0.01, "Snapshot audit, 2026-08-31. Source: platforms.csv", fontsize=8, color=TEXT_SECONDARY)
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    fig.savefig("01_business_models.png", dpi=150)
    plt.close(fig)


def fig_rel_compliance(rows):
    gradable = [r for r in rows if r["paid_link_rel"] != "unknown" and r["free_link_rel"] != "unknown"]
    n = len(gradable)
    metrics = [
        ("Paid links pass PageRank\n(no sponsored/nofollow on paid placements)",
         sum(1 for r in gradable if r["paid_passes_pagerank"] == "True")),
        ("rel_inversion\n(paid = dofollow, free = nofollow)",
         sum(1 for r in gradable if r["rel_inversion"] == "True")),
        ("Guarantees a specific DR/DA number\nin marketing copy",
         sum(1 for r in rows if r["guarantees_dr"] == "True")),
        ("Free tier requires a reciprocal\nbadge/link on your site",
         sum(1 for r in rows if r["badge_required_free"] == "True")),
    ]
    labels = [m[0] for m in metrics]
    values = [m[1] for m in metrics]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    y = range(len(labels))
    bars = ax.barh(list(y), values, color=[RED, RED, ORANGE, ORANGE], height=0.55)
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel(f"Number of platforms (of {len(rows)} audited)")
    ax.set_title("Link-attribution patterns observed", fontsize=13, fontweight="bold", color=TEXT_PRIMARY, loc="left")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis="x", color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for bar, v in zip(bars, values):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2, str(v),
                 va="center", ha="left", color=TEXT_PRIMARY, fontsize=10)
    fig.text(0.02, 0.05,
              f"Top two rows are of the {n} platforms (of {len(rows)}) with a gradable paid/free rel; "
              "the rest were unknown (JS-rendered or no visible outbound member links).",
              fontsize=7.5, color=TEXT_SECONDARY)
    fig.text(0.02, 0.01, "Snapshot audit, 2026-08-31. Google's link spam policy requires paid links to carry "
                          "rel=\"sponsored\" or rel=\"nofollow\". Source: platforms.csv", fontsize=7.5, color=TEXT_SECONDARY)
    fig.tight_layout(rect=[0, 0.09, 1, 1])
    fig.savefig("02_rel_compliance.png", dpi=150)
    plt.close(fig)


def fig_network_graph():
    with open("network_graph.csv") as f:
        edges = list(csv.DictReader(f))

    G = nx.Graph()
    style_map = {
        "high": {"color": RED, "width": 2.4, "style": "solid"},
        "medium": {"color": ORANGE, "width": 1.6, "style": "solid"},
    }
    kept = [e for e in edges if e["confidence"] in ("high", "medium")]
    low_count = sum(1 for e in edges if e["confidence"] == "low")

    for e in kept:
        G.add_edge(e["domain_a"], e["domain_b"], confidence=e["confidence"], signal=e["shared_signal"])

    fig, ax = plt.subplots(figsize=(9, 7))
    if len(G.nodes) == 0:
        ax.text(0.5, 0.5, "No medium/high-confidence ownership edges found", ha="center", va="center")
    else:
        pos = nx.spring_layout(G, seed=7, k=1.1)
        for conf in ("medium", "high"):
            elist = [(u, v) for u, v, d in G.edges(data=True) if d["confidence"] == conf]
            if elist:
                nx.draw_networkx_edges(G, pos, edgelist=elist, ax=ax,
                                        edge_color=style_map[conf]["color"],
                                        width=style_map[conf]["width"])
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=SURFACE, edgecolors=BLUE,
                                linewidths=1.8, node_size=1800)
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=9, font_color=TEXT_PRIMARY)
        ax.axis("off")

        handles = [
            plt.Line2D([0], [0], color=RED, lw=2.4, label="High confidence (shared GA/Stripe ID or explicit self-declared ownership statement)"),
            plt.Line2D([0], [0], color=ORANGE, lw=1.6, label="Medium confidence (shared IP + shared WHOIS registrant)"),
        ]
        ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.08),
                  frameon=False, fontsize=8.5, labelcolor=TEXT_SECONDARY)

    ax.set_title("Confirmed ownership connections between audited platforms", fontsize=13, fontweight="bold",
                  color=TEXT_PRIMARY, loc="left")
    fig.text(0.02, 0.01,
              f"{low_count} additional low-confidence shared-IP edges are excluded from this figure -- "
              "shared hosting/CDN IPs alone are weak evidence and are not shown. See network_graph.csv "
              "for the full edge list with confidence tiers.", fontsize=7.5, color=TEXT_SECONDARY, wrap=True)
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig("03_network_graph.png", dpi=150)
    plt.close(fig)


def main():
    rows = load_platforms()
    fig_business_models(rows)
    fig_rel_compliance(rows)
    fig_network_graph()
    print("wrote 01_business_models.png, 02_rel_compliance.png, 03_network_graph.png")


if __name__ == "__main__":
    main()
