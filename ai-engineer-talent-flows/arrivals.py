"""Arrivals (role start-events) per year by role, from the owned talent graph.
Censoring-immune: a role-start is a fully-observed past event. Spell-level (consecutive
same-role positions merged). Emits arrivals_by_role.csv."""
import json, re, csv
from collections import Counter, defaultdict
PATH="/Users/jrand/git-repos/skillenai-ds/work/company-eliteness/talent_graph/_data/profiles.jsonl"
OUT="/Users/jrand/git-repos/skillenai-notebooks/.claude/worktrees/ai-eng-graph/ai-engineer-talent-flows/arrivals_by_role.csv"
MONTHS={m:i for i,m in enumerate(["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"],1)}
def yr(s):
    if not s: return None
    s=s.strip()
    if s.lower()=="present": return None
    p=s.split()
    if len(p)==2 and p[0][:3].lower() in MONTHS: return int(p[1])
    if re.fullmatch(r"\d{4}",s): return int(s)
    return None
FOCAL=[("AIE",re.compile(r'\bai engineer|artificial intelligence engineer|\bai/ml engineer|generative ai engineer|\bllm engineer|applied ai engineer|\bai software engineer',re.I)),
("MLE",re.compile(r'machine learning engineer|\bml engineer\b',re.I)),
("DS",re.compile(r'\bdata scientist\b|\bdata science\b',re.I)),
("DE",re.compile(r'\bdata engineer\b',re.I))]
EDU=re.compile(r'university|college|\bschool\b|bootcamp|study abroad|hackathon|\bcamp\b|teaching assistant',re.I)
def role(t):
    for r,p in FOCAL:
        if p.search(t or ""): return r
    return None
arr=defaultdict(Counter)
with open(PATH) as f:
    for line in f:
        d=json.loads(line)
        jobs=[]
        for e in (d.get("experience") or []):
            # multi-role companies nest the real roles under positions[]; the top-level
            # item is just the company (null dates). Flatten so nested roles are counted.
            roles=e.get("positions") or [e]
            for r in roles:
                t=r.get("title") or ""
                if EDU.search(t): continue
                y=yr(r.get("start_date"))
                if y: jobs.append((y,role(t)))
        jobs.sort(key=lambda x:x[0])
        i=0
        while i<len(jobs):
            r=jobs[i][1]
            if r is None: i+=1; continue
            j=i
            while j+1<len(jobs) and jobs[j+1][1]==r: j+=1
            arr[r][jobs[i][0]]+=1
            i=j+1
with open(OUT,"w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["year","AI_Engineer","Data_Scientist","ML_Engineer","Data_Engineer"])
    for y in range(2015,2026): w.writerow([y,arr["AIE"][y],arr["DS"][y],arr["MLE"][y],arr["DE"][y]])
print("wrote",OUT)
print("AIE:", [arr["AIE"][y] for y in range(2019,2026)])
