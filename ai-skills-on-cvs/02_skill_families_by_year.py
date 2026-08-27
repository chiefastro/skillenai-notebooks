#!/usr/bin/env python3
"""Step 2 — measure skill families against DATED CV text, by year.

Why raw text and not the enrichment pipeline's extracted skills:
`HAS_SKILL` edges in the talent graph attach to the *person* and carry no
dates (0 of 18,412 sampled edges had a startDate), so they cannot answer
"when did this skill appear". Position dates live on `WORKED_AT`; there is no
join back to skills. Tracked as SKI-577. Until that lands, a dated supply-side
series can only come from raw position descriptions, i.e. string matching.

Why families and not raw entity names:
Entity resolution fragments a single skill across several entities --
`LLMs` / `LLM` / `Large language models (LLMs)` are three entities for one
skill, and the agent family splits four ways. Measured unmerged, every one of
them ranks lower than it should. We merge the fragments discovered in step 1
into families and count each family at most once per position.

Input:  profiles.jsonl  (Bright Data LinkedIn snapshot; NOT in this repo -- PII)
Output: skill_families_by_year.csv

Usage:
    python 02_skill_families_by_year.py /path/to/profiles.jsonl
"""
import collections
import csv
import json
import re
import sys

# Education/activity entries are not jobs; they inflate early years.
EDU = re.compile(
    r"universit|college|school|bootcamp|hackathon|study abroad|teaching assistant", re.I
)

# Families group the entities DISCOVERED in step 1. Each value is a list of
# regex alternatives; a position counts once per family regardless of how many
# alternatives hit.
FAMILIES: dict[str, list[str]] = {
    # --- GenAI-era ---
    "LLMs": [r"llms?", r"large language models?"],
    "Generative AI": [r"generative ai", r"gen-?ai"],
    "RAG": [r"retrieval[- ]augmented generation", r"rag"],
    "AI agents": [r"ai agents?", r"agentic ai", r"agentic workflows?", r"agentic"],
    "prompt engineering": [r"prompt engineering", r"prompt engineer"],
    "LangChain": [r"langchain", r"llamaindex"],
    "vector databases": [r"vector databases?", r"vector stores?"],
    "MCP": [r"mcp", r"model context protocol"],
    "AI tools": [r"ai tools?"],
    "fine-tuning": [r"fine-?tuning"],
    "embeddings": [r"embeddings"],
    # --- classical ML baselines, for comparison ---
    "machine learning": [r"machine learning"],
    "deep learning": [r"deep learning"],
    "NLP": [r"nlp", r"natural language processing"],
    "MLOps": [r"mlops"],
}

# Bare "Agents" is deliberately EXCLUDED from the AI agents family: insurance
# and real-estate agents contaminate it heavily.

COMPILED = {
    name: re.compile("(?<![a-z0-9])(" + "|".join(alts) + ")(?![a-z0-9])")
    for name, alts in FAMILIES.items()
}

YEAR_MIN, YEAR_MAX = 2018, 2025


def year_of(raw: str | None) -> int | None:
    m = re.search(r"(19|20)\d{2}", raw or "")
    return int(m.group(0)) if m else None


def main(path: str) -> None:
    totals: collections.Counter = collections.Counter()
    fam_counts: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)

    with open(path) as fh:
        for line in fh:
            try:
                doc = json.loads(line)
            except ValueError:
                continue
            if doc.get("country_code") != "US":
                continue
            for exp in doc.get("experience") or []:
                company = exp.get("company") or ""
                # PARSE GOTCHA: multi-role companies nest real roles under
                # experience[].positions[]; the top-level item is just the
                # company with null dates. Flattening recovers ~1/3 of positions.
                for pos in exp.get("positions") or [exp]:
                    desc = pos.get("description") or ""
                    if not desc:
                        continue
                    if EDU.search(company) or EDU.search(pos.get("title") or ""):
                        continue
                    yr = year_of(pos.get("start_date"))
                    if not yr or yr < YEAR_MIN or yr > YEAR_MAX:
                        continue
                    lowered = desc.lower()
                    totals[yr] += 1
                    for name, rx in COMPILED.items():
                        if rx.search(lowered):
                            fam_counts[name][yr] += 1

    years = sorted(totals)
    with open("skill_families_by_year.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["family", "year", "positions", "mentions", "share_pct"])
        for name in FAMILIES:
            for yr in years:
                n = fam_counts[name].get(yr, 0)
                w.writerow([name, yr, totals[yr], n, round(100 * n / totals[yr], 4)])

    print("positions per year:", {y: totals[y] for y in years})
    print(f"\n{'family':<22}{'2022%':>8}{'2025%':>8}{'+pp':>8}{'mult':>7}{'n25':>7}")
    print("-" * 60)
    rows = []
    for name in FAMILIES:
        c = fam_counts[name]
        s22 = 100 * c.get(2022, 0) / totals.get(2022, 1)
        s25 = 100 * c.get(2025, 0) / totals.get(2025, 1)
        rows.append((name, s22, s25, s25 - s22, (s25 / s22) if s22 else float("inf"), c.get(2025, 0)))
    for name, s22, s25, pp, mult, n25 in sorted(rows, key=lambda r: -r[3]):
        m = "inf" if mult == float("inf") else f"{mult:.1f}x"
        print(f"{name:<22}{s22:>7.2f}%{s25:>7.2f}%{pp:>7.2f}{m:>7}{n25:>7}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "profiles.jsonl")
