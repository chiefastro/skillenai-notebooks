# AI skills on CVs: machine learning didn't lose, it stopped moving

**Date:** 2026-08-27
**Author:** Skillenai AI Analyst
**Sources:**
- **Supply** — Bright Data LinkedIn snapshot, 300,000 US tech worker profiles (`bd_20260724`), position descriptions dated by role start year, 2012–2025. **Positions with an AI job title are excluded** — they are the panel's selection channel.
- **Demand** — Skillenai jobs index (`prod-enriched-jobs`), 2026-03-01 onward. Headline figures use a **182,347-posting cohort** titled as non-AI tech roles; the full 342,815-posting corpus selects on AI and is reported only as a contrast.

---

## TL;DR

Everyone asks whether AI skills are showing up on CVs. They are — but the interesting part is what happened to the skills they replaced.

**Generative-AI skills went from 1.1% of roles started in 2022 to 4.3% in 2025, and overtook classical machine learning in 2024.** Not because GenAI grew faster than ML. Because **ML stopped growing entirely** — 2.72% in 2022, 2.60% in 2025, a 1.0x multiple over three years — and GenAI walked past a stationary target.

All supply-side figures **exclude positions with an AI job title**. Those roles are the panel's selection channel, and including them inflates the recent end of every trend — see the correction notes.

On the demand side, **24.1% of US tech postings that are not themselves AI roles now mention AI** — and when employers write about it they reach for generic vocabulary ("AI tools", "AI-assisted") **5x more often** than any named product like ChatGPT or Copilot. AI fluency is being described as a way of working, not a tool checkbox.

![Generative AI overtook classical machine learning on US tech CVs in 2024, while machine learning itself stayed flat](01_genai_vs_ml_crossover.png)

The shift is real. It is a **substitution, not an expansion** — and on the demand side it is still a tiebreaker, not a filter.

---

## 1. The top 3 AI skills to emerge since 2022

Share of US tech CV position descriptions, by the year the role started.

Positions with an AI job title are excluded throughout.

| # | Skill | 2022 | 2023 | 2024 | 2025 | Change | Multiple |
|---|---|---:|---:|---:|---:|---:|---:|
| =1 | **AI agents / agentic** | 0.09% | 0.09% | 0.53% | **1.36%** | +1.26pp | **14.5x** |
| =1 | **LLMs** | 0.40% | 0.85% | 1.44% | **1.65%** | +1.25pp | 4.1x |
| 3 | **Generative AI** | 0.39% | 0.69% | 0.85% | **0.94%** | +0.55pp | 2.4x |
| 4 | RAG | 0.10% | 0.27% | 0.61% | 0.59% | +0.49pp | 5.9x |
| 5 | AI tools | 0.10% | 0.15% | 0.32% | 0.51% | +0.41pp | 5.1x |
| 6 | MCP | 0.01% | 0.02% | 0.05% | 0.28% | +0.27pp | **27.5x** |
| 7 | prompt engineering | 0.04% | 0.16% | 0.17% | 0.26% | +0.22pp | 6.4x |
| 8 | LangChain | 0.07% | 0.19% | 0.21% | 0.25% | +0.18pp | 3.7x |

**AI agents and LLMs are a statistical tie** at the top — 1.26pp against 1.25pp is well inside the noise, so treat them as joint first rather than ranked. What separates them is shape: LLMs grew steadily from a higher base, while AI agents was flat until 2023 and then went almost vertical (0.09% → 0.53% → 1.36%). Most of the agent story is the last eighteen months.

**MCP is the fastest-growing skill in the corpus at 27.5x**, which fits — Model Context Protocol only launched in late 2024. We keep it out of the headline: n=29 in 2025, and bare "MCP" collides with the Microsoft Certified Professional credential. The 2025-only spike argues the signal is genuine (a stale certification would be flat or declining), but the base is too thin to quote.

![Change in skill prevalence on US tech CVs 2022 to 2025: every generative-AI skill grew while machine learning shrank](02_emerging_skills.png)

## 2. The classical ML stack is flat — or shrinking

This is the finding that reframes the rest.

| Skill | 2022 | 2025 | Multiple |
|---|---:|---:|---:|
| machine learning | 1.74% | 1.42% | **0.8x** |
| NLP | 0.38% | 0.50% | 1.3x |
| deep learning | 0.20% | 0.23% | 1.1x |
| MLOps | 0.07% | 0.08% | 1.1x |

Once AI-titled roles are removed, "machine learning" does not merely flatten — it **declines**, from 1.74% to 1.42%. In ordinary tech roles the term is being used less than it was three years ago. The other classical families are flat. All net growth in AI skills on CVs since 2022 is GenAI-native.

## 3. GenAI overtook ML in 2024

| Year | Positions | GenAI (strict) | GenAI (loose) | Classical ML |
|---|---:|---:|---:|---:|
| 2020 | 24,987 | 0.34% | 0.53% | 2.61% |
| 2021 | 29,578 | 0.55% | 0.76% | 2.49% |
| 2022 | 29,946 | 1.06% | 1.39% | 2.72% |
| 2023 | 24,126 | 2.11% | 2.47% | 3.18% |
| 2024 | 21,198 | **3.50%** | 4.07% | **3.35%** |
| 2025 | 10,534 | 4.28% | 4.69% | 2.60% |

The crossover lands in 2024 under both the strict and loose definitions.

Note this table's "classical ML" is a broader regex than the family in §2 (it includes TensorFlow, PyTorch, scikit-learn, computer vision and NLP), which is why its levels are higher. The trend is the same: it peaks in 2023 and turns down.

## 4. Demand side: AI language in jobs that are *not* AI jobs

Measured on **182,347 postings whose title is a non-AI tech role** — software engineer, devops, security engineer, product manager and similar — with any AI-titled role excluded. This restriction is essential and explained under "the corpus selects on AI" below: the whole-corpus figure is inflated by construction.

**These four rows are all the same measure** — does the phrase appear anywhere in the posting? — so they can be compared with each other.

| Topic mention | Postings | Share |
|---|---:|---:|
| Mention AI at all | 43,917 | **24.1%** |
| Describe the company as AI-native ("AI-first", "AI-powered") | 26,541 | 14.6% |
| Generic AI vocabulary ("AI tools", "AI-assisted") | 26,120 | **14.3%** |
| Name a specific product (ChatGPT, Copilot, LangChain, …) | 5,208 | 2.9% |

![A quarter of ordinary tech jobs now talk about AI: 24.1% mention AI, and generic AI vocabulary is used 5x more than any named product](03_demand_side.png)

**A quarter of ordinary tech jobs now talk about AI** — jobs that are not themselves AI roles. And generic vocabulary beats named products **5.0:1**: employers are describing a way of working, not a tool to tick off.

### Explicit requirement language — a floor, not a rate

**4.8%** of the cohort (8,678 postings) contains an explicit requirement construction aimed at the candidate — "experience with LLMs", "proficiency with AI", "hands-on experience with AI" and 18 similar phrasings.

**Treat that as a floor, not a measurement.** Requirements are also written as bullet points ("3+ years ML experience") and structured skill tags, which no phrase list catches. It is not comparable with the topic-mention rows above, and must not be used as the denominator of a ratio — see the correction notes.

### Why there is no department breakdown

An earlier version reported that "AI language is densest outside engineering" — Marketing at 45.1% against Engineering's 34.1%. **That finding was withdrawn**; see the correction notes.

---

## Reproducing

```bash
source .env                       # SKILLENAI_INSIGHTS_API_KEY
python 01_discover_skill_vocab.py                       # -> skills_vocab.json
python 02_skill_families_by_year.py profiles.jsonl      # -> skill_families_by_year.csv
python 03_genai_vs_ml_trend.py     profiles.jsonl       # -> genai_vs_ml_by_year.csv
python 04_demand_side_postings.py                       # -> demand_side_stats.csv
python 05_make_figures.py                               # -> 01..03 .png
```

`profiles.jsonl` is the Bright Data LinkedIn snapshot. **It is not in this repo and must not be** — it is personal data, held in `s3://skillenai-linkedin-pii-prod/raw/`. Only aggregates are committed here.

## Method notes

**The vocabulary is discovered, not hard-coded.** Step 1 pulls the top 400 entity-resolved skills from the jobs index and uses those as the measurement set. Hard-coding a list biases results toward what the author already knows — a list written in 2024 would not contain MCP, which turned out to be the fastest-growing skill in the corpus.

**Entity fragmentation had to be merged.** Resolution splits one skill across several entities: `LLMs` / `LLM` / `Large language models (LLMs)` are three, and the agent family splits four ways (`AI agents` / `agentic AI` / `agentic workflows` / `Agents`). Measured unmerged, every one ranks below its true position. Bare `Agents` is excluded from the family — insurance and real-estate agents contaminate it.

**Ambiguous terms were audited, not assumed.** Pre-2020 positions are 56.4% of the corpus, so a term that is merely ordinary English should land ~56% of its hits pre-2020. Every suspect term came in far below that:

| Term | Hits | Pre-2020 share | vs 56.4% baseline |
|---|---:|---:|---|
| bare "RAG" | 857 | 5% | genuine |
| "prompting" | 103 | 11% | genuine |
| "embeddings" | 309 | 12% | genuine |
| "fine-tuning" | 1,069 | 20% | mostly genuine |

The headline trend still uses the **strict** pattern (ambiguous terms dropped) because it is what survives a challenge; the loose column is published alongside so the gap is visible rather than hidden.

**Never compare a topic-mention measure with a requirement-phrasing measure.** This one cost us a headline. An earlier draft of this analysis reported that employers describe themselves as AI-native **"8x more often than they ask candidates for AI proficiency" (16.1% vs 1.9%)**. That ratio was an artifact of the two phrase sets having very different breadth: the self-description set was four broad phrases matched anywhere in the text, while the requirement set was five narrow exact constructions.

Expanding the requirement set from 5 phrases to 21 obvious alternatives — `"experience with LLMs"`, `"experience using AI"`, `"hands-on experience with AI"` and similar — more than tripled it:

| Requirement phrase set | Postings | Share |
|---|---:|---:|
| Original 5 phrases | 6,688 | 1.95% |
| 16 phrasings that set missed | 16,237 | 4.74% |
| Union of all 21 | 22,065 | **6.44%** |

The original figure captured only **30%** of even this larger set, and 21 phrases is still not exhaustive. The 8.3:1 ratio becomes 2.5:1 at 6.4% — and since requirement detection remains incomplete while topic-mention detection is fairly complete, even 2.5:1 is an upper bound.

**The claim has been withdrawn.** Figure 3 now plots only topic-mention measures, the requirement rate is published as a floor, and `04_demand_side_postings.py` carries a measurement warning at the top of the file. The supply-side findings (the crossover, flat ML, the top-3 skills) come from a different dataset and method and are unaffected.

**The profile panel also selects on AI — exclude AI-titled positions.** Profiles are pulled with a job-title keyword list of ~80 R&D titles, and that list includes AI titles. A person enters the panel *because* they hold an AI-titled role — and AI titles are overwhelmingly recent, while their earlier positions carry ordinary titles. The bias therefore lands specifically on the recent end of any trend, which is the exact shape of the headline finding.

It is measurable. AI-titled positions grow as a share of dated positions:

| Year | Positions | AI-titled | Share |
|---|---:|---:|---:|
| 2018 | 27,657 | 620 | 2.2% |
| 2020 | 25,962 | 975 | 3.8% |
| 2022 | 31,422 | 1,476 | 4.7% |
| 2024 | 23,155 | 1,957 | 8.5% |
| 2025 | 11,849 | 1,315 | **11.1%** |

The selection channel itself grows 5x across the window. Excluding those positions:

| Measure | All positions | AI-titled excluded |
|---|---:|---:|
| GenAI 2022 | 1.59% | 1.06% |
| GenAI 2025 | 7.64% | **4.28%** |
| Growth | 4.8x | **4.0x** |
| Classical ML 2022 → 2025 | 4.60% → 5.06% | 2.72% → 2.60% |
| Crossover year | 2024 | **2024** |

The uncorrected recent end was **~1.8x overstated**. Every headline survives the correction — 4.0x growth, flat ML, crossover still 2024 — but the levels are materially lower, and the corrected top-3 ordering changes: RAG drops from third to fourth and Generative AI takes its place.

**The corpus selects on AI, so the demand-side denominator must be chosen with care too.** Inclusion is decided by keyword in [`lambdas/jobs_scraper/normalize.py`](https://github.com/skillenai/skillenai-ds) (`is_rnd_relevant`). A posting is admitted if **either** its title matches an R&D title keyword — a list that includes `"ai"`, `"llm"`, `"generative"`, `"machine learning"` — **or** its description names ≥3 `RND_SKILLS`, of which roughly 35 are AI-specific (`llm`, `rag`, `langchain`, `pytorch`, `embeddings`, `fine-tuning`…).

A posting naming LLM + RAG + LangChain and nothing else is therefore admitted purely on AI content. Measuring "what share of the corpus mentions AI" conditions on the numerator — and indeed **23.5% of the corpus is AI-titled**, guaranteed to mention AI.

**The fix** is to restrict to postings admitted via a *non-AI* title keyword, with no AI term in the title at all. Those were admitted regardless of AI content, so within that cohort the rate is unbiased with respect to this selection:

| Denominator | Postings | Mention AI |
|---|---:|---:|
| Whole corpus (contaminated) | 342,815 | **32.6%** |
| Non-AI-titled cohort (used here) | 182,347 | **24.1%** |

The whole-corpus headline was **1.35x overstated**. The cohort figure is also the more interesting one — it is AI language appearing in ordinary engineering jobs rather than in jobs already about AI. Note the generic-versus-named-product ratio moves the *other* way once AI roles are removed, from 3.8:1 to 5.0:1: AI-titled postings are the ones naming specific products.

**Never break this corpus down by department — the same problem, worse.** The jobs index deliberately targets tech and AI roles and excludes everything else. A non-tech department therefore appears in the corpus *only* when a posting matched tech/AI criteria in the first place. Measuring the AI-mention rate of those survivors conditions on the outcome.

A sample of postings tagged `department=Marketing` shows the problem directly:

```
Senior Generative AI Designer / Artist
Marketing Data & Agentic AI Transformation Lead
Junior Marketing Specialist – Content, Growth & AI
CMO/VP Marketing (Retail Vertical AI Company)
Forward Deployed AI Accelerator, Marketing
Marketing AI - Content Manager
```

Several carry AI in the job title. These are not representative marketing postings; they are the marketing postings that look like tech postings. The withdrawn claim (Marketing 45.1% vs Engineering 34.1%) measured the filter, not the labour market. The department queries have been removed from `04_demand_side_postings.py` with a comment explaining why, so the finding cannot be casually reintroduced.

The same caution applies to any future cut of this corpus by industry, function or seniority where the filter might correlate with the thing being measured.

**Named-entity collisions removed.** `Claude` (a common French given name), `Cursor` (UI and database cursors) and `Gemini` (zodiac sign, unrelated product lines) all scored highly on the demand side and were discarded as entity-name collisions rather than AI mentions.

## Caveats

- **US tech only**, both sides. Not a claim about the labour market as a whole.
- **String matching, not the enrichment pipeline's extracted skills.** `HAS_SKILL` edges in the talent graph attach to the person and carry **no dates** — 0 of 18,412 sampled edges had a `startDate` — so they cannot answer "when did this skill appear". Tracked as **SKI-577**. Until that lands, a dated supply-side series can only come from raw position descriptions.
- **Self-reported.** CV text is what people claim, not what they can do.
- **~35% of positions carry a description**; the rest contribute nothing to the supply-side measure.
- **2025 is partial.** The Bright Data `experience` field is vendor-current only to ~Oct 2025 (a known vendor issue, not a pipeline bug), so 2025 has 11,849 positions against 23,155 in 2024. Shares are still comparable; counts are not.
- **Retroactive CV editing biases against the trend.** People add AI to descriptions of older roles, inflating early years and flattening the curve. The real growth is likely steeper than reported.
- **No YoY on the demand side.** The jobs index begins 2026-03-10; every posting figure is a within-window share.
- Small-n departments (Customer Success n=562, Finance n=1,115) are indicative only.
