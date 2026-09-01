"""Mechanical extraction pass over raw/ HTML: rel-attribute link classification,
visible-word counts, JS-required flag, and AI-crawler robots.txt admission.

This does NOT decide business_model / dark_patterns / owner_entity (those need
contextual judgment against raw HTML and are handled in 03_grade.py by a human-
reviewed pass, per the plan's "do not guess" rule). This script produces the
mechanical columns and a per-domain link dump (raw/<domain>__links.json) that the
grading pass reads to make the paid-vs-free call.
"""
import csv
import html
import json
import re

PAID_CONTEXT_WORDS = re.compile(
    r'\b(premium|featured|spotlight|sponsored|promoted|boost(?:ed)?|paid)\b', re.I
)


def read_raw(domain, page):
    try:
        with open(f"raw/{domain}__{page}.html", "rb") as f:
            return f.read().decode("utf-8", errors="replace")
    except FileNotFoundError:
        return None


def apex_variants(domain):
    return {domain, f"www.{domain}"}


def outbound_rels(html_text, own_domain):
    own = re.escape(own_domain)
    out = []
    for m in re.finditer(r'<a\b([^>]*)>', html_text):
        tag = m.group(1)
        hm = re.search(r'href="(https?://(?!(?:www\.)?%s)[^"]+)"' % own, tag)
        if not hm:
            continue
        rel = re.search(r'rel="([^"]*)"', tag)
        out.append({"rel": rel.group(1) if rel else "", "href": hm.group(1)})
    return out


def context_window(html_text, match_start, window=400):
    start = max(0, match_start - window)
    return html_text[start:match_start]


def classify_link_context(html_text, own_domain):
    """Return list of dicts: rel, href, context ('paid'/'free'/'unknown')."""
    own = re.escape(own_domain)
    results = []
    for m in re.finditer(r'<a\b([^>]*)>', html_text):
        tag = m.group(1)
        hm = re.search(r'href="(https?://(?!(?:www\.)?%s)[^"]+)"' % own, tag)
        if not hm:
            continue
        rel = re.search(r'rel="([^"]*)"', tag)
        rel_val = rel.group(1) if rel else ""
        ctx_text = context_window(html_text, m.start())
        is_paid = bool(PAID_CONTEXT_WORDS.search(ctx_text[-250:]))
        results.append({
            "rel": rel_val,
            "href": hm.group(1),
            "context_flag": "paid" if is_paid else "unspecified",
        })
    return results


def rel_bucket(rel_val):
    if rel_val is None:
        return "unknown"
    tokens = set(rel_val.lower().split())
    has_sponsored = "sponsored" in tokens
    has_nofollow = "nofollow" in tokens
    if has_sponsored and has_nofollow:
        return "sponsored+nofollow"
    if has_sponsored:
        return "sponsored"
    if has_nofollow:
        return "nofollow"
    if rel_val.strip() == "":
        return "dofollow"
    return "dofollow"  # rel present but has neither sponsored nor nofollow (e.g. noopener only)


def visible_words(html_text):
    h2 = re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>', ' ', html_text)
    text = re.sub(r'<[^>]+>', ' ', h2)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return len(text.split()) if text else 0


def ai_crawlers_allowed(robots_text):
    if not robots_text or not robots_text.strip():
        return None  # unknown -- no robots.txt fetched/found
    bots = ["GPTBot", "ClaudeBot", "PerplexityBot", "anthropic-ai", "Google-Extended"]
    # naive parse: find each bot's User-agent block, check for "Disallow: /"
    blocks = re.split(r'(?im)^user-agent:', robots_text)
    disallowed_bots = set()
    for block in blocks[1:]:
        lines = block.strip().splitlines()
        if not lines:
            continue
        agent = lines[0].strip()
        directives = "\n".join(lines[1:])
        if re.search(r'(?im)^disallow:\s*/\s*$', directives):
            disallowed_bots.add(agent)
    for bot in bots:
        if bot in disallowed_bots:
            return False
    return True


def main():
    with open("seeds.csv") as f:
        domains = [r["domain"] for r in csv.DictReader(f)]

    rows = []
    for d in domains:
        home = read_raw(d, "home")
        submit = read_raw(d, "submit")
        pricing = read_raw(d, "pricing")
        robots = read_raw(d, "robots")

        # prefer the page most likely to list outbound member sites: home, then submit
        listing_html = home if home else (submit or "")
        words = visible_words(listing_html) if listing_html else 0
        js_required = (words < 150) if listing_html else None

        links_home = classify_link_context(home, d) if home else []
        links_submit = classify_link_context(submit, d) if submit else []
        links_pricing = classify_link_context(pricing, d) if pricing else []

        with open(f"raw/{d}__links.json", "w") as jf:
            json.dump({
                "home": links_home, "submit": links_submit, "pricing": links_pricing,
            }, jf, indent=1)

        ai_allowed = ai_crawlers_allowed(robots) if robots is not None else None

        rows.append({
            "domain": d,
            "server_rendered_words": words,
            "js_required": js_required,
            "ai_crawlers_allowed": ai_allowed,
            "n_outbound_links_home": len(links_home),
            "n_outbound_links_submit": len(links_submit),
        })

    with open("mechanical.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote mechanical.csv and raw/*__links.json for {len(rows)} domains")


if __name__ == "__main__":
    main()
