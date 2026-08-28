#!/usr/bin/env python3
"""Step 6 — the hype gap: talking about AI vs actually requiring it.

THE INSTRUMENT PAIR. This measures one quantity with two independent systems:

  (a) TEXT MENTION   — does the token "AI" appear anywhere in the posting?
      Catches everything, including "Distyl is an applied AI technology company"
      and "AI-driven workflow automation" -- i.e. company and product marketing.

  (b) EXTRACTED SKILL — did the enrichment pipeline's LLM identify an AI skill
      as a requirement of the role? This is a candidate-directed signal, and
      crucially it is NOT a phrase list of ours: the extractor catches
      requirements however they are worded, including bullet points and skill
      tags that phrase matching misses.

Why the pairing matters. An earlier version of this analysis compared two
hand-built phrase lists of very different breadth and reported an "8:1" gap
between employer self-description and candidate requirement. That ratio was an
artifact of the phrase sets, not of employer behaviour, and it was withdrawn.
Here the requirement side comes from a different measurement system entirely,
so the gap cannot be manufactured by our choice of words. Sanity check: the LLM
extraction (11.6%) catches ~2.4x more than the 21-phrase floor in step 4
(4.8%), which is how a floor should behave.

Cohort: non-AI-titled tech postings only -- the SAME definition as step 4 (the
title lists are copied from it verbatim) so the two steps are comparable. See
the selection warning in 04_demand_side_postings.py for why AI-titled roles
must be excluded.

Output: ai_hype_gap.csv

Usage:
    source .env
    python 06_ai_hype_gap.py
"""
import csv
import json
import os
import re
import urllib.request

API_URL = os.environ.get("API_URL", "https://api.skillenai.com")
API_KEY = os.environ["SKILLENAI_INSIGHTS_API_KEY"]

WINDOW = {"range": {"postedAt": {"gte": "2026-03-01"}}}
SPAM = {"terms": {"companyCanonicalName.keyword": ["Speechify"]}}

NON_AI_TITLES = [
    "software engineer", "software developer", "backend engineer", "frontend engineer",
    "fullstack engineer", "full stack engineer", "web developer", "web engineer",
    "mobile engineer", "ios engineer", "android engineer", "platform engineer",
    "infrastructure engineer", "systems engineer", "embedded engineer",
    "engineering manager", "devops", "site reliability", "cloud engineer",
    "cloud architect", "solutions architect", "security engineer", "security analyst",
    "cybersecurity", "application security", "information security", "penetration tester",
    "qa engineer", "quality assurance", "test engineer", "sdet", "automation engineer",
    "business analyst", "business intelligence", "database administrator", "etl developer",
    "product manager", "product owner", "program manager", "product designer",
    "ux designer", "ui designer", "ux researcher", "technical lead", "tech lead",
    "vp of engineering", "head of engineering", "director of engineering",
]
AI_TITLES = [
    "ai", "artificial intelligence", "machine learning", "ml", "deep learning", "llm",
    "generative", "prompt engineer", "nlp", "computer vision", "data scientist",
    "data science", "ml engineer", "mlops", "applied scientist", "research scientist",
    "research engineer", "data engineer", "analytics engineer", "data analyst",
    "quantitative",
]

AI_SKILL_PATTERN = re.compile(
    r"\b(ai|a\.i|llm|llms|gpt|chatgpt|copilot|genai|generative|agentic|agent|agents|prompt|"
    r"rag|langchain|openai|embedding|embeddings|fine-?tun|vector database|machine learning|"
    r"deep learning|nlp|mlops|transformer|model context protocol|mcp)\b", re.I)


def search(body: dict) -> dict:
    req = urllib.request.Request(
        f"{API_URL}/v1/query/search",
        data=json.dumps({"query": body, "indices": ["prod-enriched-jobs"]}).encode(),
        headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
    )
    return json.load(urllib.request.urlopen(req))


def any_of(field: str, terms: list[str]) -> dict:
    return {"bool": {"should": [{"match_phrase": {field: t}} for t in terms],
                     "minimum_should_match": 1}}


TITLE_OK = any_of("title", NON_AI_TITLES)
TITLE_AI = any_of("title", AI_TITLES)


def docs(must=None, must_not=None) -> int:
    return search({"size": 0, "track_total_hits": True, "query": {"bool": {
        "must": [WINDOW, TITLE_OK] + (must or []),
        "must_not": [SPAM, TITLE_AI] + (must_not or [])}}})["total"]


def main() -> None:
    cohort = {"bool": {"must": [WINDOW, TITLE_OK], "must_not": [SPAM, TITLE_AI]}}

    # Discover which skill entities the extractor actually produces here, then
    # keep the AI-related ones. Not hard-coded: the taxonomy comes from the data.
    agg = search({"size": 0, "query": cohort, "aggs": {"e": {
        "nested": {"path": "entities"},
        "aggs": {"sk": {"filter": {"term": {"entities.resolved.entityType": "skill"}},
                        "aggs": {"top": {"terms": {
                            "field": "entities.resolved.canonicalName.keyword",
                            "size": 600}}}}}}}})
    buckets = agg["aggregations"]["e"]["sk"]["top"]["buckets"]
    ai_names = [b["key"] for b in buckets if AI_SKILL_PATTERN.search(b["key"])]

    nested_ai_skill = {"nested": {"path": "entities", "query": {"bool": {"must": [
        {"term": {"entities.resolved.entityType": "skill"}},
        {"terms": {"entities.resolved.canonicalName.keyword": ai_names}}]}}}}
    text_ai = {"match_phrase": {"extractedText": "AI"}}

    base = docs()
    mentions = docs([text_ai])
    requires = docs([nested_ai_skill])
    both = docs([text_ai, nested_ai_skill])
    talk_only = docs([text_ai], [nested_ai_skill])

    rows = [
        ["cohort_postings", base, ""],
        ["mentions_ai_in_text", mentions, round(100 * mentions / base, 2)],
        ["requires_ai_skill", requires, round(100 * requires / base, 2)],
        ["both", both, round(100 * both / base, 2)],
        ["talks_but_does_not_require", talk_only, round(100 * talk_only / base, 2)],
        ["ai_skill_entities_found", len(ai_names), ""],
    ]
    with open("ai_hype_gap.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["metric", "count", "share_pct"])
        w.writerows(rows)

    print(f"skill entities in cohort: {len(buckets)}   AI-related: {len(ai_names)}")
    print(f"\n{'':<44}{'postings':>9}{'share':>8}")
    print("-" * 62)
    print(f"{'cohort (non-AI-titled tech postings)':<44}{base:>9,}")
    print(f"{'mentions AI anywhere in the text':<44}{mentions:>9,}{100 * mentions / base:>7.1f}%")
    print(f"{'LLM extracted an AI SKILL as a requirement':<44}{requires:>9,}{100 * requires / base:>7.1f}%")
    print(f"{'talks about AI but requires no AI skill':<44}{talk_only:>9,}{100 * talk_only / base:>7.1f}%")
    print(f"\nof postings mentioning AI, {100 * talk_only / mentions:.0f}% ask for no AI skill")
    print(f"talk-to-requirement ratio: {mentions / requires:.1f} : 1")


if __name__ == "__main__":
    main()
