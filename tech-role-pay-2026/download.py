"""Download US-USD salaried postings via documentId-range pagination.
Globally rate-limited to the measured 50 req/min query tier. Fails LOUDLY."""
import json, os, sys, time, threading
import urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

API = "https://api.skillenai.com/v1/query/search"
KEY = os.environ["API_KEY"]
OUT = sys.argv[1]
WORKERS = 3
RPM = 44.0                       # stay under the 50/min query tier

FIELDS = ["role","title","salaryMin","salaryMax","salaryCurrency","seniorityLevel",
          "companyCanonicalName","locationAdmin1","locationCity","platform","workModel",
          "sector","postedAt","postedAtSource"]
BASE = [{"term":{"locationCountry":"US"}},{"term":{"salaryCurrency":"USD"}},
        {"exists":{"field":"salaryMin"}},{"exists":{"field":"salaryMax"}}]

_tl = threading.Lock(); _next = [0.0]
def gate():
    """Global token gate: at most RPM requests per minute across all threads."""
    with _tl:
        now = time.monotonic()
        t = max(now, _next[0])
        _next[0] = t + 60.0/RPM
    d = t - time.monotonic()
    if d > 0: time.sleep(d)

lock = threading.Lock(); rows = []; out = open(OUT+".part","w")

def post(body, tries=8):
    data = json.dumps(body).encode()
    last = None
    for i in range(tries):
        gate()
        req = urllib.request.Request(API, data=data,
            headers={"X-API-Key":KEY,"Content-Type":"application/json"})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}: {e.read()[:300]!r}"
            if e.code in (429,500,502,503,504):
                time.sleep(min(60, 5*(2**i))); continue
            raise RuntimeError(last)
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
            time.sleep(min(60, 5*(2**i))); continue
    raise RuntimeError(f"exhausted retries; last error = {last}")

def shard(hexchar):
    hi = chr(ord(hexchar)+1) if hexchar != 'f' else None
    got = 0; cursor = None
    while True:
        rng = {"gt": cursor} if cursor else {"gte": hexchar}
        if hi: rng["lt"] = hi
        body = {"query":{"size":100,"sort":[{"documentId":"asc"}],"_source":FIELDS,
                         "query":{"bool":{"filter":BASE+[{"range":{"documentId":rng}}]}}},
                "indices":["prod-enriched-jobs"]}
        hits = post(body).get("hits",[])
        if not hits: break
        with lock:
            for h in hits:
                h["_docid"] = h["_id"]; out.write(json.dumps(h)+"\n")
            out.flush(); rows.append(len(hits)); got += len(hits)
            print(f"shard {hexchar}: +{len(hits)} (shard {got}, grand {sum(rows)*1})", flush=True)
        cursor = hits[-1]["_id"]
        if len(hits) < 100: break
    print(f"SHARD {hexchar} DONE: {got}", flush=True)

with ThreadPoolExecutor(max_workers=WORKERS) as ex:
    futs = [ex.submit(shard, c) for c in "0123456789abcdef"]
    for f in futs: f.result()          # re-raise loudly
out.close()
os.rename(OUT+".part", OUT)
print("wrote", sum(l for l in rows), "->", OUT, flush=True)
