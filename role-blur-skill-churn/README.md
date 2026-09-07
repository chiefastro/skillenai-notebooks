# Your job title doesn't describe your job. Your skills don't expire — your tools do.

**Date:** 2026-09-07
**Sources:** Skillenai job-postings index (`prod-enriched-jobs`) — 44,417 US tech postings; Skillenai talent graph — 569,143 career profiles yielding 1,029,639 dated position descriptions, 1995–2025.
**Scope:** US, text-bearing ATS platforms, spam employers excluded.

---

## TL;DR

1. **Job titles are weak descriptions of work.** A title explains **under 10%** of the variance in the skills a posting asks for. For **52.5%** of postings, most of their closest skill-matches carry a *different* title.
2. **How blurred a role is varies enormously.** Product Engineer postings look like someone else's job **81%** of the time. Product Designer: **9%**. That's a 9× spread.
3. **Named technologies collapse; generic capabilities endure.** Struts, WebSphere, Sybase and Perl sit at **4–8%** of their peak. **26%** of named technologies are below a quarter of their peak, versus **4%** of all other skill terms.
4. **At least a third of 2005's leading skills** have been pushed out of the top 100 by 2025.
5. **Experience is paid for a decade, then it isn't.** +5.3%/yr up to 10 years; −1.8%/yr beyond. Only **4.5%** of postings ask for more than 10 years; **0.03%** ask for more than 20.

---

## 1. How much does a job title tell you?

For each posting we find the ten postings whose *skills* are closest, and ask how many carry a different job title. No role model, no thresholds, no clustering — just nearest neighbours in skill space.

![Horizontal bar chart ranking 32 tech job titles by the share of their ten nearest postings in skill space that carry a different title, from Product Engineer at 81% down to Product Designer at 9%](01_role_blur.png)

**Product Engineer and Platform Engineer keep only ~19% of their own neighbourhood.** Four out of five of their closest postings are filed under someone else's title. At the other end, Product Designer is 92% self-contained — design is the one genuinely bounded profession in this data.

### Which roles blur into which

Listing every neighbour role holding ≥8% of the ten nearest postings (a variable-length list, so a role that blurs diffusely is visibly different from one that blurs into a single partner):

| role | keeps | blurs into |
|---|---|---|
| Platform Engineer | 19% | DevOps 20%, SRE 12%, Software Engineer 9% *(+41% spread thinly)* |
| Product Engineer | 19% | Full Stack 21%, Software Engineer 15%, Frontend 13% *(+32% thin)* |
| Infrastructure Engineer | 24% | DevOps 16%, SRE 15%, Platform 8% *(+37% thin)* |
| Technology Architect | 30% | Software Engineer 11% *(+60% thin)* |
| Software Engineer | 31% | Full Stack 11%, Backend 9% *(+49% thin)* |
| Cloud Engineer | 34% | DevOps 23% *(+42% thin)* |
| AI Engineer | 35% | ML Engineer 16% *(+50% thin)* |
| Analytics Engineer | 39% | Data Engineer 28%, Data Analyst 19% |
| UX Designer | 43% | **Product Designer 51%** |
| Data Scientist | 56% | Data Analyst 14%, ML Engineer 11% |
| Security Engineer | 72% | *nothing above threshold* |
| Product Designer | **92%** | *nothing above threshold* |

**The asymmetries are the interesting part.** UX Designer sends 51% of its neighbourhood to Product Designer, and Product Designer sends essentially nothing back — that is a title being absorbed, not two titles merging. The same one-way pull shows up in Research Engineer → ML Engineer (26%), Research Scientist → ML Engineer (24%), and Cloud/Platform/Infrastructure → DevOps (23%, 20%, 16%): four titles orbiting one job.

And some roles blur into *nothing in particular*. Technology Architect (+60%), Solutions Architect (+57%) and Software Engineer (+49%) have most of their overlap spread thinly across many roles with no single partner. These aren't hybrids of two jobs; they're titles that don't map onto a coherent skill set at all.

## 2. Named technologies collapse. Generic capabilities don't.

Tracking 85 named technologies — chosen and written down *before* their movement was examined — through 1,029,639 dated career positions:

![Two-panel bar chart on a shared scale showing named technologies that fell the most in rank, led by Struts and WebSphere, beside those that rose the most, led by Figma, Databricks and PyTorch](02_named_tech.png)

| fell | rank | now | | rose | rank | now |
|---|---|---|---|---|---|---|
| struts | #449 → #2,682 | 0.05× | | figma | #2,355 → #222 | 199× |
| websphere | #395 → #2,609 | 0.06× | | databricks | #2,348 → #246 | 181× |
| sybase | #655 → #2,731 | 0.04× | | pytorch | #2,489 → #397 | 210× |
| perl | #211 → #2,253 | 0.05× | | pandas | #2,204 → #199 | 126× |
| cobol | #402 → #2,335 | 0.11× | | snowflake | #2,098 → #196 | 89× |
| subversion | #757 → #2,712 | 0.08× | | terraform | #1,982 → #197 | 68× |

Twenty-four named technologies now sit below half their peak: AngularJS, ASP.NET, Citrix, COBOL, Cognos, DB2, Hadoop, IIS, Informatica, jQuery, JSP, MapReduce, Oracle, Perl, PHP, Ruby, Servlets, SQL Server, Struts, Subversion, SVN, Sybase, Tomcat.

**This is the distinction that matters for a career.** Generic capability words — *testing*, *architecture*, *requirements* — are durable. The specific products you list as expertise are not.

![Histogram comparing named technologies against all other skill terms by current usage as a fraction of their own peak, showing named technologies concentrated in the low range](02b_tech_vs_generic.png)

| | median now/peak | below half peak | below a quarter |
|---|---|---|---|
| **Named technologies** (85) | 0.81 | **36.5%** | **25.9%** |
| All other skill terms (2,650) | 0.89 | 18.2% | 4.1% |

Named technologies are **six times** more likely to fall below a quarter of their peak (Mann-Whitney p=0.0016).

## 3. A third of 2005's top skills have been displaced

![Line chart showing the share of the 100 most-mentioned skills of 2005-2008 that remain in the top 100, declining from 100% to 67% by 2023-2025](03_displacement.png)

**At least 33%** of the skills that were top-100 in 2005 had been pushed out of the top 100 by 2025. A floor rather than a point estimate: skills that died outright are absent from a vocabulary built on 2026 postings, so the true figure is higher. Re-running on past positions only (removing people describing their *current* job in more detail) gives 32%.

Rank is the right unit here. It is computed within each period, so the shorter descriptions in recent years deflate every skill's share together and leave the ordering intact.

## 4. Experience is paid for a decade

![Line chart of median advertised salary against required years of experience, rising steadily to ten years and then flat, with marker size showing sample size](04_pay_plateau.png)

Median advertised pay climbs to 10 years of required experience and stops. With role and state fixed effects, each year up to 10 is worth **+5.27%** (p≈0); each year beyond is worth **−1.75%** (p=1.9e-26). Under a conservative specification that also controls seniority — arguably over-controlling, since seniority is *how* experience gets paid — it is +2.40% then −0.14% (n.s.): flat either way.

Demand thins out fast:

| asks for more than | share of postings |
|---|---|
| 5 years | 37.5% |
| 10 years | 4.5% |
| 15 years | 0.89% |
| 20 years | **0.03%** (7 of 25,392) |

---

## What we could *not* establish

Stated plainly, because these were tested and failed rather than skipped:

- **Whether role blurring has increased.** The postings index begins 2026-03, so there is no demand-side history. Every supply-side proxy we built — NMF theme spread, role-axis concentration, two-role depth, raw skill density — came back **flat**, but each is measured on self-written career descriptions rather than employer requirements. *Roles are blurred* is supported; *roles are blurring more* is not.
- **A skill "half-life."** Exponential decay is the wrong model: fitting seven competing forms per skill, rise-and-fall shapes (bi-logistic 31%, logistic 21%) beat exponential (12%), and exponential wins mainly where the observation window hides the adoption phase. Roughly half of skills are still rising.
- **The true magnitude of skill death.** The skill vocabulary is built from 2026 postings and therefore contains only survivors. Every churn figure here is a lower bound.
- **Whether jobs ask for more skills than they used to.** Measured against a 2026 vocabulary, skills per position rises 1.36×. Measured on skills present in both eras, it is **0.99×** — flat. The apparent growth is the dictionary, not the jobs.

## Method

**Role blurring.** Postings are binary vectors over 7,562 canonicalised skills (≥10 postings each); cosine nearest neighbours; role labels from the index's own `role` field with spelling and seniority variants merged. 400 sampled query postings per role, roles with ≥300 postings.

**Skill churn.** 1,029,639 dated position descriptions from 569,143 profiles across two corpus snapshots, deduplicated by profile id. Skills extracted by deterministic n-gram matching (no LLM, so the instrument cannot drift across years). Yearly *shares*, so corpus growth cancels. Ranking is computed among skills only, so prose terms don't compete for rank positions.

**Pay.** 25,392 US postings carrying both a USD salary and a structured experience requirement. Years-of-experience is the *maximum* across qualification paths; the minimum is unusable because "PhD + 0 years" records as 0 in 63% of postings.

**Known caveats.** Position descriptions are self-written and edited at unknown times, so modern vocabulary may be applied retroactively to old roles. Old positions are only visible if the person still maintains a profile — survivorship. Large employers using proprietary ATS platforms are under-represented. Skill entity resolution produces duplicate surface forms, canonicalised here but imperfectly. 2024–25 position descriptions are shorter and skew heavily to current jobs; rank-based measures are robust to this, share-based ones are not, and the distinction is respected throughout.

Reusable code and the full per-role blurring table (`role_blurring.csv`) accompany this folder.
