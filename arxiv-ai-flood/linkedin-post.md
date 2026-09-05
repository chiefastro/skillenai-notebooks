Everyone blames AI slop for the flood of AI papers at NeurIPS, ICML and ICLR.

We decomposed a decade of arXiv data across AI, ML, CV and NLP. The flood is real. The explanation is wrong.

arXiv took in 106,027 AI papers in 2025, up from 5,622 in 2015. That is 18.9x. Over the same decade, on the same platform, astrophysics grew 1.5x and mathematics 1.6x. So this isn't arXiv getting busier. It's specific to AI.

Then we broke the growth into its parts. Papers equal researchers, times output per researcher, divided by team size.

More researchers: roughly 28x. Output per researcher: up 8.8% over ten years.

Headcount explains about 97% of the growth. Individual productivity explains 3%. The R-squared on that AI productivity trend is 0.95, so it is real — just tiny.

If LLMs and GenAI tools had turned researchers into paper machines, that second number is where it would show. A 9% lift per person, against 28x more people.

We also checked whether the papers are copies. Across 84,420 abstracts, only 0.51% have a near-duplicate. And among the tightest matches, 93 to 100% share an author. That's researchers re-posting their own work, not a duplication machine.

Two things we could not measure, and said so: we cannot detect machine-written text (the literature puts LLM-modified text at up to 22% of CS preprints), and peer-review rates are not measurable from arXiv metadata at all.

The AI paper flood isn't 28x more slop. It's 28x more people.

Third time our data has landed here. Entry-level hiring collapse: a frozen labor market, not AI. Middle management thinning: title inflation unwinding, not AI. Real phenomenon, plausible AI explanation, and the data points somewhere less dramatic every time.

What would change your mind about the AI slop thesis?

<!-- model score
Scored with scripts/linkedin_scoring/score.py (trained on 48 prior posts).

  version                          impressions  engagements
  v1 baseline                             1116         11.8
  vA  + exclamation in hook               1079         12.2   REJECTED (impressions -3%)
  vB  + acronym density (AI/ML/CV/NLP)    1743         13.5   accepted (+56% impressions)
  vC  + NeurIPS/ICML/ICLR, R-squared      1726         14.2   FINAL (+5% engagements vs vB)
  vD  + softened closing question         1726         13.4   REJECTED

Final: impressions 1726 (CV R2 0.27), engagements 14.2 (CV R2 0.40), followers_3d 13.3 (CV R2 -0.25).
Acronym density was by far the strongest lever, consistent with upper_word_ratio being the
top format predictor. The scorer suggested adding an exclamation while simultaneously listing
exclamation_count as a negative driver; tested and rejected.

Blog link goes in the first comment, not the body (has_link is a negative driver).
-->
