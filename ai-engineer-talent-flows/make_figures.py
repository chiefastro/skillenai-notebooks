"""
Figures for "Who Becomes an AI Engineer" — Skillenai talent graph (supply-side career
flows, entity-resolved roles) + job-postings index (demand-side skills & salary).
Reads the CSVs in this folder. See README.md for methodology.
"""
import csv, os
from collections import defaultdict
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.family":"DejaVu Sans",
    "axes.spines.top":False,"axes.spines.right":False,"axes.titleweight":"bold","axes.titlesize":15})
HERE=os.path.dirname(os.path.abspath(__file__))
def out(n): return os.path.join(HERE,n)
def read_csv(n):
    with open(out(n)) as f: return list(csv.DictReader(f))
C={"AIE":"#2563eb","DS":"#dc2626","MLE":"#7c3aed","DE":"#0d9488","SWE":"#64748b",
   "grid":"#e5e7eb","ink":"#111827"}

# ---- FIG 1 (centerpiece): resolved Sankey ----
ROLE_COLORS={"Software Engineer":"#64748b","ML Engineer":"#7c3aed","Data Scientist":"#dc2626",
    "Data Engineer":"#0d9488","Data Analyst":"#0891b2","Research Assistant":"#16a34a",
    "Researcher":"#22c55e","Teaching Assistant":"#4ade80","Founder":"#ea580c",
    "Product Manager":"#a16207","Software Developer":"#94a3b8","AI Research Engineer":"#7c3aed",
    "Other roles":"#cbd5e1"}
def _rgba(h,a):
    h=h.lstrip("#"); return f"rgba({int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)},{a})"
def fig_sankey():
    import plotly.graph_objects as go
    rows=read_csv("sankey_flows.csv")
    IN=[(r["role"],int(r["n_moves"])) for r in rows if r["direction"]=="in"]
    OUT=[(r["role"],int(r["n_moves"])) for r in rows if r["direction"]=="out"]
    def top_tail(lst,k=9):
        lst=sorted(lst,key=lambda x:-x[1]); head=lst[:k]
        tail=sum(v for _,v in lst[k:]); nt=len(lst)-k
        if tail>0: head.append((f"{nt} other roles",tail))
        return head
    IN=top_tail(IN); OUT=top_tail(OUT)
    ti=sum(v for _,v in IN); to=sum(v for _,v in OUT)
    def col(nm): return ROLE_COLORS.get(nm.split(" other")[0] if "other roles" in nm else nm, "#cbd5e1")
    n_in=len(IN); center=n_in
    labels=[f"{nm}  ({100*v/ti:.0f}%)" for nm,v in IN]+["AI ENGINEER"]+[f"{nm}  ({100*v/to:.0f}%)" for nm,v in OUT]
    colors=[col(nm) for nm,_ in IN]+[C["AIE"]]+[col(nm) for nm,_ in OUT]
    node_x=[0.001]*n_in+[0.5]+[0.999]*len(OUT)
    node_y=[(i+.5)/n_in for i in range(n_in)]+[0.5]+[0.30+0.40*(j+.5)/len(OUT) for j in range(len(OUT))]
    src,tgt,val,lc=[],[],[],[]
    for i,(nm,v) in enumerate(IN): src.append(i);tgt.append(center);val.append(v);lc.append(_rgba(col(nm),.45))
    for j,(nm,v) in enumerate(OUT): src.append(center);tgt.append(center+1+j);val.append(v);lc.append(_rgba(col(nm),.45))
    fig=go.Figure(go.Sankey(arrangement="snap",
        node=dict(label=labels,color=colors,x=node_x,y=node_y,pad=14,thickness=16,line=dict(width=0)),
        link=dict(source=src,target=tgt,value=val,color=lc)))
    fig.update_layout(title=dict(text="<b>Who becomes an AI Engineer — and where they go next</b>",x=0.5,font=dict(size=21,color=C["ink"])),
        font=dict(family="DejaVu Sans",size=13,color=C["ink"]),
        annotations=[dict(x=0.001,y=1.08,xref="paper",yref="paper",showarrow=False,text="<b>PRIOR ROLE</b>",font=dict(size=12,color="#374151")),
                     dict(x=0.999,y=1.08,xref="paper",yref="paper",showarrow=False,text="<b>NEXT ROLE</b>",font=dict(size=12,color="#374151")),
                     dict(x=0.5,y=-0.13,xref="paper",yref="paper",showarrow=False,
                          text="Source: Skillenai talent graph — entity-resolved role-to-role transitions (full population). "
                               "More arrivals than exits: the role is young, so most who joined are still in it.",
                          font=dict(size=10,color="#9ca3af"))],
        margin=dict(l=10,r=10,t=85,b=70),width=1200,height=680,paper_bgcolor="white")
    fig.write_image(out("01_sankey_flows.png"),scale=2)

# ---- FIG 2: arrivals momentum ----
def fig_arrivals():
    rows=read_csv("arrivals_by_role.csv")
    ys=[int(r["year"]) for r in rows]
    A={k:[int(r[c]) for r in rows] for k,c in [("AIE","AI_Engineer"),("DS","Data_Scientist"),("MLE","ML_Engineer"),("DE","Data_Engineer")]}
    fig,ax=plt.subplots(figsize=(10,6))
    ax.bar(ys,A["AIE"],color=C["AIE"],width=.62,label="AI Engineer",zorder=3)
    for k,lab in [("DS","Data Scientist"),("DE","Data Engineer"),("MLE","ML Engineer")]:
        ax.plot(ys,A[k],color=C[k],lw=2,marker="o",ms=3,alpha=.65,label=lab,zorder=2)
    ax.annotate(f"AI Engineer: {A['AIE'][-3]} → {A['AIE'][-1]}\nnew entrants (2023→2025)",
                (ys[-1],A["AIE"][-1]),color=C["AIE"],fontsize=10,fontweight="bold",
                xytext=(2018.2,760),va="center",arrowprops=dict(arrowstyle="->",color=C["AIE"],lw=1.5))
    ax.annotate("Data Scientist peaked 2024,\nfell in 2025",(2025,A["DS"][-1]),color=C["DS"],fontsize=9,
                xytext=(2022.4,300),va="center")
    ax.set_title("New entrants per year: AI Engineer is the only role still climbing",pad=12)
    ax.set_ylabel("People starting the role each year (new arrivals)")
    ax.set_xlabel("Year"); ax.set_xticks(ys[::1]); ax.set_xticklabels(ys,rotation=45,ha="right",fontsize=9)
    ax.grid(axis="y",color=C["grid"],lw=.7); ax.legend(frameon=False,fontsize=11,loc="upper left")
    fig.text(0.5,-0.02,"Source: Skillenai talent graph. Arrivals = role start-events per year — fully observed for past years (censoring-immune).",
             ha="center",fontsize=8,color="#9ca3af")
    fig.tight_layout(); fig.savefig(out("02_arrivals_momentum.png"),bbox_inches="tight"); plt.close(fig)

# ---- FIG 3: demand-side skill fingerprint ----
def fig_skills():
    rows=read_csv("skill_prevalence.csv")
    skills=[r["skill"] for r in rows]
    V={k:[float(r[c]) for r in rows] for k,c in [("AIE","AI_Engineer"),("MLE","ML_Engineer"),("DS","Data_Scientist"),("SWE","Software_Engineer")]}
    fig,ax=plt.subplots(figsize=(12,6)); x=np.arange(len(skills)); w=0.2
    for i,(k,lab) in enumerate([("AIE","AI Engineer"),("MLE","ML Engineer"),("DS","Data Scientist"),("SWE","Software Engineer")]):
        ax.bar(x+(i-1.5)*w,V[k],w,label=lab,color=C[k],edgecolor="white",linewidth=.4)
    ax.set_title("A different job, not a rename: what employers ask AI Engineers for",pad=12)
    ax.set_ylabel("% of the role's job postings mentioning the skill")
    ax.set_xticks(x); ax.set_xticklabels(skills,rotation=25,ha="right")
    ax.legend(frameon=False,ncol=4,loc="upper right"); ax.grid(axis="y",color=C["grid"],lw=.7)
    fig.text(0.5,-0.03,"Source: Skillenai job-postings index. AI Engineer owns the LLM/agent/RAG stack; ML Eng owns PyTorch; Data Scientist owns statistics.",
             ha="center",fontsize=8,color="#9ca3af")
    fig.tight_layout(); fig.savefig(out("03_skill_fingerprint.png"),bbox_inches="tight"); plt.close(fig)

# ---- FIG 4: salary ----
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
    fig.tight_layout(); fig.savefig(out("04_salary_band.png"),bbox_inches="tight"); plt.close(fig)

if __name__=="__main__":
    fig_sankey(); fig_arrivals(); fig_skills(); fig_salary()
    print("figures written to",HERE)
