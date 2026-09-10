import os
DATA = os.environ.get("PRP_DATA", "_data")   # collected notes; override with PRP_DATA
OUT  = os.environ.get("PRP_OUT", ".")       # figures/CSVs written here
#!/usr/bin/env python3
import matplotlib, numpy as np
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
W=OUT
BLUE="#2a78d6"; ORANGE="#eb6834"; AQUA="#1baf7a"; SURF="#fcfcfb"
INK="#0b0b0b"; SEC="#52514e"; MUTED="#898781"; GRID="#e1e0d9"; BASE="#c3c2b7"
plt.rcParams.update({"font.family":"sans-serif",
 "font.sans-serif":["Helvetica Neue","Helvetica","Arial","DejaVu Sans"],
 "figure.facecolor":SURF,"axes.facecolor":SURF,"savefig.facecolor":SURF,
 "text.color":INK,"xtick.color":MUTED,"ytick.color":MUTED,
 "axes.edgecolor":BASE,"axes.linewidth":0.8})
def style(ax,axis="y"):
    ax.set_facecolor(SURF)
    for s in ("top","right"): ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(BASE); ax.spines["bottom"].set_color(BASE)
    ax.grid(axis=axis,color=GRID,linewidth=0.8,zorder=0); ax.set_axisbelow(True)
    ax.tick_params(length=0,labelsize=10.5)
pct=FuncFormatter(lambda v,_: f"{v:.0f}%")

# ---- 01 HERO: em dash by venue-year ----
S={"ICLR":([2024,2025,2026],[6.1,12.2,36.5],BLUE,2.8),
   "NeurIPS":([2023,2024,2025],[5.2,6.4,22.4],ORANGE,2.8),
   "COLM":([2025,2026],[20.1,27.2],MUTED,1.6),
   "MIDL":([2025,2026],[20.3,31.0],MUTED,1.6)}
fig,ax=plt.subplots(figsize=(11.5,6.6),dpi=150); style(ax)
for k,(x,y,c,lw) in S.items():
    ax.plot(x,y,color=c,linewidth=lw,marker="o",markersize=7,markerfacecolor=c,
            markeredgecolor=SURF,markeredgewidth=2,zorder=5 if lw>2 else 3,
            alpha=1 if lw>2 else 0.6)
    ax.annotate(f"{k}  {y[-1]:.1f}%",(x[-1],y[-1]),textcoords="offset points",
                xytext=(10,0),va="center",fontsize=11.5 if lw>2 else 10,
                color=c if lw>2 else MUTED,fontweight="bold" if lw>2 else "normal")
ax.set_xticks([2023,2024,2025,2026]); ax.set_xlim(2022.8,2026.75); ax.set_ylim(0,41)
ax.yaxis.set_major_formatter(pct)
ax.set_ylabel("% of reviews containing an em or en dash",fontsize=11,color=SEC,labelpad=10)
ax.set_xlabel("Conference year",fontsize=11,color=SEC,labelpad=8)
ax.set_title("Peer reviews increasingly arrive with typography a plain text box cannot produce",
             fontsize=15.5,color=INK,loc="left",pad=18,fontweight="bold")
ax.annotate("6x in two years",(2025.05,26),fontsize=12,color=BLUE,fontweight="bold")
fig.text(0.008,0.015,"24,479 OpenReview official reviews of 2,000+ characters. An em dash requires a deliberate keystroke almost nobody uses mid-review, so its "
 "presence indicates text\ncomposed elsewhere and pasted in. The shift tracks calendar year across every venue measured, not any single conference.",
 fontsize=8.5,color=MUTED,linespacing=1.5)
fig.tight_layout(rect=[0,0.055,1,1]); fig.savefig(f"{W}/01_typography_by_venue.png",dpi=150,bbox_inches="tight")
print("01")

# ---- 02 THE CRUX: judge score distribution ----
bands=["0-29\nclearly human","30-49","50-69","70-84","85-100\nclearly machine"]
y24=[84.3,6.0,3.0,4.7,2.0]; y26=[53.7,13.0,11.7,18.0,3.7]
x=np.arange(len(bands)); w=0.38
fig,ax=plt.subplots(figsize=(11.5,6.4),dpi=150); style(ax)
ax.bar(x-w/2,y24,w,color=MUTED,alpha=0.55,zorder=3,label="ICLR 2024")
ax.bar(x+w/2,y26,w,color=BLUE,zorder=3,label="ICLR 2026")
for xi,(a,b) in enumerate(zip(y24,y26)):
    ax.annotate(f"{a:.0f}%",(xi-w/2,a),textcoords="offset points",xytext=(0,5),ha="center",fontsize=10,color=SEC)
    ax.annotate(f"{b:.0f}%",(xi+w/2,b),textcoords="offset points",xytext=(0,5),ha="center",fontsize=10.5,color=BLUE,fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(bands,fontsize=10.5,color=INK)
ax.set_ylim(0,95); ax.yaxis.set_major_formatter(pct)
ax.set_ylabel("% of reviews in each band",fontsize=11,color=SEC,labelpad=10)
ax.set_xlabel("Blind judge's likelihood the review was machine-drafted",fontsize=11,color=SEC,labelpad=8)
ax.set_title("Suspicion moved into the middle, not the top",fontsize=16,color=INK,loc="left",pad=18,fontweight="bold")
ax.annotate("mass moves here",(2.5,26),fontsize=11.5,color=BLUE,fontweight="bold",ha="center")
ax.annotate("but not here\n(2.0% -> 3.7%, p = 0.22)",(4,14),fontsize=10.5,color=SEC,ha="center",linespacing=1.4)
lg=ax.legend(loc="upper right",frameon=False,fontsize=11)
for t in lg.get_texts(): t.set_color(SEC)
fig.text(0.008,0.015,"899 reviews scored blind by Claude Opus 5, which was never shown the year. The judge reported keying on typography in 0.0% of cases; "
 "its stated signals were\nsubstance (69%) and structure (31%). A review drafted by a model would land in the top band. The top band did not move.",
 fontsize=8.5,color=MUTED,linespacing=1.5)
fig.tight_layout(rect=[0,0.055,1,1]); fig.savefig(f"{W}/02_polish_not_drafting.png",dpi=150,bbox_inches="tight")
print("02")

# ---- 03 what rose, what fell ----
rows=[("Any paste-typography",66.2,83.9),("Curly quotes",24.0,47.5),
      ("Em dash present",6.1,36.5),("Judge suspicion (score >=50)",9.7,33.3),
      ("Judge high-confidence (>=85)",2.0,3.7),
      ("LLM vocabulary (delve, showcase)",22.6,15.9),
      ("Non-native English markers",11.38,8.71),("\"not X but Y\" rhetoric",2.5,1.9)]
fig,ax=plt.subplots(figsize=(11.5,6.4),dpi=150)
style(ax,axis="x"); ypos=np.arange(len(rows))[::-1]
for yp,(lab,a,b) in zip(ypos,rows):
    up=b>a; c=BLUE if up else AQUA
    ax.plot([a,b],[yp,yp],color=c,linewidth=2.4,zorder=3,alpha=0.85)
    ax.scatter([a],[yp],s=52,color=MUTED,zorder=4,edgecolor=SURF,linewidth=1.5)
    ax.scatter([b],[yp],s=80,color=c,zorder=5,edgecolor=SURF,linewidth=1.5)
    # small values would collide with the axis labels; place those on the right
    right = up or b < 6
    anchor = max(a,b) if right else b
    ax.annotate(f"{b:.1f}%",(anchor,yp),textcoords="offset points",
                xytext=(12 if right else -12,0),
                va="center",ha="left" if right else "right",fontsize=10.5,color=c,fontweight="bold")
ax.set_yticks(ypos); ax.set_yticklabels([r[0] for r in rows],fontsize=11,color=INK)
ax.set_xlim(-3,95); ax.xaxis.set_major_formatter(pct)
ax.set_xlabel("% of ICLR reviews, 2024 (grey) to 2026 (coloured)",fontsize=11,color=SEC,labelpad=8)
ax.set_title("Typography rose. Every language-level signal fell.",fontsize=16,color=INK,loc="left",pad=18,fontweight="bold")
fig.text(0.008,0.015,"Blue = rose, green = fell. The evidence that reviews are machine-TOUCHED is typographic and structural. The evidence that they are machine-WRITTEN "
 "is absent:\nmodel vocabulary, model rhetoric, and the judge's high-confidence calls all move the wrong way for a drafting story.",
 fontsize=8.5,color=MUTED,linespacing=1.5)
fig.tight_layout(rect=[0,0.06,1,1]); fig.savefig(f"{W}/03_rose_and_fell.png",dpi=150,bbox_inches="tight")
print("03")

# ---- 04 ESL markers ----
fig,ax=plt.subplots(figsize=(11,6),dpi=150); style(ax)
for k,(x,y,c) in {"ICLR":([2024,2025,2026],[11.38,10.24,8.71],BLUE),
                  "NeurIPS":([2023,2024,2025],[11.13,11.82,9.84],ORANGE)}.items():
    ax.plot(x,y,color=c,linewidth=2.8,marker="o",markersize=7,markerfacecolor=c,
            markeredgecolor=SURF,markeredgewidth=2,zorder=5)
    ax.annotate(f"{k}  {y[-1]:.1f}%",(x[-1],y[-1]),textcoords="offset points",xytext=(10,0),
                va="center",fontsize=11.5,color=c,fontweight="bold")
ax.set_xticks([2023,2024,2025,2026]); ax.set_xlim(2022.8,2026.6); ax.set_ylim(7,13.5)
ax.yaxis.set_major_formatter(pct)
ax.set_ylabel("% of reviews with a non-native English marker",fontsize=11,color=SEC,labelpad=10)
ax.set_xlabel("Conference year",fontsize=11,color=SEC,labelpad=8)
ax.set_title("As polish rose, the fingerprints of non-native English receded",
             fontsize=15.5,color=INK,loc="left",pad=18,fontweight="bold")
fig.text(0.008,0.015,"High-precision markers only: subject-verb agreement slips, article omission before 'authors', determiner-count mismatch. ICLR falls 11.4% to 8.7% "
 "(z = -4.22, p = 2.4e-05).\nThis measures text, not people. Reviewers are anonymous; nothing here identifies anyone or supports a claim about any individual.",
 fontsize=8.5,color=MUTED,linespacing=1.5)
fig.tight_layout(rect=[0,0.06,1,1]); fig.savefig(f"{W}/04_esl_markers.png",dpi=150,bbox_inches="tight")
print("04")
