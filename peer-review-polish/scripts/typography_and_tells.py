#!/usr/bin/env python3
"""Broad multi-signal LLM-tell panel for peer reviews, as a time series.

Three tiers, kept separate because peer review has its own register:

 A. TYPOGRAPHY -- characters a plain <textarea> does not produce. Evidence that text
    was composed elsewhere and pasted (LLM, Word, or Docs). Highest precision for
    "not typed here", says nothing about who wrote it.
 B. LLM PHRASING -- constructions rare in human peer review but common in model prose.
 C. REGISTER-AMBIGUOUS -- AI-overused words that are also normal reviewer vocabulary
    ('robust', 'comprehensive', 'significant'). Reported, never headlined.

Plus structural metrics: sentence-length uniformity (models write evener prose) and
markdown scaffolding (headers/bold/bullets inside a plain-text review box).
"""
import os
DATA = os.environ.get("PRP_DATA", "_data")   # collected notes; override with PRP_DATA
OUT  = os.environ.get("PRP_OUT", ".")       # figures/CSVs written here
import json, re, glob, sys, collections, math, statistics as st

A_TYPO = {
 "em/en dash":      r"[—–]",
 "curly double q":  r"[“”]",
 "curly single q":  r"[‘’]",
 "ellipsis char":   r"…",
 "nonbreaking sp":  r" ",
 "bullet glyph":    r"[•▪◦‣]",
 "arrow glyph":     r"[→←⇒]",
 "md bold":         r"\*\*\w",
 "md header":       r"(?m)^#{1,4}\s",
 "md numbered":     r"(?m)^\s*\d+\.\s+\w",
}
B_LLM = {
 "delve":            r"\bdelv(?:e|es|ed|ing)\b",
 "showcase":         r"\bshowcas(?:e|es|ed|ing)\b",
 "underscore(v)":    r"\bunderscor(?:e|es|ed|ing)\b",
 "commendable":      r"\bcommendable\b",
 "meticulous":       r"\bmeticulous(?:ly)?\b",
 "noteworthy":       r"\bnoteworthy\b",
 "compelling":       r"\bcompelling\b",
 "boasts":           r"\bboasts?\b",
 "serves/stands as": r"\b(?:serves|stands) as\b",
 "plays a X role":   r"\bplays? a (?:crucial|vital|pivotal|key|significant) role\b",
 "not only/but also":r"\bnot only\b[^.]{0,80}\bbut also\b",
 "sheds light on":   r"\bsheds? light on\b",
 "paves the way":    r"\bpaves? the way\b",
 "opens new avenues":r"\bopens? (?:up )?(?:new |promising )?avenues?\b",
 "worth noting":     r"\bit(?:'s| is) worth noting\b",
 "important to note":r"\bit is important to note\b",
 "in summary":       r"(?m)^\s*(?:in summary|to summarize|overall,)\b",
 "tapestry":         r"\btapestry\b",
 "testament":        r"\bis a testament\b",
 "intricate":        r"\bintricate\b",
 "pivotal":          r"\bpivotal\b",
 "garner":           r"\bgarner(?:s|ed|ing)?\b",
 "interplay":        r"\binterplay\b",
 "multifaceted":     r"\bmultifaceted\b",
 "holistic":         r"\bholistic\b",
 "myriad/plethora":  r"\b(?:myriad|plethora)\b",
 "seamless":         r"\bseamless(?:ly)?\b",
 "at its core":      r"\bat its core\b",
}
C_AMBIG = {
 "crucial":r"\bcrucial\b", "comprehensive":r"\bcomprehensive\b", "robust":r"\brobust\b",
 "significant":r"\bsignificant\b", "novel":r"\bnovel\b", "leverage":r"\bleverag\w*\b",
 "enhance":r"\benhanc\w*\b", "valuable":r"\bvaluable\b", "nuanced":r"\bnuanced\b",
 "key(adj)":r"\bkey\b", "align with":r"\balign\w* with\b", "highlight":r"\bhighlight\w*\b",
}
RA={k:re.compile(v) for k,v in A_TYPO.items()}
RB={k:re.compile(v,re.I) for k,v in B_LLM.items()}
RC={k:re.compile(v,re.I) for k,v in C_AMBIG.items()}
TEXT=("summary","strengths","weaknesses","questions","review","metareview","comment",
      "limitations","justification_for_why_not_higher_score","reason_for_recommendation")

def text_of(c):
    return "\n".join(v for k,v in c.items()
                     if isinstance(v,str) and (k in TEXT or len(v)>120))

def sent_uniformity(t):
    s=[len(x.split()) for x in re.split(r"[.!?]+\s", t) if len(x.split())>=3]
    if len(s)<6: return None
    m=st.mean(s)
    return st.pstdev(s)/m if m else None

def load():
    seen={}
    for p in glob.glob(f"{DATA}/*.jsonl"):
        for l in open(p):
            try: r=json.loads(l)
            except Exception: continue
            if r.get("id"): seen[r["id"]]=r
    return list(seen.values())

def main():
    rows=load()
    recs=[]
    for r in rows:
        if r["kind"]!="Official_Review": continue
        t=text_of(r.get("content") or {})
        if len(t)<2000: continue          # length-matched throughout
        recs.append({"dom":r.get("domain") or "?","len":len(t),
            "A":{k:bool(rx.search(t)) for k,rx in RA.items()},
            "B":{k:bool(rx.search(t)) for k,rx in RB.items()},
            "C":{k:len(rx.findall(t)) for k,rx in RC.items()},
            "cv":sent_uniformity(t)})
    by=collections.defaultdict(list)
    for x in recs: by[x["dom"]].append(x)
    ven=[(d,g) for d,g in sorted(by.items(),key=lambda kv:-len(kv[1])) if len(g)>=250]
    order=[d for d,_ in ven]
    short=[d.replace(".cc","").replace("/Conference","").replace("colmweb.org/","")
             .replace("MIDL.io/","MIDL ").replace("ICLR/","ICLR ").replace("NeurIPS/","NeurIPS ")
             .replace("COLM/","COLM ") for d in order]

    print(f"reviews >=2000 chars: {len(recs):,}   venues shown: {len(order)}\n")
    hdr="".join(f"{s[:11]:>12}" for s in short)
    print(f"{'':<20}{hdr}")
    print(f"{'n':<20}"+"".join(f"{len(by[d]):>12,}" for d in order))
    print(f"\n--- TIER A: typography (composed outside the review box) ---")
    for k in A_TYPO:
        cells="".join(f"{100*sum(x['A'][k] for x in by[d])/len(by[d]):>11.1f}%" for d in order)
        print(f"{k:<20}{cells}")
    print(f"{'ANY tier-A':<20}"+"".join(
        f"{100*sum(any(x['A'].values()) for x in by[d])/len(by[d]):>11.1f}%" for d in order))
    print(f"\n--- TIER B: LLM phrasing (rare in human review) ---")
    for k in B_LLM:
        vals=[100*sum(x['B'][k] for x in by[d])/len(by[d]) for d in order]
        if max(vals)>=0.8:
            print(f"{k:<20}"+"".join(f"{v:>11.1f}%" for v in vals))
    print(f"{'ANY tier-B':<20}"+"".join(
        f"{100*sum(any(x['B'].values()) for x in by[d])/len(by[d]):>11.1f}%" for d in order))
    print(f"\n--- TIER C: register-ambiguous, per 10k chars (do not headline) ---")
    for k in C_AMBIG:
        cells="".join(f"{10000*sum(x['C'][k] for x in by[d])/sum(x['len'] for x in by[d]):>11.1f} " for d in order)
        print(f"{k:<20}{cells}")
    print(f"\n--- structural ---")
    print(f"{'sent-len CV':<20}"+"".join(
        f"{st.mean([x['cv'] for x in by[d] if x['cv']]):>12.3f}" for d in order))
    print("  (lower CV = more uniform sentence lengths; models write evener prose)")
    print(f"{'median chars':<20}"+"".join(f"{sorted(x['len'] for x in by[d])[len(by[d])//2]:>12,}" for d in order))

main()
