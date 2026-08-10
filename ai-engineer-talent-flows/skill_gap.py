import os, json, urllib.request, urllib.parse, csv
key=os.environ["API_KEY"]; U="https://api.skillenai.com"
def post(path,body):
    req=urllib.request.Request(f"{U}{path}",data=json.dumps(body).encode(),
        headers={"X-API-Key":key,"Content-Type":"application/json"})
    return json.load(urllib.request.urlopen(req,timeout=120))
def tg(endpoint,**p):
    req=urllib.request.Request(f"{U}/v1/talent-graph/{endpoint}?{urllib.parse.urlencode(p)}",headers={"X-API-Key":key})
    return json.load(urllib.request.urlopen(req,timeout=120)).get("rows",[])
def sql(q):
    return post("/v1/query/sql",{"sql":q,"limit":400}).get("rows",[])

AIE_ROLES=["AI Engineer","Applied AI Engineer","Artificial Intelligence Engineer"]
# 3-level agg: nested -> terms(entityId) -> reverse_nested
ids_agg={"terms":{"field":"entities.resolved.entityId","size":500},"aggs":{"docs":{"reverse_nested":{}}}}
nested={"nested":{"path":"entities"},"aggs":{"ids":ids_agg}}
query={"bool":{"must":[{"terms":{"role.keyword":AIE_ROLES}}],
               "must_not":[{"term":{"companyCanonicalName.keyword":"Speechify"}}]}}
body={"indices":["prod-enriched-jobs"],"query":{"size":0,"track_total_hits":True,"query":query,"aggs":{"e":nested}}}
d=post("/v1/query/search",body)
tot=d["total"]
demand={b["key"]: b["docs"]["doc_count"]/tot for b in d["aggregations"]["e"]["ids"]["buckets"]}
print("AIE postings:",tot,"| demand entities:",len(demand))

supply={r["skill_id"]: r["prevalence"] for r in tg("skill-prevalence", role_id="dadf0773affc09e1", limit=400) if r.get("prevalence") is not None}
print("supply skills:",len(supply))

ids=set([k for k,_ in sorted(demand.items(),key=lambda x:-x[1])[:60]])|set(supply)
meta={r["entity_id"]:(r["canonical_name"],r["entity_type"]) for r in
      sql("SELECT entity_id, canonical_name, entity_type FROM skillenai.entities WHERE entity_id IN (%s)"%",".join("'%s'"%i for i in ids))}
KEEP={"skill","product"}
rows=[]
for i in ids:
    nm,typ=meta.get(i,(i[:8],"?"))
    if typ not in KEEP: continue
    rows.append((nm, 100*demand.get(i,0), 100*supply.get(i,0)))

OUT="/Users/jrand/git-repos/skillenai-notebooks/.claude/worktrees/ai-eng-graph/ai-engineer-talent-flows/skill_supply_demand.csv"
with open(OUT,"w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["skill","demand_pct","supply_pct"])
    for nm,dm,sp in sorted(rows,key=lambda x:-(x[1]+x[2])): w.writerow([nm,round(dm,1),round(sp,1)])

print("\n=== OVER-DEMANDED (employers ask >> workers list) ===")
for nm,dm,sp in sorted(rows,key=lambda x:-(x[1]-x[2]))[:15]:
    print(f"  {nm:26} demand {dm:5.1f}  supply {sp:5.1f}  gap +{dm-sp:5.1f}")
print("\n=== OVER-SUPPLIED (workers list >> employers ask) ===")
for nm,dm,sp in sorted(rows,key=lambda x:(x[1]-x[2]))[:12]:
    print(f"  {nm:26} demand {dm:5.1f}  supply {sp:5.1f}  gap {dm-sp:6.1f}")
print("\n=== ALIGNED (both prominent, gap small) ===")
for nm,dm,sp in sorted([r for r in rows if r[1]>7 and r[2]>7],key=lambda x:abs(x[1]-x[2]))[:8]:
    print(f"  {nm:26} demand {dm:5.1f}  supply {sp:5.1f}  gap {dm-sp:+5.1f}")
