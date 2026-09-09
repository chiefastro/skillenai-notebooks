# LinkedIn post

A data team is 1 in 9 of your tech org. That ratio holds from 50 people to 10,000.

We looked at 547,000 US tech profiles across 188,361 companies, plus 182,000 open job postings.

Data roles came in at 10.5% of the tech org overall. Split into eight size bands from 10-person tech teams up to 10,000+, every band landed between 9.7% and 12.5%. A hundred-fold change in company size moved the ratio about two points.

So team size is a ratio, not a number. What actually changes with scale is the shape.

As the tech org grows, DE more than doubles as a share of the data org (11.9% to 29.1%). ML and AI roles more than double too. DS climbs. BI falls by a third (52.5% to 33.5%). Small orgs staff people who answer questions. Big orgs staff people who build the systems that answer questions.

The sharpest finding was on the supply side. AE — Analytics Engineering — is 0.9% of people currently in data roles, but 4.4% of open data postings. It is the only role where hiring runs several times ahead of the people available to fill it. BI is the mirror image: half the installed base, a quarter of the hiring.

Most of the workforce is shaped like what companies used to buy.

If you are benchmarking your team, use your tech org as the denominator, not your company. Total headcount mostly measures your industry.

What does your data-to-tech ratio look like?

<!-- model score
scripts/linkedin_scoring/score.py (trained on 48 prior posts; CV R2 0.27 impressions / 0.40 engagements)

  v1 baseline                    impressions 1872.9   engagements 20.8
  v2 + acronyms (DE/DS/BI/ML/AE) impressions 2348.7   engagements 27.4   <-- SHIPPED (+25% / +32%)
  v3 + exclamation in hook       impressions 2347.7   engagements 27.9   (-0.0% / +1.8%, below 2% threshold; reverted)

Applied: no inline URLs (link goes in the first comment), no unicode bullets,
text-only (no image), closes on a question. Stopped at v2 per diminishing-returns rule.
-->
