"""Merge the mechanical extraction (mechanical.csv, signals.csv, fetch_log.csv,
seeds.csv) with the agent-graded judgment columns (/tmp/grading_out_*.json) into
the final platforms.csv deliverable, computing the derived boolean/float columns
deterministically rather than trusting agent arithmetic.
"""
import csv
import glob
import json
import re

AUDITED_AT = "2026-08-31"


def page_title(domain):
    try:
        with open(f"raw/{domain}__home.html", encoding="utf-8", errors="replace") as f:
            html_text = f.read()
    except FileNotFoundError:
        return domain
    m = re.search(r'<title[^>]*>(.*?)</title>', html_text, re.I | re.S)
    if not m:
        return domain
    t = re.sub(r'\s+', ' ', m.group(1)).strip()
    for sep in (" - ", " | ", " — ", " – "):
        if sep in t:
            t = t.split(sep)[0]
    return t.strip() or domain


def rel_bucket_ok(v):
    return v in {"dofollow", "nofollow", "sponsored", "sponsored+nofollow", "none_observed", "unknown"}


def main():
    with open("seeds.csv") as f:
        seeds = {r["domain"]: r for r in csv.DictReader(f)}
    with open("fetch_log.csv") as f:
        fl = list(csv.DictReader(f))
    home_status = {r["domain"]: r["http_status"] for r in fl if r["page"] == "home"}
    with open("signals.csv") as f:
        signals = {r["domain"]: r for r in csv.DictReader(f)}
    with open("mechanical.csv") as f:
        mech = {r["domain"]: r for r in csv.DictReader(f)}

    graded = {}
    for path in sorted(glob.glob("/tmp/grading_out_*.json")):
        with open(path) as f:
            for row in json.load(f):
                graded[row["domain"]] = row

    missing = set(seeds) - set(graded)
    if missing:
        print(f"WARNING: {len(missing)} domains missing graded output: {sorted(missing)}")

    fieldnames = [
        "platform", "domain", "audited_at", "http_status", "seed_list_count",
        "business_model", "paid_link_rel", "free_link_rel", "rel_inversion",
        "paid_passes_pagerank", "guarantees_dr", "guarantees_dr_quote",
        "badge_required_free", "claims_owned_network", "owner_entity",
        "network_id_ga", "network_id_other", "price_usd", "claimed_link_count",
        "price_per_link", "server_rendered_words", "js_required",
        "ai_crawlers_allowed", "claims_unsubmittable_platforms", "dark_patterns",
        "evidence_file", "notes",
    ]

    rows = []
    for domain in sorted(seeds):
        g = graded.get(domain, {})
        s = signals.get(domain, {})
        m = mech.get(domain, {})

        paid_rel = g.get("paid_link_rel", "unknown")
        free_rel = g.get("free_link_rel", "unknown")
        if not rel_bucket_ok(paid_rel):
            paid_rel = "unknown"
        if not rel_bucket_ok(free_rel):
            free_rel = "unknown"

        rel_inversion = (paid_rel == "dofollow" and free_rel in ("nofollow", "sponsored+nofollow", "sponsored"))
        paid_passes_pagerank = (paid_rel == "dofollow")

        price_usd = g.get("price_usd", "unknown")
        claimed_link_count = g.get("claimed_link_count", "unknown")
        price_per_link = ""
        try:
            p = float(price_usd)
            c = float(claimed_link_count)
            if c > 0:
                price_per_link = round(p / c, 4)
        except (TypeError, ValueError):
            price_per_link = ""

        network_id_other = ";".join(x for x in [
            s.get("stripe_pk_keys", ""),
            (f"ip:{s['resolved_ip']}" if s.get("resolved_ip") else ""),
            (f"favicon:{s['favicon_sha256'][:16]}" if s.get("favicon_sha256") else ""),
        ] if x)

        owner_entity = g.get("owner_entity") or s.get("owner_entity_footer") or s.get("registrant_org") or ""

        js_required = m.get("js_required", "")
        ai_allowed = m.get("ai_crawlers_allowed", "")

        rows.append({
            "platform": page_title(domain),
            "domain": domain,
            "audited_at": AUDITED_AT,
            "http_status": home_status.get(domain, "unknown"),
            "seed_list_count": seeds[domain]["seed_list_count"],
            "business_model": g.get("business_model", "unclear"),
            "paid_link_rel": paid_rel,
            "free_link_rel": free_rel,
            "rel_inversion": rel_inversion,
            "paid_passes_pagerank": paid_passes_pagerank,
            "guarantees_dr": bool(g.get("guarantees_dr", False)),
            "guarantees_dr_quote": g.get("guarantees_dr_quote", ""),
            "badge_required_free": bool(g.get("badge_required_free", False)),
            "claims_owned_network": bool(g.get("claims_owned_network", False)),
            "owner_entity": owner_entity,
            "network_id_ga": s.get("ga_gtm_ids", ""),
            "network_id_other": network_id_other,
            "price_usd": price_usd,
            "claimed_link_count": claimed_link_count,
            "price_per_link": price_per_link,
            "server_rendered_words": m.get("server_rendered_words", ""),
            "js_required": js_required,
            "ai_crawlers_allowed": ai_allowed,
            "claims_unsubmittable_platforms": bool(g.get("claims_unsubmittable_platforms", False)),
            "dark_patterns": g.get("dark_patterns", ""),
            "evidence_file": f"raw/{domain}__*.html (not committed; kept locally)",
            "notes": g.get("notes", ""),
        })

    with open("platforms.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote platforms.csv with {len(rows)} rows")


if __name__ == "__main__":
    main()
