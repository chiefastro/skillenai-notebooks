#!/usr/bin/env python3
"""Step 5 — figures.

House palette (shared with the other Skillenai notebooks). Validated with the
dataviz palette validator: lightness band, chroma floor, CVD separation and
normal-vision floor all PASS; the green carries a sub-3:1 contrast WARN against
the surface, which is relieved by direct labels and the tables in the README.

Reads the CSVs produced by steps 2-4 so the figures cannot drift from the data.

Usage:
    python 05_make_figures.py
"""
import csv
import collections

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- house design tokens -----------------------------------------------------
C_NEW, C_OLD, C_THIRD = "#eb6834", "#2a78d6", "#1baf7a"
SURFACE, INK, INK_2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e2e1dc"
plt.rcParams["font.family"] = "DejaVu Sans"


def frame(ax, xgrid=False, ygrid=False):
    """Recessive axes: hide spines, keep one hairline baseline, grid behind."""
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK_2, labelsize=9, length=0)
    if ygrid:
        ax.yaxis.grid(True, color=GRID, lw=0.8, zorder=0)
    if xgrid:
        ax.xaxis.grid(True, color=GRID, lw=0.8, zorder=0)
    ax.set_axisbelow(True)


def titles(fig, title, subtitle):
    fig.text(0.012, 0.975, title, fontsize=15, weight="bold", color=INK, va="top")
    fig.text(0.012, 0.925, subtitle, fontsize=9.5, color=INK_2, va="top")


def footer(fig, text):
    fig.text(0.012, 0.02, text, fontsize=8, color=INK_2)


SOURCE_SUPPLY = ("Source: Skillenai — 300,000 US tech worker LinkedIn profiles. "
                 "Share of position descriptions, by year the role started. 2025 partial (to ~Oct).")
def _demand_baseline(path="demand_side_stats.csv"):
    """Read the denominator from the CSV so the caption can never go stale."""
    for r in csv.DictReader(open(path)):
        if r["metric"] == "baseline_postings":
            return int(r["count"])
    raise KeyError("baseline_postings missing from demand_side_stats.csv")


SOURCE_DEMAND = (f"Source: Skillenai jobs index — {_demand_baseline():,} US tech job "
                 "postings, 2026. Within-window shares.")


def read_genai_vs_ml(path="genai_vs_ml_by_year.csv"):
    rows = [r for r in csv.DictReader(open(path)) if int(r["year"]) >= 2018]
    return ([int(r["year"]) for r in rows],
            [float(r["genai_strict_pct"]) for r in rows],
            [float(r["classical_ml_pct"]) for r in rows])


def read_families(path="skill_families_by_year.csv"):
    out = collections.defaultdict(dict)
    for r in csv.DictReader(open(path)):
        out[r["family"]][int(r["year"])] = float(r["share_pct"])
    return out


def read_demand(path="demand_side_stats.csv"):
    return {r["metric"]: (int(r["count"]), float(r["share_pct"]) if r["share_pct"] else None,
                          r.get("measure_type", ""))
            for r in csv.DictReader(open(path))}


# --- figure 1: the crossover -------------------------------------------------
def fig_crossover():
    years, genai, ml = read_genai_vs_ml()
    fig, ax = plt.subplots(figsize=(9.4, 5.6), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    frame(ax, ygrid=True)

    ax.plot(years, ml, color=C_OLD, lw=2, marker="o", ms=5, zorder=3,
            label="Classical machine learning")
    ax.plot(years, genai, color=C_NEW, lw=2, marker="o", ms=5, zorder=4,
            label="Generative AI")

    # direct labels at the line ends — identity never rests on colour alone
    ax.text(years[-1] + 0.08, genai[-1], f"  Generative AI\n  {genai[-1]:.1f}%",
            color=INK, fontsize=9.5, va="center", weight="bold")
    ax.text(years[-1] + 0.08, ml[-1], f"  Classical ML\n  {ml[-1]:.1f}%",
            color=INK_2, fontsize=9.5, va="center")

    # the crossover
    ax.axvline(2024, color=GRID, lw=1, zorder=1)
    ax.annotate("2024: generative AI overtakes\nclassical machine learning",
                xy=(2024, 6.0), xytext=(2020.15, 6.9), fontsize=9, color=INK_2,
                arrowprops=dict(arrowstyle="->", color=INK_2, lw=0.9))

    ax.set_xlim(2017.8, 2026.5)
    ax.set_ylim(0, 8.6)
    ax.set_xticks(years)
    ax.set_yticks([0, 2, 4, 6, 8])
    ax.set_yticklabels(["0", "2%", "4%", "6%", "8%"])
    ax.set_ylabel("Share of CV role descriptions", fontsize=10, color=INK_2)
    ax.legend(frameon=False, fontsize=9.5, labelcolor=INK_2, loc="upper left")

    titles(fig, "Machine learning didn't lose. It stopped moving.",
           "Generative AI overtook classical ML on US tech CVs in 2024 — while ML itself stayed flat.")
    footer(fig, SOURCE_SUPPLY)
    fig.subplots_adjust(left=0.075, right=0.83, top=0.855, bottom=0.13)
    fig.savefig("01_genai_vs_ml_crossover.png", dpi=150, facecolor=SURFACE)
    plt.close(fig)


# --- figure 2: what grew, what didn't ---------------------------------------
def fig_emerging():
    fam = read_families()
    genai_rows = ["LLMs", "AI agents", "RAG", "Generative AI",
                  "LangChain", "AI tools", "prompt engineering", "MCP"]
    ml_rows = ["machine learning", "NLP", "deep learning", "MLOps"]
    rows = genai_rows + ml_rows

    fig, ax = plt.subplots(figsize=(9.4, 7.0), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    frame(ax, xgrid=True)

    ys = range(len(rows))
    h = 0.34
    for i, name in enumerate(rows):
        a, b = fam[name].get(2022, 0), fam[name].get(2025, 0)
        is_ml = name in ml_rows
        col = C_THIRD if is_ml else C_NEW
        # 2px surface gap between the paired bars
        ax.barh(i + h / 2 + 0.01, a, height=h, color=GRID, zorder=2)
        ax.barh(i - h / 2 - 0.01, b, height=h, color=col, zorder=2)
        ax.text(b + 0.06, i - h / 2 - 0.01, f"{b:.2f}%", va="center",
                fontsize=8.5, color=INK)
        ax.text(a + 0.06, i + h / 2 + 0.01, f"{a:.2f}%", va="center",
                fontsize=8.5, color=INK_2)

    ax.set_yticks(list(ys))
    ax.set_yticklabels(rows, fontsize=9.5, color=INK)
    ax.invert_yaxis()
    ax.set_xlim(0, 4.6)
    ax.set_xticks([0, 1, 2, 3, 4])
    ax.set_xticklabels(["0", "1%", "2%", "3%", "4%"])
    ax.set_xlabel("Share of CV role descriptions", fontsize=10, color=INK_2)

    handles = [plt.Rectangle((0, 0), 1, 1, color=GRID),
               plt.Rectangle((0, 0), 1, 1, color=C_NEW),
               plt.Rectangle((0, 0), 1, 1, color=C_THIRD)]
    ax.legend(handles, ["2022", "2025 — generative AI skills", "2025 — classical ML skills"],
              frameon=False, fontsize=9.5, labelcolor=INK_2, loc="lower right")

    # separator between the two blocks
    ax.axhline(len(genai_rows) - 0.5, color=GRID, lw=1)

    titles(fig, "Everything that grew was generative AI",
           "Change in skill prevalence on US tech CVs, 2022 to 2025. The classical stack is flat.")
    footer(fig, SOURCE_SUPPLY)
    fig.subplots_adjust(left=0.19, right=0.965, top=0.855, bottom=0.10)
    fig.savefig("02_emerging_skills.png", dpi=150, facecolor=SURFACE)
    plt.close(fig)


# --- figure 3: demand-side vocabulary ----------------------------------------
def fig_demand():
    """Only TOPIC-MENTION measures appear here.

    The requirement-phrasing measure is deliberately NOT plotted alongside
    these: it is a different kind of measurement (narrow exact constructions,
    known to undercount) and putting it on the same axis invites exactly the
    false comparison that produced the retracted "8:1" claim.
    """
    d = read_demand()
    items = [
        ("Mention AI at all", d["any_ai_mention"][1]),
        ("Generic AI vocabulary\n(“AI tools”, “AI-assisted”)", d["generic_fluency"][1]),
        ("Describe the company as AI-native\n(“AI-first”, “AI-powered”)", d["employer_self_description"][1]),
        ("Name a specific product\n(ChatGPT, Copilot, LangChain)", d["named_products"][1]),
    ]
    labels = [k for k, _ in items]
    vals = [v for _, v in items]

    fig, ax = plt.subplots(figsize=(9.4, 4.8), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    frame(ax, xgrid=True)

    # single series, magnitude only -> one hue, no legend needed
    ax.barh(range(len(vals)), vals, height=0.5, color=C_OLD, zorder=2)
    for i, v in enumerate(vals):
        ax.text(v + 0.4, i, f"{v:.1f}%", va="center", fontsize=10, color=INK, weight="bold")

    ax.set_yticks(range(len(vals)))
    ax.set_yticklabels(labels, fontsize=9.5, color=INK)
    ax.invert_yaxis()
    ax.set_xlim(0, 37)
    ax.set_xticks([0, 10, 20, 30])
    ax.set_xticklabels(["0", "10%", "20%", "30%"])
    ax.set_xlabel("Share of job postings", fontsize=10, color=INK_2)

    ratio = d["generic_fluency"][1] / d["named_products"][1]
    ax.annotate(f"{ratio:.1f}x", xy=(20.4, 2.55), fontsize=15, color=INK,
                weight="bold", ha="center")
    ax.annotate("generic AI vocabulary is used far\nmore than any named product",
                xy=(22.0, 2.55), fontsize=9, color=INK_2, va="center")

    titles(fig, "Employers ask how you work, not which tool you use",
           "How AI appears in US tech job postings. All four bars are the same measure: "
           "does the phrase appear anywhere in the posting?")
    footer(fig, SOURCE_DEMAND)
    fig.subplots_adjust(left=0.30, right=0.965, top=0.815, bottom=0.155)
    fig.savefig("03_demand_side.png", dpi=150, facecolor=SURFACE)
    plt.close(fig)




if __name__ == "__main__":
    fig_crossover()
    fig_emerging()
    fig_demand()
    print("wrote 01_genai_vs_ml_crossover.png, 02_emerging_skills.png, "
          "03_demand_side.png")
