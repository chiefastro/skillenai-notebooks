Jellyfish studied 1 million developer-weeks of Cursor and Claude Code and found AI dev output plateaus at ~4 merged PRs per week.

Last week for Skillenai I shipped 23. Solo. After hours.

I dropped my own numbers onto their chart expecting to land somewhere on the curve. Instead I landed off the top of it. My median week: 419M tokens and 23 merged PRs, about 6.4x above their "diminishing returns" ceiling. Across the quarter, 573 merged PRs across six repos.

So why doesn't the plateau apply to solo devs?

It isn't the model. If it were a capability ceiling, it would cap me too. The real answer is the Coordination Tax.

That curve is built from developers embedded in orgs, where every marginal hour gets eaten by standups, handoffs, and review queues waiting on another human.

As a solo dev with a fleet of agents, I make every decision unilaterally. I am the coordination layer between them (approving PRs, assigning tasks). Together we ship the same output as a full team (6x a single dev).

This is itself a coordination tax barrier on my agent team. I'm the bottleneck limiting us to 1 team's worth of output. Scaling further would require solving agent to agent self-coordination. I'm not there yet because I don't trust any agent to manage its own team of agents (yet).

One note on cost:
99% of my tokens are Opus 4.8. I'm on a $100/month plan that delivers about $1,700/month of API-list usage. The subscription is the quiet unlock: metered per-token, I would flinch every time I started a run and throttle myself back down the curve.

So the plateau is real for teams. But pull the coordination out, keep the tool, and the curve stops limiting you.

Where does the plateau really come from for you: the model, or the org chart?

<!-- This is the version Jared published (supersedes the model-scored draft). Key thesis correction vs. the first draft: the solo dev does NOT escape the coordination tax — he becomes the single coordination layer, which caps output at exactly one team's worth (~6x). The tax is relocated onto the one human, not eliminated. -->
