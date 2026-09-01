"""Collect ownership/network signals per domain and emit network_graph.csv.

Signals collected per domain:
  - whois registrant org, creation date, registrar
  - GA/GTM IDs and Stripe publishable keys found in fetched HTML
  - resolved A record IP
  - favicon SHA-256
  - owner entity strings found in /privacy, /terms text (best-effort, footer text)

Then emits edges between domains that share a signal, with a confidence tier:
  high   - shared GA ID, shared Stripe key, or an explicit ownership statement
  medium - shared IP AND shared registrant org
  low    - cross-linking between audited domains only

Also writes signals.csv (one row per domain) as the evidence backing the edges.
"""
import csv
import hashlib
import json
import re
import subprocess
import time
import urllib.request
import urllib.error
from itertools import combinations

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

GA_RE = re.compile(r'(G-[A-Z0-9]{8,}|GTM-[A-Z0-9]+|UA-\d+-\d+)')
STRIPE_RE = re.compile(r'pk_live_[A-Za-z0-9]+')


def read_raw(domain, page):
    try:
        with open(f"raw/{domain}__{page}.html", "rb") as f:
            return f.read().decode("utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def whois_lookup(domain):
    try:
        out = subprocess.run(["whois", domain], capture_output=True, text=True, timeout=15)
        text = out.stdout
    except Exception:
        return {"registrant_org": "", "registrar": "", "creation_date": ""}
    org = re.search(r'(?im)^(?:registrant organization|org(?:anization)?):\s*(.+)$', text)
    registrar = re.search(r'(?im)^registrar:\s*(.+)$', text)
    created = re.search(r'(?im)^(?:creation date|created(?: on)?|domain registration date):\s*(.+)$', text)
    return {
        "registrant_org": (org.group(1).strip() if org else ""),
        "registrar": (registrar.group(1).strip() if registrar else ""),
        "creation_date": (created.group(1).strip() if created else ""),
    }


def dig_a(domain):
    try:
        out = subprocess.run(["dig", "+short", "A", domain], capture_output=True, text=True, timeout=10)
        ips = [l.strip() for l in out.stdout.splitlines() if l.strip() and not l.strip().endswith(".")]
        return ips[0] if ips else ""
    except Exception:
        return ""


def favicon_hash(domain):
    for url in (f"https://{domain}/favicon.ico", f"https://www.{domain}/favicon.ico"):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                if len(data) < 50:  # too small to be a real favicon (likely error page)
                    continue
                return hashlib.sha256(data).hexdigest()
        except Exception:
            continue
    return ""


def owner_entity_strings(domain):
    """Best-effort: pull footer/privacy copyright lines out of already-fetched home page."""
    html = read_raw(domain, "home")
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text)
    hits = re.findall(r'(?:©|Copyright)\s*(?:\d{4}\s*)?([A-Z][A-Za-z0-9 ,.&\'-]{2,60}?)(?:\.|,|\s+All rights)', text)
    return "; ".join(sorted(set(h.strip() for h in hits)))[:300]


OWNERSHIP_PATTERNS = [
    re.compile(r'own(?:ed|s)?\s+(?:\d+\s+)?platforms?', re.I),
    re.compile(r'our\s+network\s+of', re.I),
    re.compile(r'sister\s+sites?', re.I),
    re.compile(r'we\s+also\s+own', re.I),
]


def page_title(domain):
    html_text = read_raw(domain, "home")
    m = re.search(r'<title[^>]*>(.*?)</title>', html_text, re.I | re.S)
    if not m:
        return ""
    t = re.sub(r'\s+', ' ', m.group(1)).strip()
    for sep in (" - ", " | ", " — ", " – "):
        if sep in t:
            t = t.split(sep)[0]
    return t.strip()


OWNED_LIST_STOP = re.compile(
    r'\bplus\b|more distribution|additional distribution|'
    r'\bwhen it\b|\bwhen they\b|["\.]', re.I
)


def explicit_ownership_edges(domains):
    """Find self-declared ownership-of-multiple-platforms statements and match
    the named platforms against other audited domains by brand name / title.

    Only names inside the bounded "owned platforms" list are matched -- text
    after a stop phrase like "plus more distribution on X, Y" describes
    non-owned channels and must not be linked as owned.
    """
    brand_map = {d: page_title(d) for d in domains}
    edges = {}  # (d, other) -> (quote, confidence) -- dedupe repeated JSON-LD blocks
    for d in domains:
        text_all = " ".join(read_raw(d, p) for p in ("home", "pricing", "submit"))
        text_all = re.sub(r'<[^>]+>', ' ', text_all)
        text_all = re.sub(r'\s+', ' ', text_all)
        for pat in OWNERSHIP_PATTERNS:
            for m in pat.finditer(text_all):
                tail = text_all[m.end():m.end() + 300]
                stop = OWNED_LIST_STOP.search(tail)
                owned_list_text = tail[:stop.start()] if stop else tail[:150]
                quote = (text_all[max(0, m.start() - 20):m.end()] + owned_list_text).strip()[:220]
                for other in domains:
                    if other == d:
                        continue
                    brand = brand_map.get(other, "")
                    label = other.split(".")[0]

                    def norm(s):
                        return s.lower().replace(" ", "").replace("++", "plusplus").replace("+", "plus")

                    haystack = norm(owned_list_text)
                    if (brand and len(brand) > 2 and norm(brand) in haystack) or \
                       (len(label) > 3 and label.lower() in haystack):
                        key = (d, other)
                        if key not in edges:
                            edges[key] = (quote, "high")
    return [(d, other, "explicit_ownership_statement", quote, conf)
            for (d, other), (quote, conf) in edges.items()]


def main():
    with open("seeds.csv") as f:
        domains = [r["domain"] for r in csv.DictReader(f)]

    signals = []
    for i, d in enumerate(domains):
        print(f"[{i+1}/{len(domains)}] signals for {d}")
        w = whois_lookup(d)
        ip = dig_a(d)
        fav = favicon_hash(d)
        owner = owner_entity_strings(d)

        html_all = " ".join(read_raw(d, p) for p in ("home", "pricing", "submit"))
        ga_ids = sorted(set(GA_RE.findall(html_all)))
        stripe_keys = sorted(set(STRIPE_RE.findall(html_all)))

        signals.append({
            "domain": d,
            "registrant_org": w["registrant_org"],
            "registrar": w["registrar"],
            "creation_date": w["creation_date"],
            "resolved_ip": ip,
            "favicon_sha256": fav,
            "owner_entity_footer": owner,
            "ga_gtm_ids": ";".join(ga_ids),
            "stripe_pk_keys": ";".join(stripe_keys),
        })
        time.sleep(0.3)

    with open("signals.csv", "w", newline="") as f:
        fieldnames = list(signals[0].keys())
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(signals)
    print("wrote signals.csv")

    # --- build edges ---
    edges = []
    by_domain = {s["domain"]: s for s in signals}
    for a, b in combinations(domains, 2):
        sa, sb = by_domain[a], by_domain[b]

        ga_a = set(x for x in sa["ga_gtm_ids"].split(";") if x)
        ga_b = set(x for x in sb["ga_gtm_ids"].split(";") if x)
        shared_ga = ga_a & ga_b
        if shared_ga:
            edges.append((a, b, "ga_gtm_id", ";".join(sorted(shared_ga)), "high"))

        sk_a = set(x for x in sa["stripe_pk_keys"].split(";") if x)
        sk_b = set(x for x in sb["stripe_pk_keys"].split(";") if x)
        shared_sk = sk_a & sk_b
        if shared_sk:
            edges.append((a, b, "stripe_pk", ";".join(sorted(shared_sk)), "high"))

        if sa["resolved_ip"] and sa["resolved_ip"] == sb["resolved_ip"]:
            same_registrant = (sa["registrant_org"] and sa["registrant_org"] == sb["registrant_org"])
            conf = "medium" if same_registrant else "low"
            edges.append((a, b, "shared_ip", sa["resolved_ip"], conf))

        if sa["favicon_sha256"] and sa["favicon_sha256"] == sb["favicon_sha256"]:
            edges.append((a, b, "favicon_hash", sa["favicon_sha256"][:16], "medium"))

    edges.extend(explicit_ownership_edges(domains))

    with open("network_graph.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["domain_a", "domain_b", "shared_signal", "signal_value", "confidence"])
        w.writerows(edges)
    print(f"wrote network_graph.csv with {len(edges)} edges")


if __name__ == "__main__":
    main()
