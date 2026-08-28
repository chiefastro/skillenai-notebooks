#!/usr/bin/env python3
"""Step 4 — the demand side: how employers write about AI in NON-AI tech roles.

SELECTION WARNING — why this file does not measure the whole corpus.
--------------------------------------------------------------------
The jobs index decides inclusion by keyword (lambdas/jobs_scraper/normalize.py,
`is_rnd_relevant`). A posting is admitted if EITHER:

  1. its title matches an R&D title keyword -- and that list includes "ai",
     "llm", "generative", "machine learning", "data scientist"; OR
  2. its description mentions >= 3 RND_SKILLS -- and ~35 of those are
     AI-specific ("llm", "rag", "langchain", "pytorch", "embeddings",
     "fine-tuning", "generative ai", ...).

So a posting naming LLM + RAG + LangChain and nothing else is admitted purely
on AI content. Measuring "what share of the corpus mentions AI" therefore
conditions on the numerator: 23.5% of the corpus is AI-titled and is
guaranteed to mention AI.

THE FIX. Restrict to postings that qualify via a NON-AI title keyword
("software engineer", "devops", "security engineer", "product manager", ...)
and whose title contains no AI term at all. Those postings were admitted under
path 1 regardless of whether the description ever says "AI", so within that
cohort the AI-mention rate is unbiased with respect to this selection.

Effect on the headline: 32.6% across the whole corpus -> 24.1% in the cohort.
The whole-corpus figure was 1.35x overstated. The cohort figure is also the
more interesting one: it is AI language appearing in ordinary engineering jobs
rather than in jobs that are already about AI.

MEASUREMENT WARNING — two kinds of measure live here, do not mix them.
---------------------------------------------------------------------
  (a) TOPIC MENTION      — does a phrase appear anywhere? Broad, fairly complete.
  (b) REQUIREMENT PHRASING — an explicit construction aimed at the candidate.
      Narrow and badly INCOMPLETE: requirements also appear as bullet points
      ("3+ years ML experience") and structured skill tags.

An earlier version compared (a) with (b) and reported an "8:1" gap between
employers describing themselves as AI-native and asking candidates for AI
proficiency. That was an artifact of phrase-set breadth: expanding the
requirement set from 5 phrases to 21 more than tripled it. Only compare
topic-mention measures with each other; always report the requirement rate as
a floor, never as the denominator of a headline ratio.

NO DEPARTMENT BREAKDOWN. Same selection problem, worse. Non-tech departments
survive in the corpus only when the posting matched tech/AI criteria, so their
AI-mention rate is pure selection. An earlier version reported "AI language is
densest outside engineering" (Marketing 45.1% vs Engineering 34.1%) on exactly
that artifact. Do not reintroduce it.

Corpus caveat: the index starts 2026-03-10, so there is no YoY series here.
Spam filter: Speechify carpet-bombs the same ~10 roles across hundreds of cities.

Output: demand_side_stats.csv

Usage:
    source .env
    python 04_demand_side_postings.py
"""
import csv
import json
import os
import urllib.request

API_URL = os.environ.get("API_URL", "https://api.skillenai.com")
API_KEY = os.environ["SKILLENAI_INSIGHTS_API_KEY"]

WINDOW = {"range": {"postedAt": {"gte": "2026-03-01"}}}
SPAM = {"terms": {"companyCanonicalName.keyword": ["Speechify"]}}

# --- the unbiased cohort ------------------------------------------------------
# Non-AI R&D title keywords: inclusion under path 1 is independent of AI content.
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
# Any of these in the title means AI could have driven inclusion -> excluded.
AI_TITLES = [
    "ai", "artificial intelligence", "machine learning", "ml", "deep learning", "llm",
    "generative", "prompt engineer", "nlp", "computer vision", "data scientist",
    "data science", "ml engineer", "mlops", "applied scientist", "research scientist",
    "research engineer", "data engineer", "analytics engineer", "data analyst",
    "quantitative",
]

# --- (a) TOPIC MENTION sets — mutually comparable ----------------------------
# Excluded despite scoring high: "Claude" (a common French given name), "Cursor"
# (UI/database cursors), "Gemini" (zodiac sign). Entity-name collisions.
AI_TERMS = [
    # bare "AI" is the single most common AI token in postings; an earlier
    # version omitted it and understated the mention rate by roughly half.
    "AI",
    "generative AI", "artificial intelligence", "machine learning", "prompt engineering",
    "AI tools", "AI-assisted", "AI agents", "ChatGPT", "GitHub Copilot", "LangChain",
    "large language model", "AI fluency", "AI literacy",
]
SELF_DESCRIPTION = ["AI-native", "AI-first", "leverage AI", "AI-powered"]
GENERIC_FLUENCY = ["AI tools", "AI-assisted", "generative AI", "prompt engineering"]
NAMED_PRODUCTS = ["ChatGPT", "GitHub Copilot", "LangChain", "Midjourney", "Hugging Face"]

# --- (b) REQUIREMENT PHRASING — a FLOOR, not comparable with the above -------
CANDIDATE_REQUIREMENT = [
    "proficiency with AI", "experience with AI tools", "familiarity with AI",
    "comfortable using AI", "hands-on with AI",
    "experience with LLMs", "experience with large language models",
    "experience with machine learning", "experience building AI",
    "experience with generative AI", "familiarity with LLMs", "proficiency in AI",
    "working knowledge of AI", "exposure to AI", "experience using AI",
    "experience with AI/ML", "hands-on experience with AI", "strong AI skills",
    "experience with AI agents", "experience with RAG", "background in machine learning",
]


def search(body: dict) -> dict:
    req = urllib.request.Request(
        f"{API_URL}/v1/query/search",
        data=json.dumps({"query": body, "indices": ["prod-enriched-jobs"]}).encode(),
        headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
    )
    return json.load(urllib.request.urlopen(req))


def phrases(field: str, terms: list[str]) -> list[dict]:
    return [{"match_phrase": {field: t}} for t in terms]


def any_of(field: str, terms: list[str]) -> dict:
    return {"bool": {"should": phrases(field, terms), "minimum_should_match": 1}}


def count(must: list, must_not: list | None = None) -> int:
    return search({
        "size": 0, "track_total_hits": True,
        "query": {"bool": {"must": [WINDOW] + must,
                           "must_not": [SPAM] + (must_not or [])}},
    })["total"]


TITLE_OK = any_of("title", NON_AI_TITLES)
TITLE_AI = any_of("title", AI_TITLES)


def main() -> None:
    rows = []

    # whole corpus — reported ONLY as the contaminated contrast
    whole = count([])
    whole_ai = count([any_of("extractedText", AI_TERMS)])
    ai_titled = count([TITLE_AI])

    # the cohort everything else is measured on
    cohort = count([TITLE_OK], [TITLE_AI])
    rows.append(["cohort_postings", "denominator", cohort, ""])
    rows.append(["whole_corpus_postings", "contaminated_contrast", whole, ""])
    rows.append(["whole_corpus_any_ai_mention", "contaminated_contrast", whole_ai,
                 round(100 * whole_ai / whole, 2)])
    rows.append(["whole_corpus_ai_titled", "contaminated_contrast", ai_titled,
                 round(100 * ai_titled / whole, 2)])

    for key, terms in [("any_ai_mention", AI_TERMS),
                       ("generic_fluency", GENERIC_FLUENCY),
                       ("employer_self_description", SELF_DESCRIPTION),
                       ("named_products", NAMED_PRODUCTS)]:
        n = count([TITLE_OK, any_of("extractedText", terms)], [TITLE_AI])
        rows.append([key, "topic_mention", n, round(100 * n / cohort, 2)])

    req = count([TITLE_OK, any_of("extractedText", CANDIDATE_REQUIREMENT)], [TITLE_AI])
    rows.append(["candidate_requirement_floor", "requirement_floor", req,
                 round(100 * req / cohort, 2)])

    look = {r[0]: r for r in rows}
    print("CONTAMINATED (whole corpus — for contrast only)")
    print(f"  postings {whole:,}   mention AI {whole_ai:,} = {100 * whole_ai / whole:.1f}%")
    print(f"  of which AI-titled: {ai_titled:,} = {100 * ai_titled / whole:.1f}% "
          f"(auto-included on an AI title)\n")
    print(f"UNBIASED COHORT — non-AI tech title, no AI term in title: {cohort:,} postings")
    for k in ("any_ai_mention", "generic_fluency", "employer_self_description", "named_products"):
        print(f"  {k:<30}{look[k][2]:>8,}  {look[k][3]:>6.2f}%   [topic mention]")
    print(f"  {'candidate_requirement_floor':<30}{req:>8,}  "
          f"{100 * req / cohort:>6.2f}%   [FLOOR — undercounts]")
    print(f"\n  generic : named products = "
          f"{look['generic_fluency'][2] / look['named_products'][2]:.1f} : 1")
    print(f"  headline inflation avoided: {100 * whole_ai / whole:.1f}% -> "
          f"{look['any_ai_mention'][3]:.1f}%")

    with open("demand_side_stats.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["metric", "measure_type", "count", "share_pct"])
        w.writerows(rows)


if __name__ == "__main__":
    main()
