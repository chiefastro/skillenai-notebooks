import sys, json; sys.path.insert(0,".")
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from brand import *

df=pd.read_parquet("clean3.parquet"); keep=json.load(open("keep.json"))["keep"]
d=df[df.family.isin(keep)]
NICE={"ml engineer":"ML Engineer","ai engineer":"AI Engineer","software engineer":"Software Engineer",
 "research scientist":"Research Scientist","product engineer":"Product Engineer","backend engineer":"Backend Engineer",
 "frontend engineer":"Frontend Engineer","infrastructure engineer":"Infrastructure Engineer",
 "security engineer":"Security Engineer","product manager":"Product Manager","platform engineer":"Platform Engineer",
 "site reliability engineer":"Site Reliability Engineer","full stack engineer":"Full Stack Engineer",
 "product designer":"Product Designer","data scientist":"Data Scientist","embedded software engineer":"Embedded SW Engineer",
 "devsecops engineer":"DevSecOps Engineer","devops engineer":"DevOps Engineer","program manager":"Program Manager",
 "cloud engineer":"Cloud Engineer","data engineer":"Data Engineer","analytics engineer":"Analytics Engineer",
 "systems engineer":"Systems Engineer","test engineer":"Test Engineer","data analyst":"Data Analyst",
 "business analyst":"Business Analyst","it specialist":"IT Specialist","software engineer in test":"SW Engineer in Test"}
LEVELS=["Entry","Mid","Senior","Staff+"]
med=lambda f,lv: d[(d.family==f)&(d.level==lv)]["mid"].median()
cnt=lambda f,lv: int(((d.family==f)&(d.level==lv)).sum())
order=sorted(keep,key=lambda f:-med(f,"Senior"))
SRC=("Source: Skillenai labor-market index (prod-enriched-jobs) · 31,738 US postings with a structured USD salary range, 2026.\n"
     "Advertised base-range midpoint; excludes equity and bonus. Role families exclude any title where one employer holds more\n"
     "than 25% of the senior rung, or where fewer than 10 employers post it. Management-titled rows are reported separately.")

# ---------------- FIG 1 ----------------
nf=len(order); h=0.80/4
fig,ax=plt.subplots(figsize=(13.2,0.42*nf+1.9))
yt=[]
for i,f in enumerate(order):
    base=nf-i; yt.append(base)
    for j,lv in enumerate(LEVELS):
        s=d[(d.family==f)&(d.level==lv)]["mid"].dropna().values
        y=base-(j-1.5)*h
        if len(s)<25: continue
        ax.boxplot([s],positions=[y],vert=False,widths=h*0.74,patch_artist=True,
            showfliers=False,whis=(10,90),medianprops=dict(color="white",lw=1.4),
            boxprops=dict(facecolor=RUNG[j],edgecolor=BG,lw=1.0),
            whiskerprops=dict(color=RUNG[j],lw=1.0),capprops=dict(color=RUNG[j],lw=1.0))
ax.set_yticks(yt); ax.set_yticklabels([NICE[f] for f in order],fontsize=9.6)
ax.set_ylim(0.35,nf+0.65); ax.set_xlim(50000,362000)
ax.xaxis.set_major_formatter(K)
ax.set_xlabel("Advertised base-range midpoint (US postings, USD)",fontsize=9.6)
tidy(ax)
sw=med("software engineer","Staff+")
ax.axvline(sw,color=VIOLET,lw=1.3,ls=(0,(4,3)),zorder=2)
ax.text(sw+3500,nf+0.30,f"Staff+ Software Engineer  ${sw/1000:,.0f}K",color=VIOLET,fontsize=8.8,
        weight="semibold",va="center")
ax.legend([plt.Rectangle((0,0),1,1,fc=c) for c in RUNG],LEVELS,loc="lower right",
          fontsize=9.2,ncol=4,handlelength=1.5,columnspacing=1.2,title="Seniority rung",title_fontsize=9.2)
top,bot=layout(fig,header_in=1.05,footer_in=0.80)
header(fig,"What tech roles actually pay in 2026, rung by rung",
  "Median advertised pay for 28 role families across four seniority rungs. Boxes span the interquartile range,\n"
  "whiskers the 10th to 90th percentile. Cells with fewer than 25 postings are omitted. Ordered by senior-rung median.",
  y=0.995,dy=0.026)
footer(fig,SRC,y=bot-0.012); stamp(fig,x=0.905,y=bot-0.052,h=0.026)
save_exact(fig,"01_pay_by_role_and_level.png")

# ---------------- FIG 2 ----------------
best=max(med(f,"Senior") for f in keep)
ref=max(keep,key=lambda f:med(f,"Senior"))     # the benchmark role itself: switch gain is 0 by construction
rows=[(f,med(f,"Senior"),med(f,"Staff+")-med(f,"Senior"),best-med(f,"Senior"))
      for f in keep if cnt(f,"Staff+")>=25 and f!=ref]
rows.sort(key=lambda r:-r[1])
fig,ax=plt.subplots(figsize=(11.6,0.40*len(rows)+1.9))
y=np.arange(len(rows))[::-1]; bw=0.36
ax.barh(y+bw/2+0.02,[r[2] for r in rows],height=bw,color=CAT2[0],
        label="Promote one rung, same role (Senior to Staff+)")
ax.barh(y-bw/2-0.02,[r[3] for r in rows],height=bw,color=CAT2[1],
        label="Switch to the best-paying role, same rung")
for i,r in zip(y,rows):
    ax.text(max(r[2],0)+1500,i+bw/2+0.02,f"+${r[2]/1000:,.0f}K",va="center",fontsize=8.0,color=INK)
    ax.text(max(r[3],0)+1500,i-bw/2-0.02,f"+${r[3]/1000:,.0f}K",va="center",fontsize=8.0,color=INK)
ax.set_yticks(y); ax.set_yticklabels([f"{NICE[r[0]]}   ${r[1]/1000:,.0f}K" for r in rows],fontsize=9.4)
ax.xaxis.set_major_formatter(K); ax.set_xlim(0,104000); ax.set_ylim(-0.8,len(rows)-0.2)
ax.set_xlabel("Gain in median advertised pay",fontsize=9.6)
tidy(ax)
ax.legend(loc="upper right",fontsize=9.2,handlelength=1.5,
          bbox_to_anchor=(1.0,1.012))
top,bot=layout(fig,header_in=1.05,footer_in=0.80)
header(fig,"Promote, or switch roles? It depends where you start",
  f"Roles ordered by senior-rung median (shown beside each name). {NICE[ref]} is the benchmark and omitted.\n"
  "Near the top of the board one promotion is worth more than moving to the highest-paying role.\n"
  "In the analyst tier the reverse holds, by a wide margin.",
  y=0.995,dy=0.024)
footer(fig,SRC,y=bot-0.012); stamp(fig,x=0.905,y=bot-0.052,h=0.026)
save_exact(fig,"02_promote_or_switch.png")

# ---------------- FIG 3 ----------------
dd=d[d.level.isin(LEVELS)].copy()
dd["st"]=np.where(dd.locationAdmin1.fillna("(unk)").isin(dd.locationAdmin1.value_counts().head(15).index),
                  dd.locationAdmin1.fillna("(unk)"),"other")
dd["emp2"]=np.where(dd.emp.isin(dd.emp.value_counts().head(60).index),dd.emp,"other")
dd["ly"]=np.log(dd["mid"])
spec={"Seniority rung":("ly ~ C(level)","4 levels"),"Employer":("ly ~ C(emp2)","top 60"),
      "US state":("ly ~ C(st)","top 15"),"Role label":("ly ~ C(family)",f"{len(keep)} roles")}
vals={k:(smf.ols(v,data=dd).fit().rsquared,sub) for k,(v,sub) in spec.items()}
fig,ax=plt.subplots(figsize=(8.8,4.6))
ks=list(vals); vs=[vals[k][0] for k in ks]
ax.bar(range(len(ks)),vs,color=[RUNG[2]]*3+[VIOLET],width=0.58,edgecolor=BG,lw=1.0)
for i,v in enumerate(vs):
    ax.text(i,v+0.007,f"{v:.3f}",ha="center",fontsize=11,weight="bold",color=INK)
ax.set_xticks(range(len(ks)))
ax.set_xticklabels([f"{k}\n({vals[k][1]})" for k in ks],fontsize=9.6)
ax.set_ylabel("R² — share of pay variation explained",fontsize=9.6)
ax.set_ylim(0,0.31)
ax.grid(axis="y",color=GRID,alpha=0.75,lw=0.7); ax.set_axisbelow(True)
for sp in ("top","right","left"): ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_color(GRID); ax.tick_params(length=0)
top,bot=layout(fig,header_in=1.10,footer_in=0.86)
header(fig,"Four things that set tech pay, and how much each explains",
  f"Single-factor models on log advertised pay, {len(dd):,} US postings across {len(keep)} roles.\n"
  "Of these four factors, the role label explains the least, despite having the most categories.",
  y=0.988,dy=0.052,ts=15.0)
footer(fig,"Source: Skillenai labor-market index (prod-enriched-jobs), 2026. Each bar is a separate OLS fit of log advertised\n"
           "base-range midpoint on that factor alone; R² is not additive across bars.",y=bot-0.030)
stamp(fig,x=0.878,y=bot-0.105,h=0.048)
save_exact(fig,"03_variance_explained.png")
