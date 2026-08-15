#!/usr/bin/env python3
"""
Figures for "Federal Data Science Is Two Different Jobs" — the bimodal supply-side
read (Skillenai owned talent graph, cross-validated with Live Data / workforce.ai).

Values captured from the owned-graph analysis (profiles.jsonl) + Live Data facets.
Palette: Skillenai gradient. LAB=emerald, OPM=violet, PRIVATE=cyan.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np

LAB = "#10b981"      # national-lab federal DS (builders)
OPM = "#7c3aed"      # OPM civil-service federal DS (analysts)
PRIV = "#06b6d4"     # private big-tech DS
RED = "#e11d48"
INK = "#1e293b"; GRID = "#e2e8f0"; MUTE = "#94a3b8"

plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.edgecolor":GRID,"axes.linewidth":1.0,"text.color":INK,"axes.labelcolor":INK,
    "xtick.color":INK,"ytick.color":INK})
SRC = "Source: Skillenai owned talent graph (LinkedIn profiles) + Live Data (workforce.ai), Aug 2026"
def brand(fig,y=0.01):
    fig.text(0.008,y,"Skillenai",fontsize=11,fontweight="bold",color=OPM)
    fig.text(0.076,y,"talent graph",fontsize=10,color=MUTE)

# ---------------------------------------------------------------------------
# Fig 1 (COVER) — Two kinds of federal DS: labs build, agencies analyze
# ---------------------------------------------------------------------------
cohorts = ["National-lab\nfederal DS\n(n=57)", "OPM-agency\nfederal DS\n(n=82)", "Private big-tech\nDS (n=284)"]
build   = [37, 17, 30]
analyst = [18, 30, 12]
x = np.arange(len(cohorts)); w = 0.36
fig, ax = plt.subplots(figsize=(10.5, 6.2))
b1 = ax.bar(x - w/2, build,   w, color=[LAB, OPM, PRIV], label="Builds / ML language")
b2 = ax.bar(x + w/2, analyst, w, color=[LAB, OPM, PRIV], alpha=0.42, hatch="///",
            edgecolor="white", label="Analyst / stats language")
for xi, bv, av in zip(x, build, analyst):
    ax.text(xi - w/2, bv + 0.8, f"{bv}%", ha="center", fontsize=10, fontweight="bold")
    ax.text(xi + w/2, av + 0.8, f"{av}%", ha="center", fontsize=10, color=MUTE)
ax.set_xticks(x); ax.set_xticklabels(cohorts, fontsize=10)
ax.set_ylabel("Share of the cohort whose profile text uses this language")
ax.set_ylim(0, 44)
ax.set_title("Federal data science is two different jobs\n"
             "National labs build ML like Big Tech; civil-service agencies do statistics-and-reporting",
             fontsize=13.5, fontweight="bold", loc="left")
ax.legend(handles=[Patch(facecolor=INK, label="Builds / ML language (solid)"),
                   Patch(facecolor=INK, alpha=0.42, hatch="///", label="Analyst / stats language (hatched)")],
          loc="upper right", frameon=False, fontsize=9.5)
ax.grid(axis="y", color=GRID); ax.set_axisbelow(True)
for s in ("top","right"): ax.spines[s].set_visible(False)
fig.text(0.99, 0.012, SRC, fontsize=7.5, color=MUTE, ha="right")
brand(fig)
fig.tight_layout(rect=[0,0.04,1,1])
fig.savefig("01_bimodal_build_analyst.png", bbox_inches="tight"); plt.close(fig)

# ---------------------------------------------------------------------------
# Fig 2 — The frontier-tech door is shut for BOTH kinds of federal DS
# ---------------------------------------------------------------------------
labels = ["National-lab\nfederal DS", "OPM-agency\nfederal DS", "Private big-tech\nDS"]
feed_bt = [0, 0, 25]   # Big Tech share of feeders
exit_bt = [0, 0, 44]   # Big Tech share of exits
x = np.arange(len(labels)); w = 0.36
fig, ax = plt.subplots(figsize=(10.5, 6.0))
ax.bar(x - w/2, feed_bt, w, color=[LAB, OPM, PRIV], label="Big Tech = share of feeders")
ax.bar(x + w/2, exit_bt, w, color=[LAB, OPM, PRIV], alpha=0.45, hatch="///", edgecolor="white")
for xi, fv, ev in zip(x, feed_bt, exit_bt):
    ax.text(xi - w/2, fv + 0.8, f"{fv}%", ha="center", fontsize=11, fontweight="bold",
            color=RED if fv == 0 else INK)
    ax.text(xi + w/2, ev + 0.8, f"{ev}%", ha="center", fontsize=11, fontweight="bold",
            color=RED if ev == 0 else MUTE)
ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=10.5)
ax.set_ylabel("Big Tech / frontier-AI share")
ax.set_ylim(0, 50)
ax.set_title("The frontier-tech door is shut for BOTH kinds of federal data scientist\n"
             "Big Tech feeds and takes ~0% of federal DS (either mode) — but 25–44% of private DS",
             fontsize=13, fontweight="bold", loc="left")
ax.legend(handles=[Patch(facecolor=INK, label="Big Tech share of feeders (solid)"),
                   Patch(facecolor=INK, alpha=0.45, hatch="///", label="Big Tech share of exits (hatched)")],
          loc="upper left", frameon=False, fontsize=9.5)
ax.grid(axis="y", color=GRID); ax.set_axisbelow(True)
for s in ("top","right"): ax.spines[s].set_visible(False)
ax.text(0.5, 6.5, "≈ 0", fontsize=9, color=RED, ha="center", style="italic")
fig.text(0.99, 0.012, SRC + " · Live Data corroborates: 1% of federal feeders, 0.3% of exits", fontsize=7.2, color=MUTE, ha="right")
brand(fig)
fig.tight_layout(rect=[0,0.04,1,1])
fig.savefig("02_frontier_door.png", bbox_inches="tight"); plt.close(fig)

# ---------------------------------------------------------------------------
# Fig 3 — Different people (Live Data education field, the OPM/health mode)
# ---------------------------------------------------------------------------
fields = ["Statistics","Computer Science","Economics","Data Science","Mathematics",
          "Biostatistics","Epidemiology","Psychology","Physics","Business Analytics"]
fed = [4.4,6.7,4.4,4.8,4.0,3.2,5.2,3.6,2.4,2.0]
priv = [9.4,7.2,5.3,4.7,4.1,1.5,0.3,0.8,2.3,3.8]
order = np.argsort([f-p for f,p in zip(fed,priv)])
fields=[fields[i] for i in order]; fed=[fed[i] for i in order]; priv=[priv[i] for i in order]
y = np.arange(len(fields)); h = 0.4
fig, ax = plt.subplots(figsize=(10, 6.2))
ax.barh(y+h/2, fed, h, color=OPM, label="Federal DS (Live Data, N=252)")
ax.barh(y-h/2, priv, h, color=PRIV, label="Private-tech DS (N=7,683)")
for yi,(f,p) in enumerate(zip(fed,priv)):
    ax.text(f+0.12, yi+h/2, f"{f:.1f}%", va="center", fontsize=8, color=OPM)
    ax.text(p+0.12, yi-h/2, f"{p:.1f}%", va="center", fontsize=8, color=PRIV)
ax.set_yticks(y); ax.set_yticklabels(fields)
ax.set_xlabel("Share holding a degree in this field")
ax.set_xlim(0,10.6)
ax.set_title("Different people — the health-agency mode\n"
             "Federal DS over-index on epidemiology & psychology; private DS on statistics",
             fontsize=12.5, fontweight="bold", loc="left")
ax.legend(loc="center right", bbox_to_anchor=(1.0,0.5), frameon=False)
ax.grid(axis="x", color=GRID); ax.set_axisbelow(True)
for s in ("top","right"): ax.spines[s].set_visible(False)
fig.text(0.99, 0.012, "Source: Live Data (workforce.ai) education facets, 2026", fontsize=7.5, color=MUTE, ha="right")
brand(fig)
fig.tight_layout(rect=[0,0.04,1,1])
fig.savefig("03_education_funnels.png", bbox_inches="tight"); plt.close(fig)

print("wrote 01_bimodal_build_analyst.png, 02_frontier_door.png, 03_education_funnels.png")
