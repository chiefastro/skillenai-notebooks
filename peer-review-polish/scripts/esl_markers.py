#!/usr/bin/env python3
"""Do non-native-English markers decline as AI polish rises?

Hypothesis: LLM polish is adopted disproportionately by non-native English speakers,
for whom it is most useful. If so, the surface markers that polish removes should
DECLINE over the same window in which typography rises.

Markers are article omission and agreement slips -- the highest-precision signal
available in academic English, because many major languages of the ML research
community (Chinese, Japanese, Korean, Russian and the Slavic family) have no articles.

This measures TEXT, not people. Reviewers are anonymised; nothing here identifies
anyone or supports a claim about any individual.
"""
import os
DATA = os.environ.get("PRP_DATA", "_data")   # collected notes; override with PRP_DATA
OUT  = os.environ.get("PRP_OUT", ".")       # figures/CSVs written here
import json, re, glob, collections, math

M = {
 # article omission before a definite, previously-introduced noun
 "'paper' w/o article":  r"(?<![\w'])(?:In|in)\s+paper\b|(?<![\w'])[Pp]aper\s+(?:proposes|presents|introduces|studies|shows)\b",
 "'authors' w/o 'the'":  r"(?<![\w'])(?<!the )(?<!The )[Aa]uthors\s+(?:propose|present|introduce|claim|show|argue|use|report)\b",
 "'method' w/o article": r"(?<![\w'])(?:[Pp]roposed|[Pp]resented)\s+method\b(?!\s*(?:is|are))",
 "in Section N w/o the": r"\bin\s+[Ss]ection\s+\d+\s+authors\b",
 # subject-verb agreement slips common in article-less L1s
 "3sg agreement slip":   r"\b(?:method|paper|model|approach|author|framework)\s+(?:achieve|propose|present|show|provide|lack|use|need)\b",
 "plural agreement":     r"\b(?:results|experiments|authors|methods)\s+(?:is|was|shows|provides|lacks)\b",
 # determiner-count mismatch
 "'a' + plural":         r"\ba\s+(?:results|experiments|methods|papers|works)\b",
 # missing 'the' before superlative
 "superlative w/o the":  r"(?<!the )\b(?:best|worst|most|largest|highest)\s+(?:performance|accuracy|result)\b",
}
R={k:re.compile(v) for k,v in M.items()}
TEXT=("summary","strengths","weaknesses","questions","review","metareview","comment","limitations")
def text_of(c): return "\n".join(v for k,v in c.items() if isinstance(v,str) and (k in TEXT or len(v)>120))

seen={}
for p in glob.glob(f"{DATA}/*.jsonl"):
    if "judgments" in p: continue
    for l in open(p):
        try: r=json.loads(l)
        except Exception: continue
        if r.get("id"): seen[r["id"]]=r
by=collections.defaultdict(list)
for r in seen.values():
    if r["kind"]!="Official_Review": continue
    t=text_of(r.get("content") or {})
    if len(t)<2000: continue
    by[r.get("domain") or "?"].append({"len":len(t),
        **{k:bool(rx.search(t)) for k,rx in R.items()}})

def zt(k1,n1,k2,n2):
    p1,p2=k1/n1,k2/n2; se=math.sqrt(p1*(1-p1)/n1+p2*(1-p2)/n2)
    if not se: return 0,1
    z=(p1-p2)/se; return z, math.erfc(abs(z)/math.sqrt(2))

ven=["ICLR.cc/2024/Conference","ICLR.cc/2025/Conference","ICLR.cc/2026/Conference",
     "NeurIPS.cc/2023/Conference","NeurIPS.cc/2024/Conference","NeurIPS.cc/2025/Conference"]
ven=[v for v in ven if len(by.get(v,[]))>=250]
print(f"{'':<24}"+"".join(f"{v.split('/')[1] if '/' in v else v:>10}" for v in ven))
print(f"{'venue':<24}"+"".join(f"{v.split('.')[0][:9]:>10}" for v in ven))
print(f"{'n':<24}"+"".join(f"{len(by[v]):>10,}" for v in ven))
print()
for k in M:
    print(f"{k:<24}"+"".join(f"{100*sum(x[k] for x in by[v])/len(by[v]):>9.1f}%" for v in ven))
print(f"\n{'ANY marker':<24}"+"".join(
    f"{100*sum(any(x[k] for k in M) for x in by[v])/len(by[v]):>9.1f}%" for v in ven))

print("\n=== ICLR 2024 -> 2026, any non-native marker ===")
a,b=by["ICLR.cc/2024/Conference"],by["ICLR.cc/2026/Conference"]
ka=sum(any(x[k] for k in M) for x in a); kb=sum(any(x[k] for k in M) for x in b)
z,p=zt(kb,len(b),ka,len(a))
print(f"  {100*ka/len(a):.1f}% -> {100*kb/len(b):.1f}%  ({100*(kb/len(b)-ka/len(a)):+.1f}pp)  z={z:+.2f} p={p:.2e}")
print(f"  prediction was a DECLINE if polish is disproportionately non-native-speaker adoption")
