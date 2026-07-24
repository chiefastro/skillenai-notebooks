#!/usr/bin/env python3
"""Hero: Jellyfish's chart, faithfully reproduced, with a BROKEN y-axis revealing
one solo developer on a different scale. The break = the Coordination Tax.
Matches the source aesthetic (orange curve, purple dots, regime bands, barrier)."""
import json, sys, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, FixedLocator

OUT = sys.argv[1] if len(sys.argv) > 1 else "hero_iter.png"

D = json.load(open("weekly_data.json"))
W = D["weeks"]
xs = np.array([w["tokens"] for w in W], float)
prs = np.array([w["prs"] for w in W], float)
a, b = D["jellyfish_curve"]["a"], D["jellyfish_curve"]["b"]
curve = lambda x: a*np.log(x) + b

# --- palette sampled to match the Jellyfish source ---
NAVY   = "#201a4d"
ORANGE = "#ff5a36"
PURPLE = "#7b3fd4"          # crowd + solo dots (same species)
GREY   = "#8a8a98"
GRID   = "#ededf2"
BAND_INT = "#ece4fb"        # interactive coding
BAND_AUT = "#b393ea"        # autonomous agents
BAND_ORC = "#7c3aed"        # agent orchestration
XMAX = 1.25e9
tokfmt = FuncFormatter(lambda v,_: "0" if v==0 else (f"{v/1e6:.0f}M" if v < 1e9 else f"{v/1e9:.1f}B"))

fig = plt.figure(figsize=(11, 8))
fig.patch.set_facecolor("white")
gs = fig.add_gridspec(3, 1, height_ratios=[2.35, 1.25, 0.30], hspace=0.10,
                      left=0.085, right=0.965, top=0.80, bottom=0.10)
ax_top  = fig.add_subplot(gs[0])                    # solo dev (broken-out scale)
ax_bot  = fig.add_subplot(gs[1], sharex=ax_top)     # the crowd (Jellyfish, intact)
ax_band = fig.add_subplot(gs[2], sharex=ax_top)     # regime bands strip
ax_top.set_xlim(0, XMAX)

# ================= BOTTOM: the Jellyfish chart, intact =================
xc = np.linspace(3.2e7, 5e8, 300)
ax_bot.plot(xc, curve(xc), color=ORANGE, lw=3.0, zorder=4, solid_capstyle="round")
xc2 = np.linspace(5e8, XMAX, 120)
ax_bot.plot(xc2, curve(xc2), color=ORANGE, lw=2.0, ls=(0,(2,2.5)), alpha=0.55, zorder=4)
xt = np.linspace(3.4e7, 4.6e8, 44)
yt = curve(xt) + 0.055*np.sin(np.arange(44)*2.3) + 0.035*np.cos(np.arange(44)*5.1)
ax_bot.scatter(xt, yt, s=34, color=PURPLE, alpha=0.9, zorder=5, edgecolor="none")
ax_bot.scatter([3.4e8],[4.15], s=34, color=PURPLE, alpha=0.9, zorder=5)
ax_bot.text(4.7e8, 1.15, "1,000,000 developers", fontsize=10, color=GREY, ha="left", style="italic")
ax_bot.set_ylim(0, 4.6)
ax_bot.set_yticks([0, 2, 4])

# ================= TOP: one solo developer, broken-out scale =================
for x, y in zip(xs, prs):
    ax_top.scatter([x],[y], s=470, color=PURPLE, alpha=0.12, zorder=5, edgecolor="none")
ax_top.scatter(xs, prs, s=150, color=PURPLE, zorder=6, edgecolor="white", lw=1.5)
ax_top.set_ylim(4.6, 40)
ax_top.set_yticks([10, 20, 30, 40])
ax_top.annotate("one solo developer, after hours",
                xy=(7.55e8, 36), xytext=(3.4e8, 38.4),
                fontsize=11.5, color=NAVY, ha="center", fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.5,
                                connectionstyle="arc3,rad=-0.12"))
ax_top.text(3.4e8, 34.4, "no standups · no handoffs · no coordination tax",
            fontsize=9.5, color=GREY, ha="center", style="italic")

# ---- the break marks + the Coordination Tax label ----
for ax, y in ((ax_top, 0), (ax_bot, 1)):
    ax.spines["bottom" if ax is ax_top else "top"].set_visible(False)
kw = dict(marker=[(-1,-0.6),(1,0.6)], markersize=11, ls="none", color=NAVY, mec=NAVY, mew=1.4, clip_on=False)
ax_top.plot([0,1],[0,0], transform=ax_top.transAxes, **kw)
ax_bot.plot([0,1],[1,1], transform=ax_bot.transAxes, **kw)
ax_top.tick_params(bottom=False)
ax_bot.tick_params(bottom=False)
plt.setp(ax_top.get_xticklabels(), visible=False)
plt.setp(ax_bot.get_xticklabels(), visible=False)
# the break = the barrier (pill sits just inside the top panel, above the break)
ax_top.text(0.5, 0.02, "THE COORDINATION TAX  —  the gap the plateau hides",
            transform=ax_top.transAxes, ha="center", va="bottom", fontsize=10.5,
            fontweight="bold", color=ORANGE, zorder=10,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=ORANGE, lw=1.4))

# ================= AGENTIC BARRIER across both data panels =================
for ax in (ax_top, ax_bot):
    ax.axvline(5e7, ls=(0,(6,4)), color=NAVY, lw=1.3, zorder=3, alpha=0.8)
ax_top.text(6e7, 38.5, "AGENTIC BARRIER", rotation=90, va="top", ha="left",
            fontsize=8, color=NAVY, fontweight="bold")

# ================= BAND STRIP =================
ax_band.set_ylim(0, 1)
for x0, x1, lbl, c, tc, fsz in [(0, 5e7, "", BAND_INT, NAVY, 6.0),
                                (5e7, 2e8, "Autonomous agents", BAND_AUT, "white", 8.5),
                                (2e8, 5e8, "Agent orchestration", BAND_ORC, "white", 8.5)]:
    ax_band.axvspan(x0, x1, color=c, zorder=1)
    if lbl:
        ax_band.text((x0+x1)/2, 0.5, lbl, ha="center", va="center",
                     fontsize=fsz, color=tc, fontweight="bold")
# beyond the source's measured range — where the solo dev lives
ax_band.axvspan(5e8, XMAX, color="#f2f2f6", zorder=1)
ax_band.text((5e8+XMAX)/2, 0.5, "beyond Jellyfish's measured range",
             ha="center", va="center", fontsize=8, color=GREY, style="italic")
ax_band.set_yticks([])

# ================= cosmetics to match source =================
for ax in (ax_top, ax_bot):
    ax.grid(True, axis="y", color=GRID, lw=0.8)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.spines["left"].set_color("#cfcfd8")
for s in ("top","right","left","bottom"): ax_band.spines[s].set_visible(False)
ax_band.tick_params(length=0)
ax_band.xaxis.set_major_locator(FixedLocator([5e7, 2e8, 5e8, 1e9]))
ax_band.xaxis.set_major_formatter(tokfmt)
ax_band.set_xlabel("Tokens per dev per week", fontsize=11, color=NAVY, labelpad=6)
fig.text(0.028, 0.52, "Merged PRs per dev per week", rotation=90,
         va="center", ha="center", fontsize=11, color=NAVY)

# ================= headline / branding =================
fig.text(0.085, 0.945, "The Real AI Development Barrier:", fontsize=20,
         fontweight="bold", color=NAVY, ha="left")
fig.text(0.085, 0.895, "The Coordination Tax", fontsize=20,
         fontweight="bold", color=ORANGE, ha="left")
fig.text(0.085, 0.855, "March – July 2026   |   1,000,000 developers, and one working solo",
         fontsize=10.5, color=GREY, ha="left")
fig.text(0.085, 0.035, "Source: Jellyfish Research (baseline curve & bands)  ·  Skillenai analysis (solo-developer overlay, Jun–Jul 2026)",
         fontsize=8, color="#a2a2ae", ha="left")

fig.savefig(OUT, dpi=140, facecolor="white")
print("wrote", OUT)
