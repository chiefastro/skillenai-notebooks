"""
Fixed-lookahead cohort exit rates from the owned talent graph — the censoring-clean
'out' signal, in 6-month cohorts. For each half-year entry cohort, the 1-year exit
rate = share whose role-spell ended within 12 months of start. Denominator restricted
to members observed a full year before the snapshot (~Jul 2026), so it's unbiased.
Reliable through the 2024 cohorts; 2025-H1 is provisional (its within-year exits run
into 2026 and are still being reported). H2-2025+ is excluded (not yet a full year old).
Emits raw half-year counts; the figure computes a trailing-12-month (2-period) average
to remove the strong H1/H2 seasonal sawtooth.
"""
import json, re, csv
from collections import Counter, defaultdict

PATH="/Users/jrand/git-repos/skillenai-ds/work/company-eliteness/talent_graph/_data/profiles.jsonl"
OUT="/Users/jrand/git-repos/skillenai-notebooks/.claude/worktrees/ai-eng-graph/ai-engineer-talent-flows/cohort_exit_rates.csv"
SNAP=2026*12+7
MONTHS={m:i for i,m in enumerate(["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"],1)}
def pd(s):
    if not s: return None
    s=s.strip()
    if s.lower()=="present": return ("P",99)
    p=s.split()
    if len(p)==2 and p[0][:3].lower() in MONTHS: return (int(p[1]),MONTHS[p[0][:3].lower()])
    if re.fullmatch(r"\d{4}",s): return (int(s),6)
    return None
def ym(t): return t[0]*12+t[1] if t and t[0]!="P" else None
FOCAL=[("AIE",re.compile(r'\bai engineer|artificial intelligence engineer|\bai/ml engineer|generative ai engineer|\bllm engineer|applied ai engineer|\bai software engineer',re.I)),
("MLE",re.compile(r'machine learning engineer|\bml engineer\b',re.I)),
("DS",re.compile(r'\bdata scientist\b|\bdata science\b',re.I)),
("DE",re.compile(r'\bdata engineer\b',re.I)),
("SWE",re.compile(r'software engineer|software developer',re.I))]
EDU=re.compile(r'university|college|\bschool\b|bootcamp|study abroad|hackathon|\bcamp\b|teaching assistant',re.I)
def role(t):
    for r,p in FOCAL:
        if p.search(t or ""): return r
    return None
elig=defaultdict(Counter); ex=defaultdict(Counter)   # role -> period(year*10+half)
with open(PATH) as f:
    for line in f:
        d=json.loads(line); exp=d.get("experience") or []
        jobs=[]
        for e in exp:
            t=e.get("title") or ""
            if EDU.search(t): continue
            s=pd(e.get("start_date"))
            if not s or s[0]=="P": continue
            jobs.append({"r":role(t),"s":s,"e":pd(e.get("end_date"))})
        jobs.sort(key=lambda j:(j["s"][0],j["s"][1]))
        i=0
        while i<len(jobs):
            r=jobs[i]["r"]
            if r is None: i+=1; continue
            j=i
            while j+1<len(jobs) and jobs[j+1]["r"]==r: j+=1
            sm=ym(jobs[i]["s"]); em=ym(jobs[j]["e"])
            per=jobs[i]["s"][0]*10+(1 if jobs[i]["s"][1]<=6 else 2)
            if sm+12<=SNAP:
                elig[r][per]+=1
                if em is not None and em-sm<=12: ex[r][per]+=1
            i=j+1
periods=[y*10+h for y in range(2018,2026) for h in (1,2) if y*10+h<=20251]
with open(OUT,"w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["x","period","role","exits","eligible","exit_1yr_pct"])
    for per in periods:
        x=per//10 + (0.0 if per%10==1 else 0.5)
        for r in ["AIE","DS","MLE","DE","SWE"]:
            n=elig[r][per]
            w.writerow([x,f"{per//10}-H{per%10}",r,ex[r][per],n,round(100*ex[r][per]/n,1) if n else ""])
print("wrote",OUT)
