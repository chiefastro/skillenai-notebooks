#!/usr/bin/env python3
"""Collect a labelled calibration set for the slop judge.

  slop_2026      : articles from 332 domains in the content-farm denylist (dev.to
                   excluded -- it is a legitimate community mislabelled in the seed).
                   Label quality: DOMAIN-level, not article-level.
  human_pre2022  : articles published on or before 2021-12-31. Definitionally
                   human -- ChatGPT launched 2022-11-30. The only true ground truth here.
  mainstream_2026: 2026 articles from non-denylist domains with domainAuthority.
                   Era-matched to the slop set; label is "presumed mostly human",
                   NOT ground truth -- these authors have the same tools available.
"""
import os
DATA = os.environ.get("PRP_DATA", "_data")   # collected notes; override with PRP_DATA
OUT  = os.environ.get("PRP_OUT", ".")       # figures/CSVs written here
import json,urllib.request,csv,time,random,sys
KEY=os.environ.get("SKILLENAI_INSIGHTS_API_KEY") or next(
    l.split("=",1)[1].strip() for l in open(os.environ.get("PRP_ENV",".env"))
    if l.startswith("SKILLENAI_INSIGHTS_API_KEY="))
DENY=[r['domain'] for r in csv.DictReader(open(
  os.environ.get("PRP_DENYLIST","../synthetic-breakout-may-2026/network_domains_seed.csv")))]
DENY=[d for d in DENY if d!="dev.to"]
OUT=f"{DATA}/calib.jsonl"
FIELDS=["extractedText","title","domain","publishedAt","author"]

def q(body):
    for a in range(4):
        try:
            req=urllib.request.Request("https://api.skillenai.com/v1/query/search",
                data=json.dumps(body).encode(),
                headers={"X-API-Key":KEY,"Content-Type":"application/json"})
            return json.loads(urllib.request.urlopen(req,timeout=120).read())
        except Exception as e:
            if a==3: print("  ERR",str(e)[:90],flush=True); return {}
            time.sleep(6*(a+1))

def pull(label,query,target=320):
    got=[];frm=0
    while len(got)<target and frm<2000:
        d=q({"query":{"size":100,"from":frm,"query":query,"_source":FIELDS,
                      "sort":[{"documentId":"asc"}]},"indices":["prod-enriched-blog"]})
        h=d.get("hits",[])
        if not h: break
        for x in h:
            t=x.get("extractedText") or ""
            if 1500<=len(t)<=9000:
                got.append({"label":label,"domain":x.get("domain"),
                            "publishedAt":x.get("publishedAt"),"title":x.get("title"),
                            "text":t})
        frm+=len(h); time.sleep(1.6)
    print(f"  {label:18s} {len(got)}",flush=True)
    return got[:target]

rows=[]
# slop: chunk the denylist to stay under the WAF body limit, take a slice per chunk
per=max(1,320//6)
for i in range(0,len(DENY),60):
    rows+=pull("slop_2026",{"terms":{"domain":DENY[i:i+60]}},per)
rows+=pull("human_pre2022",{"bool":{
    "must":[{"range":{"publishedAt":{"lte":"2021-12-31"}}}],
    "must_not":[{"terms":{"domain":DENY[:60]}}]}},320)
rows+=pull("mainstream_2026",{"bool":{
    "must":[{"range":{"publishedAt":{"gte":"2026-01-01"}}},
            {"exists":{"field":"domainAuthority"}}],
    "must_not":[{"terms":{"domain":DENY[:60]}}]}},320)
random.seed(4); random.shuffle(rows)
with open(OUT,"w") as f:
    for i,r in enumerate(rows): r["cid"]=f"C{i:04d}"; f.write(json.dumps(r)+"\n")
import collections
print("\nCOLLECTED:",dict(collections.Counter(r["label"] for r in rows)))
