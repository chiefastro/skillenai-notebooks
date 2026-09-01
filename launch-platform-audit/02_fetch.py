"""Fetch homepage, /pricing, /submit, /robots.txt for every seed domain.

Polite crawling: requests to the SAME host are sequential with a 1-2s delay.
Different hosts may run concurrently (bounded worker pool) since that maps to
independent web servers, not a single target being hammered.

Writes raw/<domain>__<page>.html for each fetch and a fetch_log.csv summary
(domain, page, url, http_status, bytes).
"""
import csv
import os
import random
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

PAGES = [
    ("home", ""),
    ("pricing", "/pricing"),
    ("submit", "/submit"),
    ("robots", "/robots.txt"),
]

RAW_DIR = "raw"
MAX_WORKERS = 8


def fetch_one(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read()
            return resp.status, body
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:
        return f"ERROR:{e}", b""


def fetch_domain(domain):
    rows = []
    for page_name, path in PAGES:
        url = f"https://{domain}{path}"
        status, body = fetch_one(url)
        # www fallback if apex fails outright (connection error, not http error)
        if isinstance(status, str) and status.startswith("ERROR") and not path:
            url2 = f"https://www.{domain}{path}"
            status2, body2 = fetch_one(url2)
            if not (isinstance(status2, str) and status2.startswith("ERROR")):
                url, status, body = url2, status2, body2
        fname = f"{RAW_DIR}/{domain}__{page_name}.html"
        with open(fname, "wb") as f:
            f.write(body)
        rows.append({
            "domain": domain, "page": page_name, "url": url,
            "http_status": status, "bytes": len(body),
        })
        time.sleep(1.2 + random.random() * 0.6)  # polite delay, same host sequential
    return rows


def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    with open("seeds.csv") as f:
        domains = [r["domain"] for r in csv.DictReader(f)]

    all_rows = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {ex.submit(fetch_domain, d): d for d in domains}
        for fut in as_completed(futures):
            d = futures[fut]
            try:
                rows = fut.result()
                all_rows.extend(rows)
                statuses = [r["http_status"] for r in rows]
                print(f"{d}: {statuses}")
            except Exception as e:
                print(f"{d}: FAILED {e}")

    with open("fetch_log.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["domain", "page", "url", "http_status", "bytes"])
        w.writeheader()
        w.writerows(all_rows)
    print(f"done. {len(all_rows)} fetches logged.")


if __name__ == "__main__":
    main()
