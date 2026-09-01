"""Scrape meta-lists of launch platforms, dedupe with known seeds, cap the crawl set.

Writes seeds.csv with columns: domain, seed_list_count, seed_lists (semicolon list),
forced (bool - was in the plan's known-seed list regardless of meta-list appearance).
"""
import csv
import re
import time
import urllib.request
import urllib.error
from collections import defaultdict

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

META_LISTS = [
    "https://makerhunt.io/places-to-launch",
    "https://launchigniter.com/submit-directories",
    "https://www.scrolllaunch.com/directories",
    "https://launchdirectories.com/",
]

KNOWN_SEEDS = [
    # directories / launch platforms
    "producthunt.com", "betalist.com", "peerpush.com", "uneed.best",
    "tinylaunch.com", "trustmrr.com", "indiehackers.com", "alternativeto.net",
    "saashub.com", "f6s.com", "startupa.ge", "huntscreens.com", "listmy.site",
    "scrolllaunch.com", "launchigniter.com", "launchdirectories.com",
    "launchpanda.dev", "launchllama.co",
    # known operator network
    "postingdude.com", "makerhunt.io", "auraplusplus.com", "earlyhunt.com",
    "indiehunt.io", "sidehunt.io", "uno.directory",
    # submission services
    "startupsubmit.app", "submitsaas.com", "listingbott.com",
    # outranking / bidding
    "outbid.lol",
]

CAP = 60

DOMAIN_RE = re.compile(
    r'https?://(?:www\.)?([a-z0-9][a-z0-9-]*(?:\.[a-z0-9][a-z0-9-]*)+)', re.I
)

# domains that are infrastructure/social/generic, not launch platforms themselves
SKIP_DOMAINS = {
    # infra / social / generic tooling picked up incidentally (share buttons, badges,
    # analytics beacons, "as seen on HN/YC" marketing copy) -- not launch platforms
    "google.com", "twitter.com", "x.com", "facebook.com", "linkedin.com",
    "github.com", "youtube.com", "instagram.com", "cloudflare.com",
    "cloudflareinsights.com", "vercel.app", "vercel.com", "fonts.googleapis.com",
    "fonts.gstatic.com", "schema.org", "w3.org", "gstatic.com",
    "googletagmanager.com", "google-analytics.com", "stripe.com",
    "makerhunt.io", "launchigniter.com", "scrolllaunch.com",
    "launchdirectories.com",  # the meta-lists themselves
    "bsky.app", "chatgpt.com", "claude.ai", "reddit.com", "techcrunch.com",
    "ycombinator.com", "news.ycombinator.com", "ahrefs.com", "sourceforge.net",
    "perplexity.ai", "datafa.st", "rybbit.io", "app.rybbit.io", "openai.com",
    "anthropic.com",
}


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.read().decode("utf-8", errors="replace"), resp.status
    except urllib.error.HTTPError as e:
        return e.read().decode("utf-8", errors="replace"), e.code
    except Exception as e:
        return "", f"ERROR:{e}"


def apex(domain):
    parts = domain.lower().split(".")
    if len(parts) <= 2:
        return domain.lower()
    # keep common two-part TLDs simple; this is a heuristic, good enough for launch-site domains
    return ".".join(parts[-2:]) if parts[-2] not in {"co", "com", "org", "gov"} or len(parts) == 2 else ".".join(parts[-3:]) if parts[-2] in {"co"} else ".".join(parts[-2:])


def main():
    counts = defaultdict(set)  # domain -> set of source list urls
    for url in META_LISTS:
        html, status = fetch(url)
        print(f"fetched {url} -> {status}, {len(html)} bytes")
        found = set()
        for m in DOMAIN_RE.finditer(html):
            d = apex(m.group(1))
            if d in SKIP_DOMAINS:
                continue
            found.add(d)
        for d in found:
            counts[d].add(url)
        time.sleep(1.5)

    rows = []
    all_domains = set(counts.keys()) | set(KNOWN_SEEDS)
    print(f"total unique domains before cap: {len(all_domains)}")
    for d in all_domains:
        rows.append({
            "domain": d,
            "seed_list_count": len(counts.get(d, set())),
            "seed_lists": ";".join(sorted(counts.get(d, set()))),
            "forced": d in KNOWN_SEEDS,
        })

    # sort: forced seeds first, then by seed_list_count desc
    rows.sort(key=lambda r: (not r["forced"], -r["seed_list_count"], r["domain"]))
    rows = rows[:CAP]
    rows.sort(key=lambda r: r["domain"])

    with open("seeds.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["domain", "seed_list_count", "seed_lists", "forced"])
        w.writeheader()
        w.writerows(rows)

    print(f"wrote {len(rows)} seed domains to seeds.csv")


if __name__ == "__main__":
    main()
