"""Supplementary polite fetch of /privacy and /terms for owner-entity extraction."""
import csv
import os
import random
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
PAGES = [("privacy", "/privacy"), ("terms", "/terms")]
RAW_DIR = "raw"
MAX_WORKERS = 8


def fetch_one(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:
        return f"ERROR:{e}", b""


def fetch_domain(domain):
    rows = []
    for name, path in PAGES:
        status, body = fetch_one(f"https://{domain}{path}")
        with open(f"{RAW_DIR}/{domain}__{name}.html", "wb") as f:
            f.write(body)
        rows.append({"domain": domain, "page": name, "http_status": status, "bytes": len(body)})
        time.sleep(1.2 + random.random() * 0.6)
    return rows


def main():
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
                print(f"{d}: {[r['http_status'] for r in rows]}")
            except Exception as e:
                print(f"{d}: FAILED {e}")
    with open("fetch_legal_log.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["domain", "page", "http_status", "bytes"])
        w.writeheader()
        w.writerows(all_rows)
    print("done")


if __name__ == "__main__":
    main()
