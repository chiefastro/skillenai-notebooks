Jellyfish studied 1 million developer-weeks of Cursor and Claude Code and found AI dev output plateaus at ~4 merged PRs per week.

Last week I shipped 23. Solo. After hours.

I dropped my own numbers onto their chart expecting to land somewhere on the curve. Instead I landed off the top of it. My median week: 419M tokens and 23 merged PRs, about 6.4x above their "diminishing returns" ceiling. Across the quarter, 573 merged PRs across six repos, running a fleet of Claude Code agents while I slept.

So why doesn't the plateau apply?

It isn't the model. If it were a capability ceiling, it would cap me too. The real answer is the Coordination Tax. That curve is built from developers embedded in orgs, where every marginal hour gets eaten by standups, handoffs, and review queues waiting on another human. A solo human plus a fleet of agents has a span of control of zero. The agents are the team, and they need no coordinating with each other. The marginal token goes into work, not into coordinating the work.

Two things that make it real:
- Roughly 6 developers worth of merged output, which is precisely the team size that would need a manager.
- 99% Opus 4.8, on a $100/month plan that delivers about $1,700/month of API-list usage. The subscription is the quiet unlock: metered per-token, I would flinch every time I started a run and throttle myself back down the curve.

The plateau is real for teams. Pull the coordination out, keep the tool, and the curve stops describing you.

Where does the plateau really come from for you: the model, or the org chart?

<!-- first comment (keep the URL out of the post body): Full writeup + charts: https://skillenai.com/2026/... (dated permalink after you publish) -->

<!-- model score (v2, chosen): impressions=712, engagements=7.9, followers_3d=12.4 | v1=709/7.9/12.2.
Suggestions NOT applied: (1) add exclamation — skill-flagged unreliable and exclamation_count is a negative driver in this draft; (2) more capitalized acronyms — contradicted by per-draft upper_word_ratio contribution (-0.304, largest drag). Clean lever used: word_count (+0.133). Gain <2% => stopped per skill guidance. Absolute numbers noisy (CV R2 0.27/0.40); used for relative ranking only. -->
