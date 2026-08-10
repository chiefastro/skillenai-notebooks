"""
Fixed-lookahead cohort exit rates from the owned talent graph — the censoring-clean
'out' signal. For each cohort (role-start year), the K-year exit rate is the share of
that cohort whose role-spell ended within K years. Denominator restricted to members
who have had the full K years to be observed before the snapshot (~Jul 2026), so the
rate is unbiased. 1-year horizon is reliable through 2024 (2025 partial: reporting lag).
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
arr=defaultdict(Counter)
elig={1:defaultdict(Counter),2:defaultdict(Counter)}
ex={1:defaultdict(Counter),2:defaultdict(Counter)}
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
            sy=jobs[i]["s"][0]; sm=ym(jobs[i]["s"]); em=ym(jobs[j]["e"])
            arr[r][sy]+=1
            for K in (1,2):
                if sm+12*K<=SNAP:
                    elig[K][r][sy]+=1
                    if em is not None and em-sm<=12*K: ex[K][r][sy]+=1
            i=j+1
with open(OUT,"w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["year","role","arrivals","exit_1yr_pct","n_1yr","exit_2yr_pct","n_2yr"])
    for r in ["AIE","DS","MLE","DE","SWE"]:
        for y in range(2016,2026):
            e1=elig[1][r][y]; e2=elig[2][r][y]
            w.writerow([y,r,arr[r][y],
                        round(100*ex[1][r][y]/e1,1) if e1 else "", e1,
                        round(100*ex[2][r][y]/e2,1) if e2 else "", e2])
print("wrote",OUT)
