#!/usr/bin/env python3
"""
Regenerates every figure and table in this analysis.

INPUT (not committed - contains personal data):
  current_roles2.tsv  -- one row per unique LinkedIn profile:
                         profile_id, company_id, company_name, title, title_src, country, city
  demand_side.json    -- role-bucket counts from the Skillenai jobs index

Both are produced by the extraction step documented in README.md ("Reproducing").
"""
import collections, csv, json, math, os, sys, re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

SRC = os.environ.get("ROLES_TSV", "current_roles2.tsv")
DEMAND = os.environ.get("DEMAND_JSON", "demand_side.json")
OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- palette
# dataviz reference palette, light mode, categorical slots 1-5 (validated:
# adjacent CVD dE 9.1, normal-vision dE 19.6; contrast WARN relieved by direct labels)
C = {"Data Engineering": "#2a78d6", "Analytics Engineering": "#eb6834",
     "Data Science": "#1baf7a", "Analytics / BI": "#eda100",
     "ML / AI Engineering": "#e87ba4"}
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e6e5e1"
ORDER = ["Data Engineering", "Analytics Engineering", "Data Science",
         "Analytics / BI", "ML / AI Engineering"]

plt.rcParams.update({
    "font.family": "DejaVu Sans", "figure.facecolor": "#fcfcfb",
    "axes.facecolor": "#fcfcfb", "axes.edgecolor": GRID, "axes.labelcolor": INK2,
    "text.color": INK, "xtick.color": INK2, "ytick.color": INK2,
    "axes.spines.top": False, "axes.spines.right": False, "font.size": 11,
})

def wilson(k, n, z=1.96):
    """95% Wilson score interval for a proportion."""
    if n == 0: return (0.0, 0.0)
    p = k / n; d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d
    h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return (max(0.0, c-h), min(1.0, c+h))

# ---------------------------------------------------------------- classify
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from classify import classify as cl

tech = collections.Counter()
data = collections.defaultdict(collections.Counter)
with open(SRC) as f:
    f.readline()
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) < 7: continue
        k = p[1] if p[1] else "name:" + p[2].strip().lower()
        tech[k] += 1
        b = cl(p[3].strip())
        if b: data[k][b] += 1

TOTAL_TECH = sum(tech.values())
NAT = collections.Counter()
for d in data.values(): NAT.update(d)
TOTAL_DATA = sum(NAT.values())
print(f"tech profiles {TOTAL_TECH:,} | data-role profiles {TOTAL_DATA:,} "
      f"({100*TOTAL_DATA/TOTAL_TECH:.1f}%) | companies {len(tech):,}")

# ------------------------------------------------- table 1: size bands
BANDS = [(1,4,"10-40"),(5,9,"50-90"),(10,24,"100-240"),(25,49,"250-490"),
         (50,99,"500-990"),(100,249,"1k-2.5k"),(250,999,"2.5k-10k"),(1000,10**9,"10k+")]
rows = []
for lo, hi, lbl in BANDS:
    ks = [k for k, v in tech.items() if lo <= v <= hi]
    t = sum(tech[k] for k in ks)
    d = collections.Counter()
    for k in ks: d.update(data[k])
    tot = sum(d.values())
    if not tot: continue
    clo, chi = wilson(tot, t)
    rows.append({"band": lbl, "companies": len(ks), "tech_obs": t, "data_obs": tot,
                 "data_share": tot/t, "ci_lo": clo, "ci_hi": chi,
                 **{b: d[b]/tot for b in ORDER}, **{b+"_n": d[b] for b in ORDER}})
with open(f"{OUT}/size_band_table.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

# ------------------------------------------------- fig 1: flat ratio
fig, ax = plt.subplots(figsize=(9.5, 5.0))
x = range(len(rows))
vals = [r["data_share"]*100 for r in rows]
err = [[ (r["data_share"]-r["ci_lo"])*100 for r in rows],
       [ (r["ci_hi"]-r["data_share"])*100 for r in rows]]
ax.bar(x, vals, color="#2a78d6", width=0.62, zorder=3)
ax.errorbar(x, vals, yerr=err, fmt="none", ecolor=INK2, elinewidth=1.4, capsize=4, zorder=4)
overall = 100*TOTAL_DATA/TOTAL_TECH
ax.axhline(overall, color="#e34948", lw=2, ls="--", zorder=5)
ax.text(len(rows)-0.4, overall+0.55, f"overall {overall:.1f}%", color="#e34948",
        ha="right", fontsize=10, fontweight="bold")
for i, v in enumerate(vals):
    ax.text(i, v+1.25, f"{v:.1f}%", ha="center", fontsize=10, color=INK, fontweight="bold")
ax.set_xticks(list(x)); ax.set_xticklabels([r["band"] for r in rows])
ax.set_xlabel("Estimated tech-org size (people)")
ax.set_ylabel("Data roles as % of tech org")
ax.set_ylim(0, 17); ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))
ax.grid(axis="y", color=GRID, zorder=0)
ax.set_title("A data team is ~1 in 9 of the tech org — at every company size",
             fontsize=14, fontweight="bold", pad=14, loc="left")
ax.text(0, 1.015, "Bars show 95% confidence intervals. 188,361 US companies.",
        transform=ax.transAxes, fontsize=9.5, color=INK2)
fig.tight_layout(); fig.savefig(f"{OUT}/01_data_share_by_size.png", dpi=150); plt.close(fig)

# ------------------------------------------------- fig 2: mix shift
fig, ax = plt.subplots(figsize=(9.5, 5.4))
bottom = [0.0]*len(rows)
for b in ORDER:
    vals = [r[b]*100 for r in rows]
    ax.bar(x, vals, bottom=bottom, color=C[b], width=0.62, label=b,
           edgecolor="#fcfcfb", linewidth=2, zorder=3)
    for i, (v, bo) in enumerate(zip(vals, bottom)):
        if v >= 6:
            ax.text(i, bo+v/2, f"{v:.0f}", ha="center", va="center",
                    fontsize=9.5, color="#ffffff", fontweight="bold")
    bottom = [bo+v for bo, v in zip(bottom, vals)]
ax.set_xticks(list(x)); ax.set_xticklabels([r["band"] for r in rows])
ax.set_xlabel("Estimated tech-org size (people)")
ax.set_ylabel("Share of the data org")
ax.set_ylim(0, 100); ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))
ax.grid(axis="y", color=GRID, zorder=0)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=3, frameon=False, fontsize=10)
ax.set_title("Small orgs staff analysts. Scale buys engineers.",
             fontsize=14, fontweight="bold", pad=14, loc="left")
ax.text(0, 1.015, "Composition of the data org by company size. Numbers are % of that org.",
        transform=ax.transAxes, fontsize=9.5, color=INK2)
fig.tight_layout(); fig.savefig(f"{OUT}/02_mix_by_size.png", dpi=150); plt.close(fig)

# ------------------------------------------------- fig 3: supply vs demand
dem = collections.Counter(json.load(open(DEMAND)))
CORE = ["Data Engineering", "Analytics Engineering", "Data Science", "Analytics / BI"]
sc = sum(NAT[k] for k in CORE); dc = sum(dem[k] for k in CORE)
sd = [{"role": k, "supply_pct": 100*NAT[k]/sc, "demand_pct": 100*dem[k]/dc,
       "supply_n": NAT[k], "demand_n": dem[k], "ratio": (dem[k]/dc)/(NAT[k]/sc)} for k in CORE]
with open(f"{OUT}/supply_vs_demand.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(sd[0].keys())); w.writeheader(); w.writerows(sd)

fig, ax = plt.subplots(figsize=(8.2, 6.6))
lim = 60
ax.plot([0, lim], [0, lim], color=INK2, lw=1.4, ls="--", zorder=2)
ax.text(lim*0.82, lim*0.82+1.6, "supply = demand", color=INK2, fontsize=9.5, rotation=38, ha="center")
ax.fill_between([0, lim], [0, lim], [lim, lim], color="#2a78d6", alpha=0.05, zorder=1)
ax.fill_between([0, lim], [0, 0], [0, lim], color="#eb6834", alpha=0.05, zorder=1)
ax.text(4, lim-6, "hiring runs AHEAD\nof the installed base", color="#2a78d6",
        fontsize=10.5, fontweight="bold", va="top")
ax.text(lim-4, 5, "more people than\nopen roles", color="#eb6834", fontsize=10.5,
        fontweight="bold", ha="right")
OFF = {"Data Engineering":       ((-12,  20), "right"),
       "Data Science":           (( 16, -34), "left"),
       "Analytics / BI":         ((-14,  18), "right"),
       "Analytics Engineering":  (( 16,   4), "left")}
for r in sd:
    ax.scatter(r["supply_pct"], r["demand_pct"], s=190, color=C[r["role"]],
               edgecolor="#fcfcfb", linewidth=2, zorder=5)
    off, ha = OFF[r["role"]]
    ax.annotate(f"{r['role']}\n{r['supply_pct']:.1f}% → {r['demand_pct']:.1f}%  ({r['ratio']:.1f}x)",
                (r["supply_pct"], r["demand_pct"]), textcoords="offset points",
                xytext=off, ha=ha, fontsize=10, color=INK, fontweight="bold", zorder=6)
ax.set_xlim(0, lim); ax.set_ylim(0, lim)
ax.set_xlabel("Share of people currently in the role  (supply)")
ax.set_ylabel("Share of open postings  (demand)")
ax.xaxis.set_major_formatter(PercentFormatter(decimals=0)); ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))
ax.grid(color=GRID, zorder=0)
ax.set_title("Analytics Engineering is the one role the market wants\nmore of than exists",
             fontsize=14, fontweight="bold", pad=14, loc="left")
fig.tight_layout(); fig.savefig(f"{OUT}/03_supply_vs_demand.png", dpi=150); plt.close(fig)

# ------------------------------------------------- national mix csv
with open(f"{OUT}/national_role_mix.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["role", "profiles", "pct_of_data_org"])
    for b, n in NAT.most_common(): w.writerow([b, n, round(100*n/TOTAL_DATA, 2)])

print("figures + csvs written to", OUT)
for r in rows:
    print(f"  {r['band']:>9s} share={100*r['data_share']:5.1f}% "
          f"DE={100*r['Data Engineering']:4.1f}% BI={100*r['Analytics / BI']:4.1f}%")
