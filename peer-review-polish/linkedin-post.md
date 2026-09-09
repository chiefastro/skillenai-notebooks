Everyone blames AI slop for what happened to ML peer review. We measured 24,479 reviews across ICLR, NeurIPS, COLM and MIDL. The data says something more uncomfortable.

Em dashes now appear in 36.5% of ICLR 2026 reviews, up from 6.1% in 2024. A 6x rise. An em dash takes a deliberate keystroke nobody uses mid-review, so it means the text was written somewhere else and pasted in. NeurIPS, COLM and MIDL all moved the same way. It tracks the calendar, not the venue.

So are LLMs now writing ML peer reviews?

We had Claude Opus 5 read 899 reviews blind, never showing it the year, scoring each 0-100 on how likely a machine drafted it.

Moderate suspicion tripled: scores of 50+ went from 9.7% to 33.3%.

High-confidence calls did not move. 85+ went from 2.0% to 3.7%, p = 0.22. Not significant.

The mass moved out of "clearly human" into the middle. It never arrived at "clearly machine." That is what polishing looks like, not drafting.

Everything else agrees. LLM vocabulary fell (delve: 3.1% to 0.4%). LLM rhetoric fell. Open-source AI detectors built on GPT-2 pointed the wrong way entirely. And ESL markers, the fingerprints of non-native English, fell by a quarter, 11.4% to 8.7%.

That last one reframes it. The people reaching for these tools are disproportionately the ones for whom writing English is work. The tell a native speaker notices, that smooth em-dashed prose, may be picking out exactly the reviewers who had the most to gain from the tool and the least to do with laziness.

Same researchers write the arXiv papers and the ML reviews. We showed last month that arXiv is 28x more people, not machine slop. Papers carry your name. Anonymous reviews carry nothing. Only the incentives flip, and the behavior flips with them.

Reviewers are not sending machines to do their thinking. They are sending their thinking through a machine on the way out.

Whether that is a collapse depends on where you think a review's value lives. If it lives in the judgment, this data says the judgment is intact.

Where do you think it lives?

<!-- model score
Scored with scripts/linkedin_scoring/score.py (trained on 48 prior posts).

  version                                  impressions  engagements
  v1 baseline                                     1008         13.2
  vB  + acronym density (ML, LLM, ESL)            1097         13.6   accepted (+9%)
  vC  vB + exclamation in hook                    1039         13.9   REJECTED (impressions -5%)
  vD  vB + GPT-2 detector line, more acronyms      1181         14.7   FINAL (+17% / +11% vs base)

Acronym density remains the strongest lever, consistent with upper_word_ratio being the
top format predictor and with the previous post's result (+56% there). The scorer again
suggested an exclamation while its own driver list is ambivalent; tested and rejected
on impressions, as in the arxiv-ai-flood post.

Blog link goes in the first comment, not the body (has_link is a negative driver).
-->
