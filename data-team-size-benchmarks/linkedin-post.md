# LinkedIn post

A data team is 1 in 9 of your tech org. That ratio holds from 50 people to 10,000.

We looked at 547,000 US tech profiles across 188,361 companies, plus 182,000 open job postings.

Data roles came in at 10.5% of the tech org overall. Split into eight size bands from 10-person tech teams up to 10,000+, every band landed between 9.7% and 12.5%. A hundred-fold change in company size moved the ratio about two points.

So team size is a ratio, not a number. What actually changes with scale is the shape.

As the tech org grows, DE more than doubles as a share of the data org (11.9% to 29.1%). ML and AI roles more than double too. DS climbs. BI falls by a third (52.5% to 33.5%).

Then we put the workforce next to open postings, and the mix employers are buying looks nothing like the mix that exists. ML and AI roles are 6% of people in data jobs but 36% of postings. AE is 0.8% of people and 2.7% of postings. DE and DS sit near parity. BI is 46% of the workforce and 18% of the hiring.

Both columns are shares, so this is zero-sum by construction and somebody has to come out under-weighted. But the direction is hard to miss. Nearly half the data workforce sits in the category being hired into least, relative to its size.

Small orgs are BI-heavy. Large orgs are engineer-heavy. The hiring market is pointed at the large-org shape.

If you are benchmarking your team, use your tech org as the denominator, not your company. Total headcount mostly measures your industry.

What does your data-to-tech ratio look like?

<!-- model score
scripts/linkedin_scoring/score.py (trained on 48 prior posts; CV R2 0.27 impressions / 0.40 engagements)

  v1 baseline                    impressions 1872.9   engagements 20.8
  v2 + acronyms (DE/DS/BI/ML/AE) impressions 2348.7   engagements 27.4
  v3 + exclamation in hook       impressions 2347.7   engagements 27.9   (-0.0% / +1.8%, below 2% threshold; reverted)
  v4 corrected Finding 3         impressions 2640.4   engagements 29.4   <-- SHIPPED

v4 rewrote the supply/demand paragraph after ML/AI Engineering was added to the comparison:
the earlier claim that AE was "the only role where hiring runs ahead of supply" was wrong on
both counts (three of four buckets were above the diagonal, and ML/AI has the larger gap).
Correcting it also scored better.

Applied: no inline URLs (link goes in the first comment), no unicode bullets,
text-only (no image), closes on a question.
-->
