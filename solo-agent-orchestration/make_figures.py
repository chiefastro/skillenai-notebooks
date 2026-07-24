#!/usr/bin/env python3
"""Figures for the solo-agent-orchestration post.
Run: python3 make_figures.py  (needs numpy, matplotlib)
Data: weekly_data.json (one solo dev, Jun 1 - Jul 20 2026)."""
import json, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

D = json.load(open("weekly_data.json"))
W = D["weeks"]
xs = np.array([w["tokens"] for w in W], float)
prs = np.array([w["prs"] for w in W], float)
tix = np.array([w["tickets"] for w in W], float)

# Jellyfish reference curve  y = a ln(x) + b
a, b = D["jellyfish_curve"]["a"], D["jellyfish_curve"]["b"]
curve = lambda x: a*np.log(x) + b
CEIL = D["jellyfish_curve"]["pr_ceiling"]

# palette
JELLY_ORANGE = "#ff5a36"
JELLY_PURPLE = "#7c5cff"      # their obedient dots
SK_CYAN = "#18c8d8"           # Skillenai brand
SK_VIOLET = "#7b3ff2"
INK = "#141422"
GRID = "#e9e9f0"
tokfmt = FuncFormatter(lambda v,_: f"{v/1e6:.0f}M" if v < 1e9 else f"{v/1e9:.1f}B")


# ---------------------------------------------------------------- 01 MEME HERO
def meme_hero():
    fig, ax = plt.subplots(figsize=(12, 7.4))
    fig.patch.set_facecolor("white")

    # --- reconstruct Jellyfish's own chart, obedient dots hugging the curve ---
    xc = np.logspace(np.log10(3.5e7), np.log10(5e8), 300)
    ax.plot(xc, curve(xc), color=JELLY_ORANGE, lw=3.2, zorder=3, solid_capstyle="round")
    # their ~40 points along the curve (deterministic jitter, no RNG)
    xt = np.logspace(np.log10(3.8e7), np.log10(4.4e8), 40)
    jitter = 0.10*np.sin(np.arange(40)*2.3) + 0.06*np.cos(np.arange(40)*5.1)
    yt = curve(xt) + jitter
    ax.scatter(xt, yt, s=42, color=JELLY_PURPLE, alpha=0.85, zorder=4, edgecolor="none")
    ax.scatter([3.4e8],[4.15], s=42, color=JELLY_PURPLE, alpha=0.85, zorder=4)  # their lone outlier

    # agentic barrier + band bar (their framing)
    ax.axvline(5e7, ls=(0,(6,4)), color="#5a5a6e", lw=1.4, zorder=2)
    ax.text(5.3e7, 39, "AGENTIC BARRIER", rotation=90, va="top", ha="left",
            fontsize=8.5, color="#5a5a6e", fontweight="bold")
    for x0,x1,lbl,c in [(3.5e7,5e7,"Interactive","#efeafc"),
                        (5e7,2e8,"Autonomous agents","#c9b8f7"),
                        (2e8,5e8,"Agent orchestration","#8b5cf6")]:
        ax.axvspan(x0,x1, ymin=0.0, ymax=0.028, color=c, zorder=1)
        if lbl!="Interactive":
            ax.text(np.sqrt(x0*x1), 0.35, lbl, ha="center", va="center",
                    fontsize=8, color="white", fontweight="bold", zorder=2)

    # --- THE INTRUDER: our 8 weekly points, way up top ---
    ax.scatter(xs, prs, s=230, color=SK_VIOLET, edgecolor="white", lw=2.2, zorder=6)
    for w in W:
        if w["prs"] >= 20:  # label the high cluster once via annotation, keep dots clean
            pass
    med_x, med_y = float(np.median(xs)), float(np.median(prs))

    # deadpan meme annotations
    ax.annotate("me. solo. after hours. ☕",
                xy=(med_x, med_y), xytext=(5.8e7, 31.5),
                fontsize=15.5, fontweight="bold", color=SK_VIOLET,
                arrowprops=dict(arrowstyle="-|>", color=SK_VIOLET, lw=2.2,
                                connectionstyle="arc3,rad=-0.18"))
    ax.text(5.8e7, 29.2, "(these are weeks, not a typo)", fontsize=10.5,
            style="italic", color="#555")
    ax.annotate("everyone else, politely\nobeying the plateau",
                xy=(2.4e8, 3.3), xytext=(1.55e8, 11.5),
                fontsize=10.5, color="#5a5a6e", ha="center",
                arrowprops=dict(arrowstyle="-|>", color="#9a9aae", lw=1.6,
                                connectionstyle="arc3,rad=0.25"))
    ax.axhline(CEIL, ls=":", color=JELLY_ORANGE, lw=1.3, zorder=2)
    ax.text(3.6e7, CEIL+0.55, "Jellyfish 'diminishing returns' ceiling  ~3.9 PRs/wk",
            fontsize=8.5, color=JELLY_ORANGE)

    ax.set_xscale("log")
    ax.set_xlim(3.5e7, 1.5e9)
    ax.set_ylim(0, 40)
    ax.set_xlabel("Tokens per dev per week  (total, incl. cache reads)", fontsize=11)
    ax.set_ylabel("Merged PRs per dev per week", fontsize=11)
    ax.xaxis.set_major_formatter(tokfmt)
    ax.grid(True, which="both", color=GRID, lw=0.6)
    for s in ("top","right"): ax.spines[s].set_visible(False)
    fig.suptitle("Two Headwinds of AI Development. And Then There's Me.",
                 x=0.5, y=0.975, fontsize=17, fontweight="bold", color=INK)
    ax.text(0.0, 1.02, "Base chart & curve: Jellyfish Research (1M developer-weeks). "
            "Purple points: one solo dev, Jun–Jul 2026.",
            transform=ax.transAxes, fontsize=8.5, color="#888")
    fig.tight_layout(rect=(0,0,1,0.94))
    fig.savefig("01_hero_meme.png", dpi=140, facecolor="white")
    plt.close(fig)
    print("wrote 01_hero_meme.png  (median week:", int(med_y), "PRs @", f"{med_x/1e6:.0f}M tok)")


# ------------------------------------------------ 02 HONEST PLACEMENT (log-x)
def placement():
    fig, ax = plt.subplots(figsize=(11, 6.6))
    xc = np.logspace(np.log10(3e7), np.log10(5e8), 200)
    ax.plot(xc, curve(xc), color=JELLY_ORANGE, lw=3, label="Jellyfish curve (industry avg)")
    ax.axvline(5e7, ls="--", color="#666", lw=1.2)
    ax.text(5.3e7, 34, "AGENTIC BARRIER", rotation=90, va="top", fontsize=8, color="#666")
    ax.scatter(xs, prs, s=150, color=SK_VIOLET, edgecolor="white", lw=1.6,
               zorder=5, label="My weekly points (Jun–Jul 2026)")
    for w in W:
        ax.annotate(w["week"][5:], (w["tokens"], w["prs"]),
                    textcoords="offset points", xytext=(7,6), fontsize=7.5, color="#333")
    mx, my = float(np.median(xs)), float(np.median(prs))
    ax.scatter([mx],[my], s=340, marker="*", color=INK, zorder=6,
               label=f"My median week ({mx/1e6:.0f}M tok, {my:.0f} PRs)")
    ax.axhline(CEIL, ls=":", color=JELLY_ORANGE, lw=1)
    ax.text(3.1e7, CEIL+0.4, "curve ceiling ~3.9 PRs/wk", fontsize=8, color=JELLY_ORANGE)
    ax.set_xscale("log"); ax.set_xlim(3e7, 1.4e9); ax.set_ylim(0, 40)
    ax.set_xlabel("Tokens per dev per week  (total, incl. cache reads)")
    ax.set_ylabel("Merged PRs per dev per week")
    ax.set_title("Where one solo dev lands on the Jellyfish curve", fontweight="bold")
    ax.xaxis.set_major_formatter(tokfmt)
    ax.grid(True, which="both", color=GRID, lw=0.6)
    for s in ("top","right"): ax.spines[s].set_visible(False)
    ax.legend(loc="upper left", framealpha=0.95, fontsize=9)
    fig.tight_layout(); fig.savefig("02_placement.png", dpi=140, facecolor="white"); plt.close(fig)
    print("wrote 02_placement.png")


# ------------------------------------------------ 03 WEEKLY OUTPUT BARS
def weekly():
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(11, 7), sharex=True,
                                 gridspec_kw=dict(height_ratios=[1,1.2]))
    lbl = [w["week"][5:] for w in W]
    x = np.arange(len(W))
    a1.bar(x, xs/1e6, color=SK_CYAN, width=0.6)
    a1.axhline(500, ls="--", color=JELLY_ORANGE, lw=1.3)
    a1.text(len(W)-0.5, 520, "right edge of Jellyfish chart (500M)", ha="right",
            fontsize=8.5, color=JELLY_ORANGE)
    a1.set_ylabel("Tokens / week (M)")
    a1.set_title("Weekly throughput — one solo developer, nights & weekends", fontweight="bold")
    for s in ("top","right"): a1.spines[s].set_visible(False)

    w2 = 0.4
    a2.bar(x-w2/2, prs, w2, color=SK_VIOLET, label="Merged PRs")
    a2.bar(x+w2/2, tix, w2, color="#f4a63a", label="Tickets completed")
    a2.axhline(CEIL, ls=":", color=JELLY_ORANGE, lw=1.3)
    a2.text(len(W)-0.5, CEIL+0.5, "Jellyfish PR ceiling ~3.9/wk", ha="right",
            fontsize=8.5, color=JELLY_ORANGE)
    a2.set_ylabel("Count / week"); a2.set_xticks(x); a2.set_xticklabels(lbl)
    a2.set_xlabel("Week of (2026)"); a2.legend(loc="upper right", fontsize=9)
    for s in ("top","right"): a2.spines[s].set_visible(False)
    fig.tight_layout(); fig.savefig("03_weekly.png", dpi=140, facecolor="white"); plt.close(fig)
    print("wrote 03_weekly.png")


# ------------------------------------------------ 04 VIRTUAL-TEAM ECONOMICS
def economics():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 5.2))
    # left: team-equivalent
    med_pr = float(np.median(prs))
    team = med_pr / CEIL
    a1.bar(["Jellyfish\navg dev", "Me\n(solo + agents)"], [CEIL, med_pr],
           color=["#c9c9d6", SK_VIOLET], width=0.55)
    a1.text(0, CEIL+0.4, f"{CEIL:.1f}", ha="center", fontsize=11)
    a1.text(1, med_pr+0.4, f"{med_pr:.0f}", ha="center", fontsize=11, fontweight="bold")
    a1.set_ylabel("Median merged PRs / week")
    a1.set_title(f"~{team:.0f} developers' worth of merged output\n(the size that needs a manager)",
                 fontweight="bold", fontsize=11)
    for s in ("top","right"): a1.spines[s].set_visible(False)

    # right: cost — what it "should" cost vs what it costs
    T = D["totals"]
    a2.bar(["API list-price\nequivalent", "What I\nactually pay"],
           [T["cost_api_equiv_total"], T["actual_subscription_per_month"]*1.8],
           color=["#c9c9d6", SK_CYAN], width=0.55)
    a2.text(0, T["cost_api_equiv_total"]+60, f"${T['cost_api_equiv_total']:,}", ha="center", fontsize=11)
    a2.text(1, T["actual_subscription_per_month"]*1.8+60, "~$180\n($100/mo plan)",
            ha="center", fontsize=10.5, fontweight="bold")
    a2.set_ylabel("Cost over the 8-week window ($)")
    a2.set_title(f"~17× list value — and {int(T['opus_share_cost']*100)}% of it is Opus,\nnot cheap-model filler",
                 fontweight="bold", fontsize=11)
    for s in ("top","right"): a2.spines[s].set_visible(False)
    fig.suptitle("The virtual team's payroll", fontsize=14, fontweight="bold", y=1.0)
    fig.tight_layout(); fig.savefig("04_economics.png", dpi=140, facecolor="white"); plt.close(fig)
    print("wrote 04_economics.png")


if __name__ == "__main__":
    # NOTE: the final hero (01_hero_meme.png) is generated by hero.py, not meme_hero()
    # below — hero.py holds the shipped "mystery"-tone version. meme_hero() is kept
    # only as the earlier draft for reference and is intentionally NOT called here.
    placement(); weekly(); economics()
