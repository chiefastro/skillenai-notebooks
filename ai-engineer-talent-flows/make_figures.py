"""
Figures for "Who Becomes an AI Engineer" — sourced from Skillenai's owned talent
graph (supply) and job-postings index (demand-side salary). Reads the CSVs in this
folder. See README.md for methodology and caveats.
"""
import csv, os, json
from collections import defaultdict
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.family":"DejaVu Sans",
    "axes.spines.top":False,"axes.spines.right":False,"axes.titleweight":"bold","axes.titlesize":15})
HERE=os.path.dirname(os.path.abspath(__file__))
def out(n): return os.path.join(HERE,n)
C={"AIE":"#2563eb","DS":"#dc2626","MLE":"#7c3aed","DE":"#0d9488","SWE":"#64748b",
   "grid":"#e5e7eb","ink":"#111827","base":"#94a3b8"}

def read_csv(name):
    with open(out(name)) as f: return list(csv.DictReader(f))

arr=read_csv("arrivals_by_role.csv")
years=[int(r["year"]) for r in arr]
A={ "AIE":[int(r["AI_Engineer"]) for r in arr],"DS":[int(r["Data_Scientist"]) for r in arr],
    "MLE":[int(r["ML_Engineer"]) for r in arr],"DE":[int(r["Data_Engineer"]) for r in arr]}

# ---- FIG 1: arrivals momentum (the handoff) ----
def fig_arrivals():
    fig,ax=plt.subplots(figsize=(10,6))
    for k,lab,lw in [("DS","Data Scientist",3.2),("DE","Data Engineer",1.8),
                     ("MLE","ML Engineer",1.8),("AIE","AI Engineer",3.6)]:
        ax.plot(years,A[k],color=C[k],lw=lw,marker="o",
                ms=5 if k in("AIE","DS") else 3,
                alpha=1 if k in("AIE","DS") else .6,label=lab,
                zorder=3 if k in ("AIE","DS") else 2)
    ax.axvline(2024,color="#9ca3af",ls=":",lw=1,alpha=.7)
    ax.annotate("only role still\nrising in 2025",(2025,A["AIE"][-1]),color=C["AIE"],
        fontsize=10,fontweight="bold",xytext=(2022.4,300),
        arrowprops=dict(arrowstyle="->",color=C["AIE"],lw=1.5))
    ax.annotate(f"{A['DS'][-2]}→{A['DS'][-1]}",(2025,A["DS"][-1]),color=C["DS"],
        fontsize=10,xytext=(6,-4),textcoords="offset points",va="center")
    ax.set_title("New entrants each year: AI Engineer is the only role still climbing",pad=12)
    ax.set_ylabel("People starting the role each year (new arrivals)")
    ax.set_xlabel("Year"); ax.set_xticks(years[::2]+[2025])
    ax.grid(axis="y",color=C["grid"],lw=.7); ax.legend(frameon=False,fontsize=11,loc="upper left")
    fig.text(0.5,-0.02,"Source: Skillenai talent graph. Arrivals = role start-events per year (fully observed for past years).",
             ha="center",fontsize=8,color="#9ca3af")
    fig.tight_layout(); fig.savefig(out("01_arrivals_momentum.png"),bbox_inches="tight"); plt.close(fig)

# ---- FIG 2: fixed-lookahead cohort exit rate (censoring-clean 'out' signal) ----
def fig_cohort_exit():
    rows=read_csv("cohort_exit_rates.csv")
    by=defaultdict(dict)
    for r in rows:
        if r["exit_1yr_pct"]!="": by[r["role"]][int(r["year"])]=float(r["exit_1yr_pct"])
    fig,ax=plt.subplots(figsize=(10,6))
    ys=list(range(2018,2026)); solid=[y for y in ys if y<=2024]
    for k,lab,lw in [("DS","Data Scientist",3.4),("SWE","Software Engineer",3.0),
                     ("AIE","AI Engineer",2.4),("MLE","ML Engineer",1.6),("DE","Data Engineer",1.6)]:
        v=[by[k].get(y) for y in solid]
        ax.plot(solid,v,color=C[k],lw=lw,marker="o",ms=5 if k in("DS","SWE") else 3,
                alpha=1 if k in("DS","SWE","AIE") else .55,label=lab,
                zorder=3 if k in("DS","SWE") else 2)
        # 2025 partial: dashed continuation, hollow marker
        if by[k].get(2025) is not None:
            ax.plot([2024,2025],[by[k][2024],by[k][2025]],color=C[k],lw=lw,ls=":",alpha=.45,zorder=1)
            ax.plot(2025,by[k][2025],marker="o",ms=6,mfc="white",mec=C[k],mew=1.5,alpha=.6,zorder=2)
    ax.axvspan(2024.5,2025.5,color="#f8fafc",zorder=0)
    ax.text(2025,3,"2025 partial\n(reporting lag)",ha="center",fontsize=8,color="#9ca3af")
    ax.annotate("Data Scientists leaving\nwithin a year: 30% → 45%",(2024,by["DS"][2024]),
                color=C["DS"],fontsize=10,fontweight="bold",xytext=(2018.2,53),va="center")
    ax.set_title("Who's leaving faster: 1-year exit rate by entry cohort",pad=12)
    ax.set_ylabel("% of the cohort who left the role within 1 year")
    ax.set_xlabel("Year entered the role (cohort)")
    ax.set_xticks(ys); ax.set_ylim(0,60); ax.grid(axis="y",color=C["grid"],lw=.7)
    ax.legend(frameon=False,fontsize=10,loc="upper left",bbox_to_anchor=(0.0,0.86))
    fig.text(0.5,-0.02,"Source: Skillenai talent graph. Fixed 1-year lookahead per cohort (denominator = members observed a full year) — censoring-free, no future data needed.",
             ha="center",fontsize=8,color="#9ca3af")
    fig.tight_layout(); fig.savefig(out("02_cohort_exit_rate.png"),bbox_inches="tight"); plt.close(fig)

# ---- FIG 3: supply-side skill fingerprint ----
def fig_skills():
    rows=read_csv("skill_prevalence.csv")
    skills=[r["skill"] for r in rows]
    V={"AIE":[float(r["AI_Engineer"]) for r in rows],"MLE":[float(r["ML_Engineer"]) for r in rows],
       "DS":[float(r["Data_Scientist"]) for r in rows],"SWE":[float(r["Software_Engineer"]) for r in rows]}
    fig,ax=plt.subplots(figsize=(12,6)); x=np.arange(len(skills)); w=0.2
    for i,(k,lab) in enumerate([("AIE","AI Engineer"),("MLE","ML Engineer"),("DS","Data Scientist"),("SWE","Software Engineer")]):
        ax.bar(x+(i-1.5)*w,V[k],w,label=lab,color=C[k],edgecolor="white",linewidth=.4)
    ax.set_title("The AI Engineer skill fingerprint — measured on the workers themselves",pad=12)
    ax.set_ylabel("% of the role's workers whose profile mentions the skill")
    ax.set_xticks(x); ax.set_xticklabels(skills,rotation=25,ha="right")
    ax.legend(frameon=False,ncol=4,loc="upper right"); ax.grid(axis="y",color=C["grid"],lw=.7)
    fig.text(0.5,-0.03,"Source: Skillenai talent graph — NER over profile 'about' + role descriptions. AI Engineers own the LLM/agent/RAG stack; Data Scientists own statistics.",
             ha="center",fontsize=8,color="#9ca3af")
    fig.tight_layout(); fig.savefig(out("03_skill_fingerprint.png"),bbox_inches="tight"); plt.close(fig)

# ---- FIG 4: Sankey feeders/exits (plotly) ----
def fig_sankey():
    import plotly.graph_objects as go
    s=json.load(open(out("summary.json")))
    colmap={"Software Engineer":"#64748b","Data Scientist":"#dc2626","ML Engineer":"#7c3aed",
            "Data / Analytics Eng":"#0d9488","Researcher / Scientist":"#16a34a","Founder / Leadership":"#ea580c",
            "Other Engineering":"#9ca3af","Product / PM":"#0891b2","Manager / Lead":"#a16207","Other":"#cbd5e1"}
    IN=[(nm,v) for nm,v,_ in s["feeders"]]; OUT=[(nm,v) for nm,v,_ in s["exits"]]
    def rgba(h,a):
        h=h.lstrip("#"); return f"rgba({int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)},{a})"
    n_in=len(IN); center=n_in
    labels=[f"{nm} ({100*v/sum(x[1] for x in IN):.0f}%)" for nm,v in IN]+["AI ENGINEER"]+[f"{nm} ({100*v/sum(x[1] for x in OUT):.0f}%)" for nm,v in OUT]
    colors=[colmap.get(nm,"#cbd5e1") for nm,_ in IN]+[C["AIE"]]+[colmap.get(nm,"#cbd5e1") for nm,_ in OUT]
    node_x=[0.001]*n_in+[0.5]+[0.999]*len(OUT)
    node_y=[(i+.5)/n_in for i in range(n_in)]+[0.5]+[0.30+0.40*(j+.5)/len(OUT) for j in range(len(OUT))]
    src,tgt,val,lc=[],[],[],[]
    for i,(nm,v) in enumerate(IN): src.append(i);tgt.append(center);val.append(v);lc.append(rgba(colmap.get(nm,"#cbd5e1"),.45))
    for j,(nm,v) in enumerate(OUT): src.append(center);tgt.append(center+1+j);val.append(v);lc.append(rgba(colmap.get(nm,"#cbd5e1"),.45))
    fig=go.Figure(go.Sankey(arrangement="snap",
        node=dict(label=labels,color=colors,x=node_x,y=node_y,pad=13,thickness=16,line=dict(width=0)),
        link=dict(source=src,target=tgt,value=val,color=lc)))
    fig.update_layout(title=dict(text="<b>Who becomes an AI Engineer — and where they go next</b>",x=0.5,font=dict(size=20,color=C["ink"])),
        font=dict(family="DejaVu Sans",size=13,color=C["ink"]),
        annotations=[dict(x=0.001,y=1.09,xref="paper",yref="paper",showarrow=False,text="<b>PRIOR ROLE</b>",font=dict(size=12,color="#374151")),
                     dict(x=0.999,y=1.09,xref="paper",yref="paper",showarrow=False,text="<b>NEXT ROLE</b>",font=dict(size=12,color="#374151")),
                     dict(x=0.5,y=-0.13,xref="paper",yref="paper",showarrow=False,
                          text="Source: Skillenai talent graph — full-population career transitions adjacent to an AI Engineer role. Fewer exits than entries: the role is young, so most are still in it.",
                          font=dict(size=10,color="#9ca3af"))],
        margin=dict(l=10,r=10,t=90,b=70),width=1150,height=680,paper_bgcolor="white")
    fig.write_image(out("04_sankey_flows.png"),scale=2)

# ---- FIG 5: salary (demand-side postings) ----
def fig_salary():
    SAL={"MLE":(171960,248688),"AIE":(159659,220104),"SWE":(155326,218376),"DS":(145199,201261)}
    order=["MLE","AIE","SWE","DS"]; labels=["ML Engineer","AI Engineer","Software Engineer","Data Scientist"]
    fig,ax=plt.subplots(figsize=(9,5)); y=np.arange(len(order))[::-1]
    for yi,r,lab in zip(y,order,labels):
        lo,hi=SAL[r]; m=(lo+hi)/2
        ax.plot([lo/1000,hi/1000],[yi,yi],color=C[r],lw=8,solid_capstyle="round",alpha=.85)
        ax.plot(m/1000,yi,"o",color="white",ms=7,markeredgecolor=C[r],markeredgewidth=2)
        ax.text(hi/1000+4,yi,f"${m/1000:.0f}k mid",va="center",fontsize=10,color=C["ink"])
    ax.set_yticks(y); ax.set_yticklabels(labels)
    ax.set_xlabel("USD advertised salary band (median min → max, thousands)")
    ax.set_title("AI Engineer pays like a premium software engineer",pad=12)
    ax.grid(axis="x",color=C["grid"],lw=.7); ax.set_xlim(120,285)
    fig.text(0.5,-0.02,"Source: Skillenai job-postings index (advertised base bands).",ha="center",fontsize=8,color="#9ca3af")
    fig.tight_layout(); fig.savefig(out("05_salary_band.png"),bbox_inches="tight"); plt.close(fig)

if __name__=="__main__":
    fig_arrivals(); fig_cohort_exit(); fig_skills(); fig_sankey(); fig_salary()
    print("figures written to",HERE)
