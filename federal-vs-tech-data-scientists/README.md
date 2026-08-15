# Federal Data Science Is Two Different Jobs — and Neither Crosses to Big Tech

*Skillenai analysis · August 2026 · supply-side profile data from Skillenai's **owned talent graph** (LinkedIn profiles), cross-validated against [Live Data (workforce.ai)](https://workforce.ai).*

Two earlier Skillenai posts looked at federal tech from the **demand** side (what postings pay and ask for): [the federal tech bargain](https://github.com/skillenai/skillenai-notebooks/tree/master/federal-tech-broken-bargain) and [same title, different job](https://github.com/skillenai/skillenai-notebooks/tree/master/federal-tech-skills-wall). Both concluded federal data scientists are a *statistics-and-reporting* workforce that doesn't build the way private ones do.

Reading the **people** instead of the postings, that turns out to be **half the story**. "Federal data scientist" is not one job — it's two, and they barely resemble each other.

**TL;DR**
- **Two kinds of federal data scientist.** In their own profile text, **national-lab** data scientists (PNNL, Idaho National Lab, JPL…) **build ML** — 37% use build/ML language vs 18% analyst/stats language, a profile that looks like *private* data science. **Civil-service (OPM) agency** data scientists are the mirror image — 17% build vs **30% analyst/stats** — the "government analyst" the earlier posts described. The old "federal DS don't build" finding was capturing only the OPM half.
- **The frontier-tech door is shut for BOTH kinds.** Big Tech / frontier-AI labs supply **0%** of federal DS (either mode) and take **~0%** on exit — versus **25%** of the inflow and **44%** of the outflow for private DS. This replicates on both data sources (Live Data: 1% in, 0.3% out).
- **Different people, two ways.** Federal DS over-index on domain science (Epidemiology is the #2 field of study at 5.2%; Psychology 3.6%) and come from **state and regional schools** (Montana State, Idaho, Arkansas, Naval Postgraduate); private DS come from statistics-heavy, elite/CS-powerhouse schools (Berkeley, Stanford, Georgia Tech).
- **Built on two independent instruments.** Our owned LinkedIn graph and Live Data cover different slices of the federal workforce (owned skews national-lab, Live Data skews health agencies); the load-bearing finding — the frontier-tech wall — holds on both.

**The one-line takeaway:** *The government data scientist you're picturing — the careful analyst who reports but doesn't build — is real, but only half the story. The other half sits in the national labs doing reinforcement learning. Neither half ever touches Big Tech.*

---

## Data & method

- **Primary source — Skillenai's owned talent graph:** ~300K LinkedIn profiles (Bright Data snapshot, a ~10% tech-oriented sample) with dated job history, education, and free-text `about` + per-position `description`. This is what lets us read *what federal DS actually do* rather than proxy it from titles.
- **Cross-validation — Live Data (workforce.ai):** an independent ~95M-profile panel, used for the education-field pillar (which our graph covers too sparsely) and to check the transition findings on a second sample.
- **Cohorts.** Federal DS = a "Data Scientist"-titled position at a federal employer, split into **national-lab / FFRDC** (n=57) and **OPM civil-service agency** (n=82); private reference = "Data Scientist" at nine big-tech firms (n=284).
- **Skill read.** Because the LinkedIn *Skills* field isn't in the data, "what they do" is measured from **profile text** (`about` + position descriptions), scored for *build/ML* vs *analyst/stats* language. This is self-reported and sparse — read the direction, not the decimals.

---

## Part 1 — Two kinds of federal data scientist

![Bimodal build vs analyst language by cohort](01_bimodal_build_analyst.png)

Score each cohort's profile text for hands-on ML language (machine learning, deep/reinforcement learning, deployment, pipelines) versus analyst/reporting language (statistical analysis, surveillance, dashboards, SAS/SPSS):

| Cohort | Build / ML | Analyst / stats | Looks like |
|---|---:|---:|---|
| **National-lab federal DS** (n=57) | **37%** | 18% | private data science |
| **OPM-agency federal DS** (n=82) | 17% | **30%** | the "government analyst" |
| Private big-tech DS (n=284) | 30% | 12% | (reference) |

National-lab data scientists describe building — reinforcement learning, graph ML, model deployment — at a rate *higher* than private big-tech DS. OPM-agency data scientists invert it: statistics and reporting dominate. The two federal modes are as far apart from each other as either is from private tech. The earlier "federal DS describe ML but don't ship it" conclusion was true — of the OPM half only.

---

## Part 2 — The frontier-tech door is shut for both

![Big Tech share of feeders and exits by cohort](02_frontier_door.png)

Whichever mode you're in, one thing is constant: **almost nobody crosses to or from frontier tech.**

| | Big Tech share of feeders | Big Tech share of exits |
|---|---:|---:|
| National-lab federal DS | 0% | 0% |
| OPM-agency federal DS | 0% | 0% |
| Private big-tech DS | 25% | 44% |

Federal data scientists are fed by **academia** (60% of national-lab entrants) and **older-economy private industry** (74% of OPM entrants), and they exit mostly to **non-frontier private industry** (~57% for both) and — for OPM especially — **back into government** (27% of OPM exits vs 14% for labs). Private DS, by contrast, both arrive from and leave for Big Tech at 25–44%. The frontier-tech ↔ federal pipeline effectively does not exist, in either direction, for either kind of federal data scientist. **This is the finding that replicates across both data sources** (Live Data independently: 1% of federal feeders and 0.3% of exits touch Big Tech).

---

## Part 3 — Different people

![Federal vs private education fields](03_education_funnels.png)

The two populations are trained differently. On field of study (Live Data), federal DS carry a **domain- and social-science tail** — Epidemiology is their #2 field (5.2% vs 0.3%), Psychology 3.6% vs 0.8%, Biostatistics 3.2% vs 1.5% — while private DS concentrate in statistics (9.4% vs 4.4%). Computer Science is a near-tie (6.7% vs 7.2%): federal DS aren't CS-poor, they're domain-heavy.

And on **where they went to school** (owned graph), the split is just as clear:

| | Top schools |
|---|---|
| Private big-tech DS | UC Berkeley, Stanford, Georgia Tech, UW, UT Austin |
| Federal DS | Montana State, Idaho, Arkansas, Naval Postgraduate, NC State |

Private data science recruits from elite and CS-powerhouse programs; federal data science recruits from **state, regional (often lab-adjacent), and federal-adjacent** schools.

---

## Part 4 — Two instruments, one robust finding

This piece deliberately runs on two independent supply-side datasets, because they have **complementary blind spots**. Our owned LinkedIn graph is a ~10% tech-oriented sample that captures the **national labs** well; Live Data's panel covers **civil-service health agencies** (VA, CDC) far better. Neither is complete — across 17 federal agencies our graph holds ~11% of Live Data's cumulative federal-DS count in aggregate, but that ratio swings from under 5% at VA to a reversal at NIH, where our graph sees more.

That's exactly why the agreement matters: the load-bearing claim — **the frontier-tech wall** — shows up identically on both. Where the sources *diverge* (labs vs health agencies) is itself the finding: the composition of "federal data science" depends on which population your instrument sees best, and only using both reveals that it's bimodal.

---

## What it means

**If you're a federal data scientist thinking about the private market:** which of the two jobs you have matters enormously. If you're in a national lab doing ML, your skills travel — but the data says the path is still rarely walked. If you're an OPM-agency analyst, the private market runs on tooling your role doesn't use, and the move is a retraining project.

**If you're a private engineer eyeing government:** frontier-tech experience is essentially absent from the federal data workforce in both modes — which is both a culture gap and, if the mission appeals, an unusual scarcity.

**For the government:** there was never a frontier-tech ↔ federal pipeline to build on, in either direction. The talent it draws is the academic/domain-science lineage (for labs) and the older-economy-industry/analyst lineage (for agencies). Closing a pay gap doesn't change where the pipelines run.

---

## Reproduce it & caveats

Figures render from `make_figures.py` using values captured from the owned-graph analysis (`profiles.jsonl`) and Live Data facets.

- **Supply-side proxy, not listed skills.** The LinkedIn *Skills* field isn't in the data; "what they do" is scored from profile text (self-reported, sparse). Read the direction.
- **Small sub-populations → wide confidence intervals.** National-lab n=57, OPM n=82; exit-movers only 21 and 30 respectively. The build-vs-analyst *direction* is robust; the exact percentages are not.
- **"National lab" vs "civil-service agency" is partly an employer distinction.** National labs are FFRDCs run by contractors and universities, not GS civil servants — so "two modes of federal data science" is also, honestly, "two different kinds of federal employer." That's part of the point: the colloquial term lumps them; the data shows they're different worlds.
- **Owned graph = ~10% sample; employment history current to ~Oct 2025.** Live Data pillars carry their own fuzzy-match and coverage caveats.
- **Complementary coverage, disclosed:** owned ≈11% of Live Data's cumulative federal DS in aggregate, but agency-by-agency uneven (VA/CDC better in Live Data, NIH better in the owned graph).
