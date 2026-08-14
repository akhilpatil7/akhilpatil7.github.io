---
title: "Proving What Marketing Actually Works: A Geo Holdout Test for Social Ads"
date: 2026-04-20
tags: [incrementality, causal-inference, synthetic-control, difference-in-differences, marketing-analytics, experimentation]
excerpt: "Attribution tools tell you which ads got clicked. They don't tell you which ads actually changed someone's behaviour. Here's how I designed a geo holdout experiment to measure the true, causal contribution of a social advertising channel — and why the answer surprised everyone."
---

## The question nobody could actually answer

Every marketing team I've worked with lives with the same uncomfortable secret: the numbers on the dashboard are not the numbers that matter.

Platform attribution — the "this channel drove X quotes" figure that comes straight out of the ad platform — is built on a simple rule: *someone saw or clicked our ad, and later did something we care about, so the ad gets the credit.* That's correlation dressed up as causation. It quietly takes credit for people who would have converted anyway, and quietly ignores people the ads genuinely nudged but who converted through a different door.

For a direct-to-consumer auto insurer deciding how many dollars to put behind a social advertising channel, that gap isn't academic. Over- or under-invest by even a few percentage points of a large budget and you're lighting money on fire — or starving a channel that's actually working.

I led the design of an experiment to answer the real question: **if we turned this channel off, what would we actually lose?**

## Why you can't just "turn it off and see"

The naive version — pause the channel everywhere for a month and watch the numbers — is worthless, because the world doesn't hold still. Seasonality, competitor activity, pricing changes, and plain randomness all move quote and sale volumes week to week. If sales drop after you pause a channel, you have no idea how much of that drop was the channel and how much was just... February.

The fix is to run a **geo holdout**: keep the channel running everywhere except one geographic area (the *treatment* region), where you pause it. Then you compare the treatment region not against its own past, but against a **control** region that behaved just like it before the test. Whatever diverges between the two, after the pause, is the channel's causal fingerprint — because seasonality and market-wide movements hit both regions equally.

The whole game, then, comes down to one thing: **finding a control that is genuinely a twin of the treatment.** Get that wrong and every downstream number is fiction.

## Building a "synthetic twin"

No single real region is ever a perfect match for another. So instead of hunting for one lookalike, I built a **synthetic control** — a weighted blend of several untouched regions, combined so that the blend traces the treatment region's pre-test history as closely as possible.

I built this at the county level. For each candidate treatment county, an optimiser searched over all the other (untreated) counties and solved for the set of weights that minimised the gap between the synthetic blend and the real county across the pre-period — matching not just on the outcome trend, but on the demographic and behavioural drivers underneath it:

- education and employment profile,
- median household income,
- how many quotes the area generated per capita, and
- the channel's own share of quote activity in that area.

The result is a bespoke "twin" — say, *roughly 40% of one county, a third of another, and the remainder spread across a couple more* — that moves in lockstep with the treatment county historically, and therefore tells us what the treatment county *would have done* had we never paused anything.

To choose *which* county to actually test, I didn't pick by gut. I ran every candidate through the same pipeline and compared them on three things: how tightly the synthetic twin fit the pre-period (prediction error), how stable the donor pool was, and — critically — how long the resulting test would need to run. Some candidates looked great statistically but would have needed three-plus months to reach significance. I wanted a clean twin *and* a decisive read.

## Making sure the test could actually detect something

A control group only solves half the problem. The other half is **power**: if the channel really is driving, say, a 10–15% lift, is the test even capable of *seeing* a lift that size against the natural week-to-week noise — and if so, for how long does it need to run?

I ran a proper power analysis. Using the pre-period residuals (how much the real county wobbles around its synthetic twin even when nothing is happening) as the noise floor, I modelled statistical power as a function of test duration for a range of possible true lifts. The logic is intuitive: signal accumulates with the square root of time, so a bigger true effect crosses the detectability threshold sooner, and a smaller one needs patience.

That analysis produced concrete guidance the business could plan around: *to detect a lift of this size at this confidence level, run for roughly this many weeks.* I also validated the whole apparatus by **injecting a known, artificial lift into the data and confirming the model recovered it** — if you simulate a 10% lift and your method reports ~10%, you can trust it to measure the real thing. And I carved out the first few weeks as an "immature data zone," because early post-launch data is dominated by ramp-up noise and will mislead you if you read it too soon.

## Measuring the result: difference-in-differences

Once the test ran, measurement used **difference-in-differences (DiD)**. In plain terms:

1. Measure how the treatment region changed from before to during the test.
2. Measure how the synthetic control changed over the same window.
3. The *difference between those two changes* is the incremental effect.

Because both regions absorb the same seasonal and market-wide forces, subtracting one change from the other cancels those forces out and isolates what the channel itself did. I tracked this across the whole funnel — quote starts, completed quotes, and sales — because a channel can look very different depending on where you measure.

I also stood up a **monitoring dashboard** with guardrails while the test was live, so we could catch a broken control or a contaminated treatment early rather than discovering it in the post-mortem.

## What we found — and why it was more interesting than a single number

Three findings mattered more than the headline lift:

**1. The channel was genuinely incremental — but not where attribution said it was.** The platform's own attribution told a top-of-funnel story: lots of credit for quote starts, very little for sales. The incrementality read told almost the opposite story — the channel's real value showed up *lower* in the funnel, on sales, precisely where click-based attribution is blindest. The two measurement systems disagreed by multiples, in *both* directions depending on the metric.

**2. "Incremental" and "efficient" are different questions.** A channel can be truly causal and still be a poor place for the *next* dollar. So I modelled marginal efficiency across a range of spend levels and compared each to the blended, all-channel benchmark. That located the point where the channel crosses from "pulling the average down" into diminishing returns — turning a vague "should we spend more?" into a defensible "hold here; scaling further isn't supported by the data."

**3. I was honest about what the test could and couldn't prove.** The most valuable part of the write-up was the limitations section. The channel wasn't perfectly excluded from the treatment region, which meant the true effect was likely *larger* than measured — so the numbers were conservative. And incremental sales volume was thin enough that the sales figure had to be treated as directional, not gospel. I recommended replicating in a second state before anyone applied these coefficients nationally. Overstating confidence would have been the easiest way to destroy trust in the whole method.

## Why this mattered

The deliverable wasn't a lift percentage. It was a **decision framework**: a defensible spend level for the channel, a correction to how attribution was feeding the company's marketing-mix model, and a repeatable testing pipeline — control construction, power analysis, DiD readout, monitoring — that could be pointed at the next channel and the next state.

That last part is the real payoff. The first geo holdout is a project. The *tenth* is a capability. By the end, "how do we know this actually works?" had a real answer, and a repeatable way to get it.

---

*Part of a series on causal measurement in marketing. Companion posts cover the [paid-search holdout with organic cannibalisation](02-paid-search-incrementality-cannibalization.md) and the [two-philosophy approach to programmatic control selection](03-programmatic-dsp-incrementality.md).*
