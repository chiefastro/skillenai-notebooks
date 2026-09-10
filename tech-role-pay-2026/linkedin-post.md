Which tech role pays the best in 2026?

We measured 62,805 US job postings that disclose a salary range. The answer is ML and AI research roles: Research Scientist at $215K and ML Engineer at $209K at the senior rung, with AI Engineer fourth at $198K.

Now the part that should actually change what you do. The gap between an ML Engineer and a plain Software Engineer is $16K. The gap between a mid-level and a staff-level engineer doing the same job is $65K. One rung is worth three role switches.

The ML premium is real, to be clear. Across the 37 employers that post both roles at the senior rung, ML Engineer pays more at 25 of them — same companies, same level. It's just small.

Three things surprised us. The top of the board is compressed: ranks 1 through 13 span $215K to $180K, so most of the engineering market sits inside a $35K band, and the top two roles aren't statistically separable from each other at all. The real cliff is analyst to engineer — Data Analyst sits $63K below Software Engineer at the same rung, and no engineer-versus-engineer gap comes close (DS vs SWE is $18K). And the advice inverts by tier: if you're a mid-level engineer the promotion is the whole game, but if you're an analyst the tier boundary is worth $63K to $86K, far more than any promotion inside it.

Of four factors setting your pay, the job title explains the least: seniority rung 0.261, employer 0.223, US state 0.195, role label 0.168. A posting in Florida advertises 33% less than the same role and rung in California.

We also threw out eight job titles. Our first leaderboard was topped by Research Engineer at $260K, until we noticed 27% of those postings came from one employer — drop them and it's $220K. When 85% of "Mission Software Engineer" postings trace to a single defense manufacturer, that title is one company's internal ladder, not a market rate.

Full breakdown, all 28 roles, methodology in the comments.

What would move your pay more this year: the title, or the rung?

<!-- model score
Scorer: scripts/linkedin_scoring/score.py (trained on 48 of the author's own posts)
CV R2: impressions 0.268, engagements 0.402, followers_3d -0.254 (followers target unreliable, not cited)

v1  baseline (14 blocks)                impressions 7,808  engagements 35.9
v2  consolidated blocks (10)            impressions 7,800  engagements 37.6   ACCEPTED (+4.7% eng, line_count
                                                                              dropped off the negative drivers)
v3  + "The answer surprised us!" hook   impressions 7,195  engagements 37.6   REVERTED (-7.8% imp)
v4  + exclamation only, no new words    impressions 7,491  engagements 37.7   REVERTED (-4.0% imp)

Conclusion: the scorer's standing "add an exclamation" suggestion is WRONG for this draft, and v4
isolates why - the punctuation alone costs ~4% impressions, independent of the wording change in v3.
Consistent with the skill's note that this suggestion is draft-dependent and must be tested, not applied.

Top positive drivers present: upper_word_ratio (0.489 - ML, AI, DS, SWE acronyms), word_count (0.262),
ends_with_question (0.191), ngram "scientist" (0.51).
Link kept out of the body; goes in the first comment.
-->
