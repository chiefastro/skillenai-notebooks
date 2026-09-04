#!/usr/bin/env python3
"""Charts for 'The Coordination Tax' — PM-to-engineer ratios vs span of control.
Data: Live Data (workforce.ai) current headcount + Skillenai job postings, 2026-07.
Skillenai palette: cyan -> violet."""
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

CYAN, BLUE, VIOLET, PURPLE, INK, GREY = "#06b6d4", "#3b82f6", "#8b5cf6", "#a855f7", "#0f172a", "#94a3b8"
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.edgecolor": "#cbd5e1",
                     "axes.linewidth": 0.8, "figure.dpi": 150, "savefig.dpi": 150,
                     "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK})

def grad(n):
    from matplotlib.colors import LinearSegmentedColormap
    cm = LinearSegmentedColormap.from_list("skn", [CYAN, BLUE, VIOLET, PURPLE])
    return [cm(i/(max(n-1,1))) for i in range(n)]

def header(fig, main, sub):
    fig.text(0.015, 0.965, main, fontsize=13.5, fontweight="bold", color=INK, va="top")
    fig.text(0.015, 0.905, sub, fontsize=9.3, color="#475569", va="top")

# ---------- Chart 1: span of control (engineers per manager), all companies ----------
span = [("Mastercard",3.9),("Amex",6.6),("Apple",6.7),("Meta",7.2),("Stripe",7.8),
        ("Google",7.9),("Amazon",8.5),("Uber",8.6),("Walmart",9.6),
        ("Microsoft",13.8),("Anthropic",16.4),("OpenAI",19.4)]
span.sort(key=lambda x: x[1])
names=[x[0] for x in span]; vals=[x[1] for x in span]
fig,ax=plt.subplots(figsize=(10,6.4))
ax.axvspan(6,9,color=CYAN,alpha=0.10,zorder=0)
ax.text(7.5,len(names)-0.4,"typical span\n(~6–9)",ha="center",va="top",fontsize=8.5,color="#0e7490")
bars=ax.barh(names,vals,color=grad(len(names)),zorder=3,height=0.68)
for b,v in zip(bars,vals):
    ax.text(v+0.25,b.get_y()+b.get_height()/2,f"{v:.1f}",va="center",fontsize=9,color=INK)
ax.set_xlabel("Engineers per manager  (engineering function, current headcount)")
header(fig,"No one runs engineers unmanaged: span of control is nearly invariant",
       "Even the flattest AI labs sit at ~16–19 engineers per manager — not the 60–90 their PM ratio implies.")
ax.set_xlim(0,21); ax.spines[["top","right"]].set_visible(False)
plt.tight_layout(rect=[0,0,1,0.86]); plt.savefig("01_span_of_control.png",bbox_inches="tight"); plt.close()

# ---------- Chart 2: dumbbell eng-per-PM vs eng-per-manager ----------
# eng per PM: clean SWE-title/clean-PM (conventional); AI labs function-based (MTS caveat, capped display)
dumb = [("Amazon",4.8,8.5),("Mastercard",3.1,3.9),("Uber",8.1,8.6),("Google",11.2,7.9),
        ("Meta",11.4,7.2),("Stripe",14.3,7.8),("Apple",14.6,6.7),
        ("OpenAI",64.0,19.4),("Anthropic",91.0,16.4)]
dumb.sort(key=lambda x:x[1])
names=[x[0] for x in dumb]; pm=[x[1] for x in dumb]; mgr=[x[2] for x in dumb]
y=np.arange(len(names))
fig,ax=plt.subplots(figsize=(10,6.2))
for i in range(len(names)):
    ax.plot([mgr[i],min(pm[i],40)],[y[i],y[i]],color=GREY,lw=2,zorder=1)
    if pm[i]>40: ax.annotate("",xy=(41,y[i]),xytext=(38,y[i]),arrowprops=dict(arrowstyle="-|>",color=GREY))
ax.scatter([min(v,40) for v in pm],y,s=95,color=VIOLET,zorder=3,label="Engineers per PM")
ax.scatter(mgr,y,s=95,color=CYAN,zorder=3,label="Engineers per manager")
for i in range(len(names)):
    lab=f"{pm[i]:.0f}" if pm[i]>=20 else f"{pm[i]:.1f}"
    ax.text(min(pm[i],40)+0.7,y[i]+0.02,lab+("*" if pm[i]>40 else ""),va="center",fontsize=8,color=VIOLET)
    ax.text(mgr[i]-0.7,y[i]+0.02,f"{mgr[i]:.1f}",va="center",ha="right",fontsize=8,color="#0e7490")
ax.set_yticks(y); ax.set_yticklabels(names)
ax.set_xlim(0,44); ax.set_xlabel("Ratio (engineers per …)")
header(fig,"The PM ratio is elastic (5–91). The manager ratio is not (7–19).",
       "Same coordination work, different accounting.  *AI-lab PM ratio is function-based — they title engineers 'Member of Technical Staff'.")
ax.legend(loc="lower right",frameon=False,fontsize=9.5)
ax.spines[["top","right"]].set_visible(False)
plt.tight_layout(rect=[0,0,1,0.86]); plt.savefig("02_pm_vs_manager_dumbbell.png",bbox_inches="tight"); plt.close()

# ---------- Chart 3: coordination language in IC engineer postings ----------
phr=["navigate\nambiguity","own the\nroadmap","0-to-1\nbuilding","drive\nalignment","cross-\nfunctional"]
ai=[41.3,14.9,5.3,6.3,26.5]; amz=[21.8,8.7,0.0,1.0,23.3]; base=[12.0,10.0,1.2,3.2,22.6]
x=np.arange(len(phr)); w=0.26
fig,ax=plt.subplots(figsize=(10,5.8))
ax.bar(x-w,ai,w,label="AI labs (Anthropic, OpenAI)",color=VIOLET)
ax.bar(x,amz,w,label="Amazon (PM-rich)",color=BLUE)
ax.bar(x+w,base,w,label="Market baseline",color=CYAN)
for xi,v in zip(x-w,ai): ax.text(xi,v+0.6,f"{v:.0f}",ha="center",fontsize=8,color=INK)
ax.set_xticks(x); ax.set_xticklabels(phr,fontsize=9)
ax.set_ylabel("% of IC engineer postings mentioning")
header(fig,"Flat orgs write the coordination into the engineer's job",
       "AI-lab IC postings demand ambiguity-navigation at 3.4× and 0-to-1 building at 4.4× the market rate.")
ax.legend(frameon=False,fontsize=9.5); ax.spines[["top","right"]].set_visible(False)
ax.set_ylim(0,46)
plt.tight_layout(rect=[0,0,1,0.87]); plt.savefig("03_coordination_language.png",bbox_inches="tight"); plt.close()

# ---------- Chart 4: hiring trend (no AI break) ----------
q=["24Q1","24Q2","24Q3","24Q4","25Q1","25Q2","25Q3","25Q4","26Q1","26Q2"]
r=[6.75,10.23,8.79,8.64,7.64,10.10,8.69,7.93,8.10,8.67]
fig,ax=plt.subplots(figsize=(10,5.2))
ax.axhspan(min(r)-0.5,max(r)+0.5,color=CYAN,alpha=0.08)
ax.plot(q,r,"-o",color=VIOLET,lw=2.2,markersize=6)
for xi,v in zip(q,r): ax.text(xi,v+0.28,f"{v:.1f}",ha="center",fontsize=8,color=INK)
ax.axvline(3.5,color=GREY,ls="--",lw=1); ax.text(3.6,6.3,"ChatGPT-era\nAI coding wave →",fontsize=8,color="#475569")
ax.set_ylabel("Engineers hired per PM hired")
ax.set_ylim(5.5,11.5)
header(fig,"If AI were breaking the PM rule, it isn't showing up in hiring",
       "Big Tech + AI labs still hire ~8 engineers per PM — flat through 2026, squarely in the classic 6–10 band.")
ax.spines[["top","right"]].set_visible(False)
plt.tight_layout(rect=[0,0,1,0.87]); plt.savefig("04_hiring_trend.png",bbox_inches="tight"); plt.close()
print("charts written")
