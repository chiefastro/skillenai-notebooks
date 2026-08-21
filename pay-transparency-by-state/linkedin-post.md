In Washington state, 47% of job postings tell you what the job pays. In Kansas, 5.3% do!

We analyzed 118,706 US job postings across 38 states and measured one thing: does the posting contain a salary range?

The answer is mostly determined by law. States that require pay in the posting disclose at 43.3%; states with no law, 15.6%. A 2.8x gap.

But the number that surprised us was the first one. Even where the law requires a salary range, roughly half of postings still don't show one.

Four reasons stack up, and only one is employers ignoring the rules. Small employers are exempt (NY covers 4+ employees, NJ 10+, CA and WA 15+, MA 25+, MN 30+ — and MN, with the highest threshold of any mandate state, sits near the bottom of the mandate group). The law follows the job, not the employer, so out-of-state roles aren't covered just because the listing surfaces in your local search. Compliance is imperfect — the NY Fed puts it around 76%. And some of the gap is measurement error on our side, which we measured rather than assumed.

The middle category is the real confirmation. CT, NV and RI require disclosure only if you ask, and land at 22.3%, between the two groups. A weaker rule, a weaker result.

VA's mandate took effect July 1. ME's on July 28. DE follows in 2027. Fourteen jurisdictions require pay in the posting today. Five years ago, none did.

So if you're negotiating without an anchor right now, is that your employer's choice, or your state's?

<!-- model score
Scorer: scripts/linkedin_scoring/score.py (trained on 48 prior posts; CV R2 imp 0.268 / eng 0.402)
Final (draft 5): impressions 1667.9 | engagements 11.7 | followers_3d ~19 (ignored: CV R2 -0.254)

Revision ladder:
  d1 original                          874.3 imp /  9.5 eng
  d2 compressed list to prose,        1654.0 imp / 10.0 eng   (+89% imp)
     raised acronym density (NY/NJ/CA/WA/MA/MN/CT/NV/RI/VA/ME/DE)
  d4 + "just" in hook                 1604.2 imp /  9.9 eng   (reverted - hurt both)
  d3 + "just" + exclamation           1608.8 imp / 11.5 eng
  d5 + exclamation only  <- SHIPPED   1667.9 imp / 11.7 eng   (best on both)

Note for future sessions: the skill documents the "add an exclamation" suggestion as
unreliable (2026-05-03: -5% imp / -13% eng). That did not reproduce here. Isolating the
edits showed the exclamation alone was a clean win (+0.8% imp, +17% eng); the harm in the
combined test came from the word "just", not the punctuation. Test edits one at a time.

Posting notes: no URL in body (has_link is a negative driver) - put the blog link in the
first comment. No Unicode bullets (emoji_count negative). Ends with a question (positive).
-->
