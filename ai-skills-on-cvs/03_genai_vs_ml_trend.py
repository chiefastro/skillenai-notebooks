#!/usr/bin/env python3
"""Step 3 — GenAI vs classical ML on CVs, plus a contamination audit.

Two things happen here:

1. A per-term contamination audit. Several plausible GenAI terms are ambiguous
   in CV text: bare "RAG" collides with red/amber/green status reporting,
   "prompting" and "fine-tuning" are ordinary English verbs, "embeddings"
   predates GenAI by a decade, and "LLM" collides with the LL.M. law degree.
   The test: pre-2020 positions are ~56% of the corpus, so a term that is just
   ordinary English should land ~56% of its hits pre-2020. Every suspect term
   came in far below that (bare RAG 5%, prompting 11%, embeddings 12%,
   fine-tuning 20%), i.e. they are genuinely GenAI-era concentrated.

2. STRICT vs LOOSE trend. We report STRICT (ambiguous terms removed) because it
   is what survives a challenge. LOOSE is kept so the gap is visible rather than
   hidden -- the headline (GenAI overtaking classical ML in 2024) holds either way.

Output: genai_vs_ml_by_year.csv, term_contamination_audit.csv

Usage:
    python 03_genai_vs_ml_trend.py /path/to/profiles.jsonl
"""
import collections
import csv
import json
import re
import sys

EDU = re.compile(
    r"universit|college|school|bootcamp|hackathon|study abroad|teaching assistant", re.I
)

# Individually probed so the audit can attribute the signal per term.
AUDIT_TERMS = {
    "generative ai": r"\b(generative ai|gen-?ai)\b",
    "LLM/large language model": r"\b(large language models?|llms?)\b",
    "chatgpt/gpt-N": r"\b(chatgpt|gpt-?[345])\b",
    "openai": r"\bopenai\b",
    "prompt engineering": r"\bprompt engineer\w*\b",
    "PROMPTING (ambiguous)": r"\bprompting\b",
    "RAG bare (ambiguous)": r"\brag\b",
    "retrieval-augmented": r"\bretrieval[- ]augmented\b",
    "langchain/llamaindex": r"\b(langchain|llamaindex)\b",
    "copilot bare (ambiguous)": r"\bcopilot\b",
    "github copilot": r"\bgithub copilot\b",
    "EMBEDDINGS (ambiguous)": r"\bembeddings\b",
    "FINE-TUN (ambiguous)": r"\bfine-?tun\w+\b",
    "agentic/ai agents": r"\b(agentic|ai agents?)\b",
    "anthropic": r"\banthropic\b",
    "diffusion/midjourney/HF": r"\b(stable diffusion|midjourney|hugging ?face)\b",
    "vector database": r"\bvector databases?\b",
}

# STRICT drops bare rag / prompting / fine-tun* / embeddings / bare copilot.
STRICT = re.compile(
    r"\b(generative ai|gen-?ai|large language models?|llms?|chatgpt|gpt-?[345]|openai|"
    r"prompt engineer\w*|retrieval[- ]augmented|langchain|llamaindex|github copilot|"
    r"stable diffusion|midjourney|hugging ?face|vector databases?|agentic|ai agents?|anthropic)\b",
    re.I,
)
LOOSE = re.compile(
    r"\b(generative ai|gen-?ai|large language model|llms?|chatgpt|gpt-?[345]|openai|"
    r"prompt engineer\w*|prompting|retrieval[- ]augmented|\brag\b|langchain|llamaindex|"
    r"copilot|stable diffusion|midjourney|hugging ?face|vector database|embeddings|"
    r"fine-?tun\w+|agentic|ai agents?|anthropic|claude ai)\b",
    re.I,
)
# NOTE: `nlp` here also matches "neuro-linguistic programming". That inflates the
# ML baseline, which makes the GenAI-overtakes-ML crossover HARDER to reach --
# the claim is therefore conservative.
CLASSIC = re.compile(
    r"\b(machine learning|deep learning|neural network\w*|tensorflow|pytorch|"
    r"scikit-?learn|xgboost|random forest|computer vision|nlp|"
    r"natural language processing)\b",
    re.I,
)

# --- SELECTION CORRECTION -----------------------------------------------------
# Profiles are pulled with a job-title keyword list (~80 R&D titles), and that
# list includes AI titles. A person therefore enters the panel BECAUSE they hold
# an AI-titled role -- and AI titles are overwhelmingly recent. Their pre-2022
# positions carry ordinary titles. The effect is to inflate the recent end of any
# trend specifically: AI-titled positions rise from 2.2% of dated positions in
# 2018 to 11.1% in 2025, a 5x growth in the selection channel itself.
#
# Measured on all positions, generative-AI mentions run 1.59% (2022) -> 7.64%
# (2025). Excluding AI-titled positions -- which were never the selection reason
# for the roles that remain -- gives 1.06% -> 4.28%. The uncorrected recent end
# was ~1.8x overstated.
#
# The headline findings survive the correction: growth is still 4.0x, classical
# ML is still flat (1.0x), and the crossover is still 2024.
AI_TITLE = re.compile(
    r"(?<![a-z])(ai|a\.i\.|artificial intelligence|machine learning|ml|deep learning|"
    r"llm|genai|generative|prompt engineer|nlp|computer vision|data scientist|"
    r"data science|mlops|applied scientist|research scientist|ml engineer)(?![a-z])", re.I)


COMPILED_AUDIT = {k: re.compile(v, re.I) for k, v in AUDIT_TERMS.items()}
YEAR_MIN, YEAR_MAX = 2012, 2025


def year_of(raw):
    m = re.search(r"(19|20)\d{2}", raw or "")
    return int(m.group(0)) if m else None


def main(path: str) -> None:
    by_year = collections.defaultdict(lambda: {"n": 0, "strict": 0, "loose": 0, "ml": 0})
    hits, pre2020 = collections.Counter(), collections.Counter()

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
                for pos in exp.get("positions") or [exp]:
                    desc = pos.get("description") or ""
                    if not desc:
                        continue
                    title = pos.get("title") or ""
                    if EDU.search(company) or EDU.search(title):
                        continue
                    if AI_TITLE.search(title):
                        continue  # selection channel — see SELECTION CORRECTION
                    yr = year_of(pos.get("start_date"))
                    if not yr or yr < YEAR_MIN or yr > YEAR_MAX:
                        continue
                    b = by_year[yr]
                    b["n"] += 1
                    if STRICT.search(desc):
                        b["strict"] += 1
                    if LOOSE.search(desc):
                        b["loose"] += 1
                    if CLASSIC.search(desc):
                        b["ml"] += 1
                    for name, rx in COMPILED_AUDIT.items():
                        if rx.search(desc):
                            hits[name] += 1
                            if yr < 2020:
                                pre2020[name] += 1

    total = sum(v["n"] for v in by_year.values())
    pre_total = sum(v["n"] for y, v in by_year.items() if y < 2020)
    baseline = 100 * pre_total / total

    with open("term_contamination_audit.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["term", "hits", "pre_2020_hits", "pre_2020_pct", "corpus_baseline_pct"])
        for name, n in hits.most_common():
            w.writerow([name, n, pre2020[name], round(100 * pre2020[name] / n, 1), round(baseline, 1)])

    with open("genai_vs_ml_by_year.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["year", "positions", "genai_strict", "genai_strict_pct",
                    "genai_loose_pct", "classical_ml_pct"])
        for yr in sorted(by_year):
            b = by_year[yr]
            if b["n"] < 300:
                continue
            w.writerow([yr, b["n"], b["strict"], round(100 * b["strict"] / b["n"], 3),
                        round(100 * b["loose"] / b["n"], 3), round(100 * b["ml"] / b["n"], 3)])

    print(f"corpus pre-2020 baseline: {baseline:.0f}%  "
          f"(a pure-English term should land ~this share of hits pre-2020)\n")
    print(f"{'term':<28}{'hits':>8}{'pre2020%':>10}")
    print("-" * 48)
    for name, n in hits.most_common():
        print(f"{name:<28}{n:>8,}{100 * pre2020[name] / n:>9.0f}%")

    print(f"\n{'year':<6}{'positions':>10}{'strict%':>9}{'loose%':>9}{'ML%':>8}")
    print("-" * 44)
    for yr in sorted(by_year):
        b = by_year[yr]
        if b["n"] < 300:
            continue
        print(f"{yr:<6}{b['n']:>10,}{100 * b['strict'] / b['n']:>8.2f}%"
              f"{100 * b['loose'] / b['n']:>8.2f}%{100 * b['ml'] / b['n']:>7.2f}%")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "profiles.jsonl")
