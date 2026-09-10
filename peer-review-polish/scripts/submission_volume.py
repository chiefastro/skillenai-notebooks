#!/usr/bin/env python3
import os
DATA = os.environ.get("PRP_DATA", "_data")   # collected notes; override with PRP_DATA
OUT  = os.environ.get("PRP_OUT", ".")       # figures/CSVs written here
"""Venue volume time series from public OpenReview data.

submissions   : German tank estimator on Submission<N> in reviewer signatures.
                Counts submission SLOTS (includes withdrawn/desk-rejected), so it
                runs above published accept-track figures. Ratios are the usable part.
reviews/paper : our corpus is term-sampled, so a raw mean is a lower bound. Instead we
                fit a zero-truncated binomial: if a paper has R reviews and each is
                sampled independently w.p. p, the observed per-forum counts (conditioned
                on >=1) identify R and p jointly. Grid-search MLE.
"""
import json, glob, re, collections, math

def load():
    seen={}
    for p in glob.glob(f"{DATA}/*.jsonl"):
        for l in open(p):
            try: r=json.loads(l)
            except Exception: continue
            if r.get("id"): seen[r["id"]]=r
    return list(seen.values())

rows=load()
sub=collections.defaultdict(set); fo=collections.defaultdict(lambda: collections.Counter())
for r in rows:
    if r["kind"]!="Official_Review": continue
    d=r.get("domain") or "?"
    for s in (r.get("signatures") or []):
        m=re.search(r"/Submission(\d+)/",s)
        if m: sub[d].add(int(m.group(1)))
    if r.get("forum"): fo[d][r["forum"]]+=1

def ztb_fit(counts):
    """counts: Counter of observed reviews-per-forum (>=1). Grid MLE over R,p."""
    dist=collections.Counter(counts.values())
    obs=[(k,v) for k,v in dist.items() if k>=1]
    n=sum(v for _,v in obs)
    best=None
    for R in range(2,9):
        for pi in range(1,200):
            p=pi/200
            if p>=1: continue
            denom=1-(1-p)**R
            if denom<=1e-9: continue
            ll=0
            for k,v in obs:
                if k>R: ll=-1e18; break
                pk=math.comb(R,k)*p**k*(1-p)**(R-k)/denom
                if pk<=0: ll=-1e18; break
                ll+=v*math.log(pk)
            if best is None or ll>best[0]: best=(ll,R,p)
    return best

print(f"{'venue':<34}{'k subs seen':>12}{'max sub#':>10}{'est. submissions':>18}"
      f"{'forums seen':>13}{'fit R':>7}{'fit p':>7}")
out={}
for d in sorted(sub, key=lambda x:-len(sub[x])):
    u=sorted(sub[d]); k=len(u)
    if k<40: continue
    mx=max(u); est=mx*(k+1)/k-1
    f=ztb_fit(fo[d]); R=f[1] if f else None; p=f[2] if f else None
    out[d]=dict(est=est,R=R,p=p,forums=len(fo[d]))
    print(f"{d:<34}{k:>12,}{mx:>10,}{est:>18,.0f}{len(fo[d]):>13,}{R:>7}{p:>7.2f}")

print("\n=== ICLR time series ===")
print(f"{'year':<7}{'est. submissions':>18}{'growth':>9}{'fit reviews/paper':>19}")
prev=None
for y in (2024,2025,2026):
    d=f"ICLR.cc/{y}/Conference"
    if d not in out: continue
    o=out[d]; g=f"{o['est']/prev:.2f}x" if prev else "-"
    print(f"{y:<7}{o['est']:>18,.0f}{g:>9}{o['R']:>19}")
    prev=o['est']
print("\n=== NeurIPS time series ===")
prev=None
for y in (2023,2024,2025):
    d=f"NeurIPS.cc/{y}/Conference"
    if d not in out: continue
    o=out[d]; g=f"{o['est']/prev:.2f}x" if prev else "-"
    print(f"{y:<7}{o['est']:>18,.0f}{g:>9}{o['R']:>19}")
    prev=o['est']
