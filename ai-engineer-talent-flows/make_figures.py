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
    solid=[y for y in ys if y<=2024]
    LO,MID,HI=1.3,1.4,1.5   # full-year projection multipliers for the ~Oct 2025 employment cutoff
    fig,ax=plt.subplots(figsize=(10,6))
    for k,lab,lw in [("AIE","AI Engineer",3.6),("DS","Data Scientist",2),("DE","Data Engineer",2),("MLE","ML Engineer",2)]:
        vs=[A[k][ys.index(y)] for y in solid]
        hi=(k=="AIE")
        ax.plot(solid,vs,color=C[k],lw=lw,marker="o",ms=5 if hi else 3,alpha=1 if hi else .65,label=lab,zorder=3 if hi else 2)
        # 2025 = full-year PROJECTION (diamond) with a x1.3-1.5 range bar
        obs=A[k][ys.index(2025)]; mid=obs*MID
        ax.plot([2024,2025],[A[k][ys.index(2024)],mid],color=C[k],lw=lw,ls=":",alpha=.5,zorder=1)
        ax.errorbar(2025,mid,yerr=[[obs*(MID-LO)],[obs*(HI-MID)]],fmt="D",ms=6,mfc="white",mec=C[k],
                    color=C[k],ecolor=C[k],elinewidth=1.4,capsize=4,alpha=.95 if hi else .6,zorder=3 if hi else 2)
    ax.axvspan(2024.5,2025.5,color="#f8fafc",zorder=0)
    ax.text(2025,865,"2025\nprojected",ha="center",fontsize=8.5,color="#6b7280",fontweight="bold")
    ax.annotate("AI Engineer climbs every year through 2024 —\nand its projected 2025 lands well above 2024",
                (2024,A["AIE"][ys.index(2024)]),color=C["AIE"],fontsize=10,fontweight="bold",
                xytext=(2015.2,470),va="center",arrowprops=dict(arrowstyle="->",color=C["AIE"],lw=1.5))
    ax.set_title("New entrants per year: AI Engineer is the fastest-growing role",pad=12)
    ax.set_ylabel("People starting the role each year (new arrivals)")
    ax.set_xlabel("Year"); ax.set_xticks(ys[::1]); ax.set_xticklabels(ys,rotation=45,ha="right",fontsize=9)
    ax.grid(axis="y",color=C["grid"],lw=.7); ax.legend(frameon=False,fontsize=11,loc="upper left")
    fig.text(0.5,-0.02,"Source: Skillenai talent graph. Arrivals = role start-events per year. Employment records are current to ~Oct 2025; the 2025 diamond is a full-year projection (×1.3–1.5 range for the partial year), not an observed count.",
             ha="center",fontsize=8,color="#9ca3af")
    fig.tight_layout(); fig.savefig(out("02_arrivals_momentum.png"),bbox_inches="tight"); plt.close(fig)

# ---- FIG 3: supply vs demand skill gap (scatter) ----
def fig_skill_gap():
    rows=[(r["skill"],float(r["demand_pct"]),float(r["supply_pct"])) for r in read_csv("skill_supply_demand.csv")]
    L=24
    fig,ax=plt.subplots(figsize=(11,8.5))
    BAND=3
    xs=np.linspace(0,L,200); lo=np.clip(xs-BAND,0,L); hi=np.clip(xs+BAND,0,L)
    ax.fill_between(xs,hi,L,color="#dbeafe",alpha=.35,zorder=0)   # demand ahead
    ax.fill_between(xs,0,lo,color="#fee2e2",alpha=.35,zorder=0)   # supply legacy
    ax.fill_between(xs,lo,hi,color="#e5e7eb",alpha=.7,zorder=0)   # aligned band (±3 pts)
    ax.plot([0,L],[0,L],color="#9ca3af",ls="--",lw=1,zorder=1)
    ax.text(19.5,17.6,"aligned",color="#6b7280",fontsize=9,rotation=45,ha="center",va="center")
    ax.text(1.5,22.5,"EMPLOYERS ASK FOR IT MORE than workers list it\nthe reskilling frontier",color="#1d4ed8",fontsize=10.5,fontweight="bold",va="top")
    ax.text(15.2,2.9,"WORKERS LIST IT MORE than employers ask\nlegacy from prior roles",color="#b91c1c",fontsize=10.5,fontweight="bold",va="top")
    LABELS={"prompt engineering":(6,2,"left"),"LLMs":(6,1,"left"),"rag":(6,-3,"left"),
        "machine learning":(6,4,"left"),"langchain":(7,-6,"left"),"AWS":(-6,5,"right"),
        "TypeScript":(-7,1,"right"),"vector databases":(6,5,"left"),"fine-tuning":(7,-3,"left"),
        "pytorch":(6,0,"left"),"observability":(5,5,"left"),"langgraph":(6,-1,"left"),
        "APIs":(5,-7,"left"),"kubernetes":(6,3,"left"),"docker":(6,-1,"left"),"sql":(-6,3,"right"),
        "tensorflow":(6,-3,"left"),"evaluation frameworks":(6,1,"left"),"guardrails":(5,-3,"left"),
        "JavaScript":(6,2,"left"),"computer vision":(6,-9,"left"),"NLP":(6,5,"left"),
        "Excel":(5,5,"left"),"Tableau":(-4,10,"right")}
    for nm,dm,sp in rows:
        gap=dm-sp
        c="#2563eb" if gap>3 else ("#dc2626" if gap<-3 else "#6b7280")
        ax.scatter(sp,dm,s=42,color=c,zorder=3,alpha=.9,edgecolors="white",linewidths=.4)
        if nm in LABELS:
            dx,dy,ha=LABELS[nm]
            ax.annotate(nm,(sp,dm),xytext=(dx,dy),textcoords="offset points",fontsize=8.5,color="#111827",ha=ha)
    ax.annotate("Python sits at 47% / 48% — off-chart top-right, perfectly aligned",
                (L,L),xytext=(-8,-10),textcoords="offset points",ha="right",va="top",fontsize=8.5,color="#6b7280",style="italic")
    ax.set_xlim(0,L); ax.set_ylim(0,L)
    ax.set_xlabel("SUPPLY — % of AI Engineers who list the skill (talent graph)")
    ax.set_ylabel("DEMAND — % of AI Engineer postings that ask for it (job index)")
    ax.set_title("Supply vs demand: where AI Engineer skills line up — and don't",pad=12)
    ax.grid(color=C["grid"],lw=.6)
    fig.text(0.5,-0.02,"Both entity-resolved to the same skill taxonomy. On the diagonal = aligned; above = demand runs ahead of supply; below = workers carry prior-role skills employers no longer ask for.",
             ha="center",fontsize=8,color="#9ca3af")
    fig.tight_layout(); fig.savefig(out("03_skill_gap.png"),bbox_inches="tight"); plt.close(fig)

# ---- FIG 4: demand-side skill fingerprint ----
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
    fig.tight_layout(); fig.savefig(out("04_skill_fingerprint.png"),bbox_inches="tight"); plt.close(fig)

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
    fig.tight_layout(); fig.savefig(out("05_salary_band.png"),bbox_inches="tight"); plt.close(fig)

if __name__=="__main__":
    fig_sankey(); fig_arrivals(); fig_skill_gap(); fig_skills(); fig_salary()
    print("figures written to",HERE)
