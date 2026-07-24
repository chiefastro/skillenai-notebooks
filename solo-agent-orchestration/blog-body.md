![The Real AI Development Barrier: The Coordination Tax — a broken-axis chart. Below the break, one million developers plateau near 4 merged PRs per week on the Jellyfish curve; above the break, one solo developer's weeks sit at 20 to 36 PRs on a different scale entirely](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/07/24/e955cb79-d6bf-4b65-9c50-5facd727e73f/uwbD0fjk8DA-01-hero-meme.png)

Jellyfish published a chart I can't stop thinking about. They took **one million developer-weeks** of Cursor and Claude Code usage and plotted tokens spent per week against merged PRs shipped per week. Two "headwinds" fall out of it:

1. **The Agentic Barrier (~50M tokens/week).** Below it, you're doing interactive, autocomplete-style coding. Above it, you've handed real work to autonomous agents.
2. **Diminishing returns.** Past the barrier, the curve bends over and flattens toward **~4 merged PRs per developer per week**. Spend more tokens, get almost nothing back.

It's a good chart. Careful, well-sampled, honest about its own shape. So I dropped my own numbers onto it — I run a solo, nights-and-weekends Skillenai side project with a fleet of Claude Code agents — fully expecting to land somewhere respectable on the curve.

I did not land on the curve. That purple smear across the top of the chart is me.

## Where I actually land

Over the eight weeks I have clean token logs for (June–July 2026), here's the comparison:

| Metric | Jellyfish population | Me (solo + agents) |
|---|---|---|
| Median tokens / week | *chart tops out at 500M* | **419M** |
| Peak tokens / week | 500M (right edge) | **1.17B** — 2.3× off the chart |
| Median merged PRs / week | curve ceiling ~**3.9** | **23** |
| Best week | — | **36** |

My *median* week sits about **6.4× above** the curve's PR ceiling. My busiest token week runs clean off the right edge of their plot. Even my two laziest weeks — 6 and 8 PRs — clear the top of their chart.

![My eight weekly points on the Jellyfish curve, all far above the ~3.9 PR ceiling](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/07/24/e955cb79-d6bf-4b65-9c50-5facd727e73f/Tous-14HKr0-02-placement.png)

## This isn't one heroic week

It's the steady state. Most weeks land 20–36 merged PRs and 5–16 completed tickets, spread across **six repositories** — a Fargate backend, a data pipeline, a public API and plugin set, and a notebooks repo. In a company, that surface area is three or four teams with three or four standups.

![Weekly tokens, merged PRs, and completed tickets across the eight-week window](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/07/24/e955cb79-d6bf-4b65-9c50-5facd727e73f/rqIOE_Vi_40-03-weekly.png)

Across the full window it's **573 merged PRs**. And the tickets — a separate, coarser tracker of *units of work finished* — move right alongside the PR count. That matters, because it means the number isn't an artifact of chopping work into tiny PRs to game a metric. Real things got finished.

## So why doesn't the plateau apply to me?

Here's the claim I'll actually defend: **the Jellyfish curve flattens because of coordination, and I don't pay for any.**

In a [companion Skillenai analysis](https://skillenai.com/2026/06/15/how-to-build-agents-in-2026-low-level-runtimes-vs-orchestration-frameworks) I've been picking apart how engineering orgs spend their marginal effort, and the pattern is stubborn: coordination is nearly invariant — roughly **7–9 engineers per manager** — and most of it gets *badged* as engineering-management, TPM, and product-owner headcount rather than shown as the overhead it is. The bigger the team, the larger the fraction of every new hour that disappears into standups, handoffs, review queues waiting on a human in another timezone, and the sheer work of keeping N people's mental models in sync. That is the Coordination Tax, and it is exactly the kind of cost that makes an output curve bend over. You add capacity, and the capacity gets eaten by the friction of using it together.

A solo human plus a fleet of agents has a **span of control of zero.** The agents *are* the team, and they need no coordinating with each other. No standup. No handoff. No cross-team dependency. No PR sitting for two days waiting on a reviewer. The marginal token goes almost entirely into *work* instead of into *coordinating the work* — so the thing that flattens team output simply isn't in the room.

Notice what this argument is **not**. It is not "the model is superhuman." If the plateau were a model-capability ceiling, it would cap me too — and it plainly doesn't. I'm at 23, not 4. Whatever separates me from the million-developer-week average isn't the model. It's the org chart.

## The economics are the funny part

![Two bars: ~6 developers' worth of output, and $3,032 of API-list value delivered for a $100/month subscription](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/07/24/e955cb79-d6bf-4b65-9c50-5facd727e73f/QyAsmqGWRvI-04-economics.png)

Two numbers make the "virtual team" framing real:

- **~6 developers' worth of merged output.** 23 PRs/week ÷ 3.9 (the Jellyfish per-dev ceiling) ≈ **5.9** — precisely the team size at which span-of-control math says you'd hire a manager. I get that team's throughput and skip both the team *and* the manager.
- **A payroll of about $100/month.** Tooling prices my usage at **$3,032** for the eight weeks — but that's the *API list-price equivalent*, not what I pay. I'm on a **$100/month Claude subscription**. My real out-of-pocket for the window is roughly **$180**. The subscription delivers around **17× its list value** — call it $1,700/month of usage for a $100 bill.

And none of it is cheap-model filler: **98.9% of my tokens and 99.6% of the cost are Opus**, almost entirely Opus 4.8. This is premium-model work, not a haiku token count run up to look impressive. (For the curious: **97% of those tokens are cache reads**, billed at roughly a tenth of the input rate — and that discount is *already* in the $3,032. Priced without caching, the list number would be closer to $50K.)

### The pricing model is the real unlock

This is, honestly, why I moved from Cursor to Claude Code. Cursor's pricing is usage-based — and it more or less *has* to be, because it pays third-party model vendors per token. Every token you spend is a token it owes upstream, so it can't just eat your usage behind a flat fee. (Even its push into in-house models is partly an attempt to escape that pass-through.) A subscription that swallows the token cost can really only exist when the vendor also *owns* the model.

That structure — not any single feature — is what makes "just let the agents run" a rational default instead of a running budget decision. Metered per-token at these volumes, I'd flinch every time I kicked off a fleet, and I'd instinctively throttle myself back down into the "interactive coding" band. The flat plan removes the meter, and removing the meter is what lets you sit on the far right of that x-axis at all. The plateau on Jellyfish's chart is largely coordination — but the reason *anyone* reaches orchestration scale is partly which pricing model they happen to be standing on.

## The honest caveats

I'd rather hand you these than have you find them:

- **What "tokens" means.** About 97% of my volume is cache reads — agents re-reading large contexts. On a *billable-non-cache* definition, my weekly input+output is only ~0.5–6M, which would drop me to the far **left** of the chart. I read Jellyfish's axis as total throughput (their 50M starting point is unreachable otherwise), but you should know the metric is load-bearing here.
- **PR granularity.** A big share of these PRs are authored by agents inside orchestrated flows. They're plausibly finer-grained than a human's hand-written PR, so "23 PRs" is a claim about *merged throughput*, not 23 acts of individual genius. The tickets number is the more conservative read.
- **The tax buys something.** Coordination isn't pure waste. It buys shared context, mutual error-catching, and institutional memory. A solo-plus-agents setup skips the tax partly by skipping what it pays for — which is fine for a side project and emphatically *not* fine for a bank.
- **n = 1.** One person, eight weeks, one setup. This is a demonstration, not a study.

## What I take from it

The plateau is real — for teams. It's a curve built from developers embedded in orgs, and it measures coordination drag at least as much as it measures the tool. Pull the coordination out, keep the tool, and the curve stops describing you.

For a solo builder, that's a genuinely new thing: the reach of several teams, on premium models, for the price of a gym membership — as long as you remember that the same thing you deleted to get here (a second pair of human eyes) is the thing you'll miss the moment the work stops being a side project.

Look what's possible after hours.

---

*Full methodology, data, and the code that made these charts: [github.com/skillenai/skillenai-notebooks](https://github.com/skillenai/skillenai-notebooks/tree/master/solo-agent-orchestration). Reference chart: [Jellyfish Research, "Two Headwinds of AI Development."](https://jellyfish.co/)*
