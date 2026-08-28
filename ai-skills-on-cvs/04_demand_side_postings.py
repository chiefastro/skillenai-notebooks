#!/usr/bin/env python3
"""Step 4 — the demand side: how employers actually write about AI in postings.

MEASUREMENT WARNING — read before comparing any two numbers here.
------------------------------------------------------------------
Two different kinds of measurement live in this file, and they are NOT
interchangeable:

  (a) TOPIC MENTION  — does a phrase appear anywhere in the posting text?
      Broad, and fairly complete: if a posting is about generative AI, some
      phrase in the set will catch it.

  (b) REQUIREMENT PHRASING — does the posting contain an explicit construction
      directed at the candidate ("experience with LLMs", "proficiency with AI")?
      Narrow, and badly INCOMPLETE: requirements are also written as bullet
      points ("3+ years ML experience") and structured skill tags, which no
      phrase list catches.

An earlier version of this analysis compared (a) against (b) and reported an
"8:1" gap between employers describing themselves as AI-native and asking
candidates for AI proficiency. That ratio was mostly an artifact of the two
phrase sets having very different breadth. Expanding the requirement set from
5 phrases to 21 more than tripled it (1.95% -> 6.44%), collapsing the ratio
from 8.3:1 to 2.5:1 -- and 6.44% is still only a FLOOR.

Rules that follow from this:
  * Only compare topic-mention measures with other topic-mention measures.
  * Always report the requirement rate as a floor ("at least X%"), never as a
    point estimate, and never as the denominator of a headline ratio.

Corpus caveat: the jobs index only starts 2026-03-10, so there is no YoY series
here. Every figure is a within-window share, robust to crawler coverage bias in
a way absolute volumes are not.

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

# --- (a) TOPIC MENTION sets — mutually comparable ----------------------------
# Deliberately excluded despite scoring high: "Claude" (a common French given
# name), "Cursor" (UI and database cursors), "Gemini" (zodiac sign, unrelated
# product lines). Entity-name collisions, not AI mentions.
AI_TERMS = [
    "generative AI", "artificial intelligence", "machine learning", "prompt engineering",
    "AI tools", "AI-assisted", "AI agents", "ChatGPT", "GitHub Copilot", "LangChain",
    "large language model", "AI fluency", "AI literacy",
]
SELF_DESCRIPTION = ["AI-native", "AI-first", "leverage AI", "AI-powered"]
GENERIC_FLUENCY = ["AI tools", "AI-assisted", "generative AI", "prompt engineering"]
NAMED_PRODUCTS = ["ChatGPT", "GitHub Copilot", "LangChain", "Midjourney", "Hugging Face"]

# --- (b) REQUIREMENT PHRASING — a FLOOR, not comparable with the above -------
CANDIDATE_REQUIREMENT = [
    # the original narrow set
    "proficiency with AI", "experience with AI tools", "familiarity with AI",
    "comfortable using AI", "hands-on with AI",
    # phrasings the narrow set missed — these alone are 2.4x the original
    "experience with LLMs", "experience with large language models",
    "experience with machine learning", "experience building AI",
    "experience with generative AI", "familiarity with LLMs", "proficiency in AI",
    "working knowledge of AI", "exposure to AI", "experience using AI",
    "experience with AI/ML", "hands-on experience with AI", "strong AI skills",
    "experience with AI agents", "experience with RAG", "background in machine learning",
]

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
    rows.append(["baseline_postings", "denominator", base, ""])

    # -- topic-mention family (comparable with each other) --
    for key, terms in [("any_ai_mention", AI_TERMS),
                       ("generic_fluency", GENERIC_FLUENCY),
                       ("employer_self_description", SELF_DESCRIPTION),
                       ("named_products", NAMED_PRODUCTS)]:
        n = count([any_of(terms)])
        rows.append([key, "topic_mention", n, round(100 * n / base, 2)])

    # -- requirement floor (NOT comparable with the above) --
    req = count([any_of(CANDIDATE_REQUIREMENT)])
    rows.append(["candidate_requirement_floor", "requirement_floor", req,
                 round(100 * req / base, 2)])

    lookup = {r[0]: r for r in rows}
    print(f"baseline (Speechify excluded)      {base:,}")
    for k in ("any_ai_mention", "generic_fluency", "employer_self_description", "named_products"):
        print(f"{k:<34} {lookup[k][2]:>8,}  {lookup[k][3]:>6.2f}%   [topic mention]")
    print(f"{'candidate_requirement_floor':<34} {req:>8,}  {100 * req / base:>6.2f}%   [FLOOR — undercounts]")
    print(f"\ngeneric : named products = "
          f"{lookup['generic_fluency'][2] / lookup['named_products'][2]:.1f} : 1  "
          f"(both topic mentions — a fair comparison)")

    print(f"\n{'department':<20}{'postings':>10}{'AI rate':>10}")
    print("-" * 42)
    for dept in DEPARTMENTS:
        f = {"term": {"department": dept}}
        n = count([f])
        a = count([f, any_of(AI_TERMS)])
        rows.append([f"dept:{dept}", "topic_mention", n, round(100 * a / n, 2)])
        print(f"{dept:<20}{n:>10,}{100 * a / n:>9.1f}%")
        time.sleep(0.2)

    with open("demand_side_stats.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["metric", "measure_type", "count", "share_pct"])
        w.writerows(rows)


if __name__ == "__main__":
    main()
