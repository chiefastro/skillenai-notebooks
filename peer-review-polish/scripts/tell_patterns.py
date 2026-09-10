#!/usr/bin/env python3
"""Direct LLM-writing-tell detection on peer reviews.

Tells come from Wikipedia's "Signs of AI writing" (via the humanizer skill). They are
split into two tiers because academic peer review has its own register:

  TIER 1 (high precision): words/punctuation that are RARE in human peer review, so a
    hit is strong evidence -- 'delve', 'tapestry', 'testament', 'showcase', 'boasts',
    em dashes, curly quotes.
  TIER 2 (low precision): AI-overused words that are ALSO normal reviewer vocabulary --
    'crucial', 'key', 'comprehensive', 'robust', 'significant'. Reported separately;
    never headline these alone.

The measurement that matters is the RATE OVER TIME within one venue, not the absolute
level. Same venue, same register, same review form -- so a rise is not explained by
academic style.
"""
import json, re, sys, collections, math

TIER1 = {
 "delve":            r"\bdelv(?:e|es|ed|ing)\b",
 "tapestry":         r"\btapestry\b",
 "testament":        r"\b(?:a|is a) testament\b",
 "showcase":         r"\bshowcas(?:e|es|ed|ing)\b",
 "boasts":           r"\bboasts?\b",
 "underscore(v)":    r"\bunderscor(?:e|es|ed|ing)\b",
 "serves/stands as": r"\b(?:serves|stands) as\b",
 "plays a X role":   r"\bplays? a (?:crucial|vital|pivotal|key|significant) role\b",
 "not only/but also":r"\bnot only\b[^.]{0,80}\bbut also\b",
 "it's not just X":  r"\b(?:it'?s|this is) not (?:just|merely|only)\b[^.]{0,60},",
 "important to note":r"\bit is important to note that\b",
 "at its core":      r"\bat its core\b",
 "the real question":r"\bthe real question is\b",
 "intricate":        r"\bintricate(?:ly|ies)?\b",
 "pivotal":          r"\bpivotal\b",
 "garner":           r"\bgarner(?:s|ed|ing)?\b",
 "foster(figurative)":r"\bfoster(?:s|ed|ing)?\b",
 "interplay":        r"\binterplay\b",
 "em/en dash":       r"[—–]",
 "curly quotes":     r"[“”‘’]",
}
TIER2 = {
 "crucial":       r"\bcrucial\b",
 "key(adj)":      r"\bkey\b",
 "comprehensive": r"\bcomprehensive\b",
 "robust":        r"\brobust\b",
 "significant":   r"\bsignificant\b",
 "enhance":       r"\benhanc(?:e|es|ed|ing|ement)\b",
 "leverage":      r"\bleverag(?:e|es|ed|ing)\b",
 "landscape":     r"\blandscape\b",
 "align with":    r"\balign(?:s|ed|ing)? with\b",
 "highlight(v)":  r"\bhighlight(?:s|ed|ing)\b",
 "nuanced":       r"\bnuanced\b",
 "valuable":      r"\bvaluable\b",
}
T1={k:re.compile(v,re.I) for k,v in TIER1.items()}
T2={k:re.compile(v,re.I) for k,v in TIER2.items()}
TEXT_FIELDS=("summary","strengths","weaknesses","questions","review","metareview",
             "comment","justification_for_why_not_higher_score","limitations")

def review_text(c):
    parts=[]
    for k,v in c.items():
        if isinstance(v,str) and (k in TEXT_FIELDS or len(v)>120):
            parts.append(v)
    return "\n".join(parts)

def main(path):
    rows=[json.loads(l) for l in open(path)]
    by=collections.defaultdict(lambda:{"n":0,"chars":0,
        "t1":collections.Counter(),"t2":collections.Counter(),"t1_docs":collections.Counter()})
    for r in rows:
        if r["kind"]!="Official_Review": continue
        dom=r.get("domain") or "?"
        if not dom.startswith(("ICLR","NeurIPS","TMLR","colmweb")): continue
        txt=review_text(r.get("content") or {})
        if len(txt)<200: continue
        b=by[dom]; b["n"]+=1; b["chars"]+=len(txt)
        for k,rx in T1.items():
            c=len(rx.findall(txt))
            if c: b["t1"][k]+=c; b["t1_docs"][k]+=1
        for k,rx in T2.items():
            b["t2"][k]+=len(rx.findall(txt))
    order=[d for d in sorted(by, key=lambda d:-by[d]["n"]) if by[d]["n"]>=40]
    print(f"{'venue':<30}{'reviews':>8}{'avg chars':>11}{'TIER1 /10k words':>19}{'% w/ any T1':>13}")
    for d in order:
        b=by[d]; words=b["chars"]/5.5
        t1=sum(b["t1"].values()); anydoc=len({0}) and 0
        # share of reviews with >=1 tier-1 hit
        print(f"{d:<30}{b['n']:>8}{b['chars']/b['n']:>11,.0f}{10000*t1/words:>19.2f}", end="")
        print(f"{100*max(b['t1_docs'].values() or [0])/b['n']:>12.1f}%")
    print(f"\nTIER 1 tell breakdown (docs containing, % of reviews):")
    hdr="".join(f"{d.split('.')[0][:11]:>13}" for d in order)
    print(f"{'tell':<20}{hdr}")
    for k in TIER1:
        cells="".join(f"{100*by[d]['t1_docs'][k]/by[d]['n']:>12.1f}%" for d in order)
        if any(by[d]['t1_docs'][k] for d in order): print(f"{k:<20}{cells}")
    print(f"\nTIER 2 (low precision, normal reviewer vocabulary) per 10k words:")
    for k in TIER2:
        cells="".join(f"{10000*by[d]['t2'][k]/(by[d]['chars']/5.5):>12.1f} " for d in order)
        print(f"{k:<20}{cells}")

if __name__=="__main__": main(sys.argv[1])
