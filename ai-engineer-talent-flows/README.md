# Who Becomes an AI Engineer — and Where They Go Next

*A Skillenai analysis. 2026.*

**Data.** Two Skillenai sources:
- **Supply** — the Skillenai **talent graph**: millions of professional career histories with dated, **entity-resolved** role-to-role transitions (roles are normalized to canonical entities, so a move is *Software Engineer → AI Engineer*, not a keyword guess).
- **Demand** — the Skillenai **job-postings index**: what employers advertise for (skills, salaries).

Together they answer: who moves *into* the AI Engineer role, where its people go *next*, how fast newcomers are arriving, and what makes the job distinct.

---

## TL;DR

- **AI Engineer sits at the crossroads of software and data.** Its biggest feeders are **Software Engineer (22%), ML Engineer (14%), and Data Scientist (13%)** — together nearly half of all identifiable moves in. The rest is a genuinely long tail of 100+ other backgrounds (Research Assistant, Data Analyst, Data Engineer, founders, academics).
- **The same roles are where AI Engineers go next** (Software Engineer 20%, Data Scientist 11%, ML Engineer 10%) — plus academia and founder/leadership. It's a two-way interchange with the rest of tech.
- **Far more arrive than leave** — the role is young, so most who've joined are still in it.
- **New entrants are still climbing** — AI Engineer arrivals grew **98 → 217 → 277** across 2023–25, the only adjacent role still rising in 2025 (Data Scientist peaked in 2024 and fell).
- **It's a distinct job, not a rename** — its postings demand an LLM/agent/RAG skill stack the neighboring roles don't.

---

## 1. Who becomes an AI Engineer — and where they go next

Because roles in the talent graph are entity-resolved, we can trace every role-to-role transition adjacent to an AI Engineer role across the whole population — and name both ends.

![Sankey of resolved role transitions into and out of AI Engineer](01_sankey_flows.png)

- **In:** **Software Engineer (22%)** is the single largest feeder, then **ML Engineer (14%)** and **Data Scientist (13%)**. After that comes a real spread of backgrounds — Research Assistant (5%), Data Analyst (4%), Data Engineer (3%), and a long tail of 100+ other roles. AI Engineering pulls from across software, ML/data, *and* academia.
- **Out:** the same three lead the exits (Software Engineer 20%, Data Scientist 11%, ML Engineer 10%), alongside academia (Research/Teaching Assistant) and founder/leadership.

Two things worth stating plainly:
1. **The big "other" slice is real diversity, not a labeling artifact.** Earlier keyword bucketing dumped a third of moves into an unnamed "Other." Entity resolution names them — it's ~110 distinct roles each contributing a handful of moves (Solutions Engineer, Business Analyst, IoT Engineer, Consultant, Lecturer, and so on). No single hidden role was lurking there.
2. **Arrivals outnumber exits ~2.5-to-1.** That's what a young, still-filling role looks like: most people who became AI Engineers haven't moved on yet.

## 2. New entrants are still climbing

Arrivals — the count of people *starting* the role each year — are fully observed for past years, which makes them the clean measure of momentum.

![New arrivals per year by role](02_arrivals_momentum.png)

- **AI Engineer** entrants grew steadily and then sharply: **98 (2023) → 217 (2024) → 277 (2025)** — the only role among its neighbors still rising in 2025.
- **Data Scientist** grew for a decade, **peaked in 2024, and fell in 2025.**
- **Data Engineer** and **ML Engineer** flattened.

## 3. A different job, not a rename

If AI Engineer were just Data Science or ML relabeled, employers would ask for the same skills. They don't — the postings demand a distinct LLM-native stack:

![Skill fingerprint from job postings](03_skill_fingerprint.png)

- **AI Engineer** owns the LLM/agent stack: **LLM 50%, agents 39%, prompt engineering 25%, LangChain 20%, RAG 14%** — multiples of any neighbor.
- **ML Engineer** owns PyTorch (39%); **Data Scientist** owns statistics (37%).

So moving in from Software Engineering or Data Science is real reskilling — which is exactly what the Sankey shows people doing.

## 4. The pay

![Salary bands by role](04_salary_band.png)

AI Engineer advertises like a **premium software engineer**: ~$190K median midpoint — above Data Science (~$173K), level with Software Engineering (~$187K), below the ML Engineering specialist (~$210K).

---

## What this means

- **Software engineers and data scientists:** AI Engineering is the highest-momentum move on the board, and the graph shows your peers already making it. It's genuine reskilling into an LLM/agent/RAG stack, not a title swap.
- **Anyone eyeing the field:** there's no single "right" background. Software, ML, data science, analytics, and even academia all feed it.
- **Hiring managers:** you're recruiting AI Engineers out of the software and ML/data pools (and a wide tail beyond), not a graduate pipeline.

---

## Methodology & caveats

- **Roles are entity-resolved.** The talent graph normalizes free-text titles to canonical role entities; the Sankey is built from the resolved **role-to-role transition matrix** (full population), so prior/next roles are named entities, not keyword buckets. The **AI Engineer** node aggregates the AI-engineer role family (AI Engineer, Generative / Applied / AI-ML / LLM Engineer, and its seniority variants); moves *within* that family are excluded so the flows show genuine cross-role movement. Synonymous destinations (e.g. "Machine Learning Engineer" / "ML Engineer") are merged for display.
- **"N other roles"** rolls up the long tail of distinct resolved roles that each contribute only a few moves — genuine diversity, shown as one node for legibility.
- **Arrivals** count role start-events per year (spell-level: consecutive same-role positions merged, so a company change within a role isn't a new arrival). A start date is a fully-observed past event, so the arrivals trend is censoring-immune, including 2025.
- **Skills and salary are demand-side**, from the Skillenai job-postings index (skill = % of a role's postings mentioning it; salary = advertised base bands). They measure what employers ask for, a different lens than the supply-side graph.
- **Sample.** The talent graph is a tech-focused sample, not a census — read the composition and trends; treat absolute move-counts as sample estimates. AI Engineer is young and its transition counts are modest (hundreds of resolved moves), so the tail percentages carry real uncertainty; the top feeders/exits are the robust part.
- **Not measured:** exits out of the tracked workforce entirely, and the eventual destinations of very recent (2025+) entrants, most of whom are still in the role.
