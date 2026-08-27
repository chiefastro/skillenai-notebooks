#!/usr/bin/env python3
"""Step 4 — the demand side: how employers actually write about AI in postings.

Three questions:
  1. What share of postings mention AI at all?
  2. Do employers describe *themselves* as AI-native, or ask *candidates* for
     AI proficiency? (the tiebreaker-vs-filter question)
  3. Do they name specific products, or ask for generic fluency?

Corpus caveat: the jobs index only starts 2026-03-10, so there is no YoY series
here. Every figure is a within-window share, which is robust to crawler coverage
bias in a way absolute volumes are not.

Spam filter: Speechify carpet-bombs the same ~10 roles across hundreds of
cities and is excluded from every denominator.

Output: demand_side_stats.csv

Usage:
    source .env
    python 04_demand_side_postings.py
"""
import csv
import json
import os
import time
import urllib.request

API_URL = os.environ.get("API_URL", "https://api.skillenai.com")
API_KEY = os.environ["SKILLENAI_INSIGHTS_API_KEY"]

WINDOW = {"range": {"postedAt": {"gte": "2026-03-01"}}}
SPAM = {"terms": {"companyCanonicalName.keyword": ["Speechify"]}}

# Deliberately excluded as AI signals despite scoring high: "Claude" (a common
# French given name), "Cursor" (UI and database cursors) and "Gemini" (zodiac
# sign / unrelated product lines). Entity-name collisions, not AI mentions.
AI_TERMS = [
    "generative AI", "artificial intelligence", "machine learning", "prompt engineering",
    "AI tools", "AI-assisted", "AI agents", "ChatGPT", "GitHub Copilot", "LangChain",
    "large language model", "AI fluency", "AI literacy",
]
SELF_DESCRIPTION = ["AI-native", "AI-first", "leverage AI", "AI-powered"]
CANDIDATE_REQUIREMENT = [
    "proficiency with AI", "experience with AI tools", "familiarity with AI",
    "comfortable using AI", "hands-on with AI",
]
GENERIC_FLUENCY = ["AI tools", "AI-assisted", "generative AI", "prompt engineering"]
NAMED_PRODUCTS = ["ChatGPT", "GitHub Copilot", "LangChain", "Midjourney", "Hugging Face"]

DEPARTMENTS = [
    "Engineering", "Product", "Marketing", "Design", "Sales", "Finance",
    "Customer Success", "Data Science",
]


def search(body: dict) -> dict:
    req = urllib.request.Request(
        f"{API_URL}/v1/query/search",
        data=json.dumps({"query": body, "indices": ["prod-enriched-jobs"]}).encode(),
        headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
    )
    return json.load(urllib.request.urlopen(req))


def count(must: list) -> int:
    return search({
        "size": 0, "track_total_hits": True,
        "query": {"bool": {"must": [WINDOW] + must, "must_not": [SPAM]}},
    })["total"]


def any_of(terms: list[str]) -> dict:
    return {"bool": {"should": [{"match_phrase": {"extractedText": t}} for t in terms],
                     "minimum_should_match": 1}}


def main() -> None:
    rows = []
    base = count([])
    ai = count([any_of(AI_TERMS)])
    rows.append(["baseline_postings", base, ""])
    rows.append(["any_ai_mention", ai, round(100 * ai / base, 2)])

    self_n = count([any_of(SELF_DESCRIPTION)])
    req_n = count([any_of(CANDIDATE_REQUIREMENT)])
    rows.append(["employer_self_description", self_n, round(100 * self_n / base, 2)])
    rows.append(["candidate_requirement", req_n, round(100 * req_n / base, 2)])

    generic = count([any_of(GENERIC_FLUENCY)])
    named = count([any_of(NAMED_PRODUCTS)])
    rows.append(["generic_fluency", generic, round(100 * generic / base, 2)])
    rows.append(["named_products", named, round(100 * named / base, 2)])

    print(f"baseline (Speechify excluded): {base:,}")
    print(f"any AI mention               : {ai:,} ({100 * ai / base:.1f}%)")
    print(f"self-description : requirement = {self_n / req_n:.1f} : 1")
    print(f"generic : named products      = {generic / named:.1f} : 1\n")

    print(f"{'department':<20}{'postings':>10}{'AI rate':>10}")
    print("-" * 40)
    for dept in DEPARTMENTS:
        f = {"term": {"department": dept}}
        n = count([f])
        a = count([f, any_of(AI_TERMS)])
        rows.append([f"dept:{dept}", n, round(100 * a / n, 2)])
        print(f"{dept:<20}{n:>10,}{100 * a / n:>9.1f}%")
        time.sleep(0.2)

    with open("demand_side_stats.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["metric", "count", "share_pct"])
        w.writerows(rows)


if __name__ == "__main__":
    main()
