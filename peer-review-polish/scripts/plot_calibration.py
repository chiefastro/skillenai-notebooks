import os
DATA = os.environ.get("PRP_DATA", "_data")   # collected notes; override with PRP_DATA
OUT  = os.environ.get("PRP_OUT", ".")       # figures/CSVs written here
#!/usr/bin/env python3
import json,collections,numpy as np,matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
W=OUT
BLUE="#2a78d6"; ORANGE="#eb6834"; AQUA="#1baf7a"; SURF="#fcfcfb"
INK="#0b0b0b"; SEC="#52514e"; MUTED="#898781"; GRID="#e1e0d9"; BASE="#c3c2b7"
plt.rcParams.update({"font.family":"sans-serif",
 "font.sans-serif":["Helvetica Neue","Helvetica","Arial","DejaVu Sans"],
 "figure.facecolor":SURF,"axes.facecolor":SURF,"savefig.facecolor":SURF,
 "text.color":INK,"xtick.color":MUTED,"ytick.color":MUTED,
 "axes.edgecolor":BASE,"axes.linewidth":0.8})
R=[json.loads(l) for l in open(f"{DATA}/calib_judgments.jsonl")]
by=collections.defaultdict(list)
for r in R: by[r["label"]].append(r["score"])
J=[json.loads(l) for l in open(f"{DATA}/judgments.jsonl")]
rev=collections.defaultdict(list)
for j in J: rev[j["lab"]].append(j["score"])

fig,ax=plt.subplots(figsize=(11.5,6.6),dpi=150)
ax.set_facecolor(SURF)
for s in ("top","right"): ax.spines[s].set_visible(False)
ax.spines["left"].set_color(BASE); ax.spines["bottom"].set_color(BASE)
ax.grid(axis="y",color=GRID,linewidth=0.8,zorder=0); ax.set_axisbelow(True)
ax.tick_params(length=0,labelsize=10.5)
bins=np.arange(0,105,5)
sets=[("Known human (published <= 2021)",by["human_pre2022"],AQUA),
      ("Mainstream 2026 publications",by["mainstream_2026"],ORANGE),
      ("Known content-farm output",by["slop_2026"],BLUE)]
ymax=0
for lab,v,c in sets:
    h,_=np.histogram(v,bins=bins)
    ymax=max(ymax,100*h.max()/len(v))
    ax.plot(bins[:-1]+2.5,100*h/len(v),color=c,linewidth=2.6,zorder=5)
    ax.fill_between(bins[:-1]+2.5,0,100*h/len(v),color=c,alpha=0.16,zorder=3)
ax.annotate("Known human\nmean 12.9",(6,ymax*0.62),fontsize=11,color=AQUA,fontweight="bold",linespacing=1.35)
ax.annotate("Mainstream 2026\nmean 57.6",(46,ymax*0.24),fontsize=11,color=ORANGE,fontweight="bold",ha="center",linespacing=1.35)
ax.annotate("Content farms\nmean 96.1",(78,ymax*0.72),fontsize=11,color=BLUE,fontweight="bold",ha="center",linespacing=1.35)
for lab,c,x in (("ICLR 2024 reviews: mean 18.6",SEC,18.6),("ICLR 2026 reviews: mean 37.5",SEC,37.5)):
    ax.axvline(x,color=MUTED,linewidth=1,linestyle="-",alpha=0.55,zorder=2)
ax.annotate("ICLR 2024\nreviews (18.6)",(19.5,ymax*1.02),fontsize=9.5,color=SEC,linespacing=1.3)
ax.annotate("ICLR 2026\nreviews (37.5)",(38.5,ymax*1.02),fontsize=9.5,color=SEC,linespacing=1.3)
ax.set_xlim(0,100); ax.set_ylim(0,ymax*1.18)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v,_: f"{v:.0f}%"))
ax.set_xlabel("Blind judge score: likelihood the text was machine-generated",fontsize=11,color=SEC,labelpad=8)
ax.set_ylabel("% of that set",fontsize=11,color=SEC,labelpad=10)
ax.set_title("The judge separates known machine content from known human writing at AUC 0.998",
             fontsize=15,color=INK,loc="left",pad=18,fontweight="bold")
fig.text(0.008,0.015,"956 blog articles scored blind by the same judge used on peer reviews. Known human = published on or before 2021-12-31, before ChatGPT existed. "
 "Known content-farm\noutput = 332 domains from a documented synthetic-persona network. Peer reviews of both years sit far below the machine signature; "
 "the vertical lines mark their means.",fontsize=8.5,color=MUTED,linespacing=1.5)
fig.tight_layout(rect=[0,0.055,1,1]); fig.savefig(f"{W}/05_judge_calibration.png",dpi=150,bbox_inches="tight")
print("05_judge_calibration.png")
