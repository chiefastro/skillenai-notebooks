# LinkedIn drafts — three-post series

One post per blog post. Each scored with `scripts/linkedin_scoring/score.py`;
every revision changed exactly one thing so the effect is attributable.
Model CV R2: impressions 0.27, engagements 0.40, followers -0.25 (followers
prediction is not trustworthy). Use for relative ranking only.

URLs go in the first comment, never the body.

---

## 1. The pay cap — `https://skillenai.com/blog/tech-pay-stops-rewarding-experience-at-exactly-10-years`

```
Advertised tech pay rises about 5% for every year of experience a job asks for, right up to 10 years.

Then it stops.

I looked at 25,392 US job postings that state both a salary and a required number of years. Median pay at 10 years: $227,500. At 11 to 12 years: $227,500. Identical. Past that it edges down.

Controlling for role and US state, each year beyond 10 is worth minus 1.8%. It holds across the board, AI and ML engineering included.

And employers barely ask for more. More than 5 years appears in 37.5% of postings. More than 10 years, 4.5%. More than 20 years? 0.03%. Seven postings out of 25,392.

Two readings fit this and my data cannot separate them. Employers may value a 20 year engineer more but have no way to say so in a requisition, because the template stops at "10+". Or the market has decided the marginal decade is not worth paying for.

Either way the advertised ladder ends at ten. If you are 15 or 25 years in, the back half of your career is not being priced, and that is a fact about job ads rather than a verdict on you.

One caveat I will not hide: postings asking for 16+ years are excluded, because 74% of that bucket turned out to be a single employer.

If the ladder stops at ten years, what is the honest argument for year eleven?
```

Score: **1403.6 impressions / 17.9 engagements**  (baseline 887.1 / 10.1;
the single change was naming AI and ML engineering, +58% / +77%)

---

## 2. Skill churn — `https://skillenai.com/blog/your-skills-don-t-expire-your-tools-do`

```
Struts is at 5% of its peak. WebSphere, 6%. Sybase, 4%. COBOL, 11%.

Nobody who built a career on those made a bad call. They were the right choices at the time.

I tracked 2,700 skills through 1,029,639 dated career positions going back to 1995, expecting to find that long careers go stale. The opposite: the median skill is still at 89% of its peak usage, and about half of all skills are still rising.

Then I split the vocabulary in two.

Named technologies, the specific products you list as expertise, versus everything else. 26% of named technologies now sit below a quarter of their peak. For all other skill terms it is 4%. Six times the collapse rate.

The risers over the same window: AWS up 23x, PyTorch 210x, Databricks 181x, GCP and Terraform close behind.

Testing, architecture, requirements gathering, incident response: durable. Oracle, SQL Server, jQuery, PHP, Hadoop, AngularJS, SVN: all below half their peak.

Which also means the number everyone repeats, that skills have a five year half life and technical skills two and a half, does not survive contact with career data. It traces to consultancy marketing, not measurement. Fit seven competing curve shapes per skill and exponential decay wins for only 12% of them. Peer reviewed estimates of human capital depreciation land at 1 to 6% a year.

Your skills are not expiring. Your tools are.

Audit the named products on your resume, not your years. Which one of yours is quietly on the way down?
```

Score: **979.9 / 10.7**  (baseline 886.3 / 9.7; the change was naming the
risers AWS/PyTorch/Databricks/GCP, +11% / +10%. A restructured version leading
with the five-year-half-life myth scored 871.4 and was rejected.)

---

## 3. Job titles — `https://skillenai.com/blog/job-titles-explain-under-10-of-the-skills-a-tech-job-requires`

```
Give me a tech job posting's title and ask me to predict which skills it requires. I can explain under 10% of the variance.

That is across 44,417 US postings, cross validated. Then I ran the identical test on a completely different corpus: 138,123 career profile positions, written by workers describing jobs they had already done rather than by recruiters advertising jobs they wanted to fill.

Postings: the title explains 6.9% of the variance in skills. Profiles: 3.9%. Titles predict even less when the person who did the job is the one describing it.

Here is the same fact in a form you can feel. For each posting, take the ten postings whose skills sit closest to it, and count how many carry a different title. For 52.5% of postings, most of their nearest skill matches are filed under someone else's title. On profiles it is 62.2%.

The spread is ninefold. A Product Engineer posting looks like another job 81% of the time. A Product Designer posting: 9%.

The asymmetries are the real finding.

UX Designer sends 51% of its neighborhood to Product Designer. Product Designer sends essentially nothing back. That is not two titles converging, it is one being absorbed. The same one way pull shows up again: Research Engineer, Research Scientist and AI Engineer all drift toward ML Engineer, which stays put. Cloud, Platform and Infrastructure Engineer all drift toward DevOps. Four titles orbiting one job.

And some titles blur into nothing in particular. Technology Architect, Solutions Architect and plain Software Engineer spread their overlap thinly across many roles with no dominant partner. Those are not hybrid jobs, they are titles that do not map onto a coherent skill set at all.

If you filter your job search by title, you are discarding most of the market.

What is the least informative job title you have ever been given?
```

Score: **1470.4 / 20.5** — highest of the three. The one revision added the
profile-corpus corroboration (6.9% postings vs 3.9% profiles), +1% impressions
and +6% engagements over the unrevised 1455.3 / 19.3. It was already
acronym-dense (AI, ML, UX, DevOps), the strongest single positive feature.

---

Suggested order: titles (strongest hook) → pay cap → skill churn.
The model rates the exclamation-in-hook suggestion as ~neutral on all three; rejected on tone.
