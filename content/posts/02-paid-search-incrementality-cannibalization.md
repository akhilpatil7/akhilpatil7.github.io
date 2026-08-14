---
title: "How Much of Paid Search Is Just Buying Clicks You'd Get for Free?"
date: 2026-04-27
tags: [incrementality, paid-search, cannibalization, difference-in-differences, causal-impact, marketing-analytics]
excerpt: "Paid search is the channel everyone trusts and nobody questions. So I ran a holdout test that asked an uncomfortable question — when we pause paid search, how much of that traffic just comes back through organic for free? The answer reshaped how the budget was allocated."
---

## The most trusted channel deserves the most scrutiny

Paid search always looks like a hero on the dashboard. Someone types your brand into a search engine, clicks your ad, gets a quote — and the ad takes full credit. Of course it does; it was the last thing they touched.

But that story has a hole in it. If someone is already searching for your brand by name, how much did the *ad* really do? If you'd shown no ad at all, a lot of those people would have scrolled one inch further and clicked your organic (free) listing instead. You'd have gotten the quote anyway — without paying for the click.

This is **cannibalisation**, and for a company spending a large share of its total marketing budget on paid search, it's a multi-million-dollar question hiding behind a green number. I designed and led a geo holdout test to measure it directly.

## The design: pause paid search in a mirror-image market

The core method is the same geo holdout logic I use across channels: keep paid search running everywhere except a **treatment county** where we pause it, and compare against a **control county** that had moved in lockstep with it beforehand. Difference-in-differences (DiD) does the rest — it compares the *change* in the treatment market to the *change* in the control market, so seasonality and market-wide swings cancel out and only the channel's causal effect remains.

But I built in a twist that made this test far more useful than a single lift number. I split the treatment into **two separate experiments running in parallel:**

- In one market, I paused **all** paid search.
- In another, I paused **only branded** search (ads triggered by our own name), leaving generic/non-brand search running.

Why? Because "is paid search worth it?" and "is *branded* paid search worth it?" are completely different questions. Branded search is where cannibalisation should be worst — those are the people already looking for you. Running the two arms side by side let me isolate exactly that.

Control and treatment counties were selected on matched demographic and performance profiles so the comparison was apples-to-apples, and one market was maintained as the untouched control throughout.

## Measuring it three ways, on purpose

For the readout I didn't rely on a single method. I triangulated:

1. **Manual difference-in-differences** on the pre/post × treatment/control cells — transparent, auditable, easy to explain to a non-technical stakeholder.
2. **A Bayesian structural time-series model** (Google's CausalImpact approach), which builds a counterfactual prediction of what the treatment market *would have done* and gives proper confidence intervals and significance around the gap.
3. **A power analysis** to confirm the test was long enough to detect an effect of the size we cared about before I trusted any of it.

When a hand-built DiD and a Bayesian counterfactual model agree, you can stand behind the result in a room full of skeptics. That mattered here, because the result was pointed.

## What the test revealed

**Paid search was genuinely incremental — meaningfully so on quotes, and even more so on sales.** Turning it off caused a real, measurable loss that organic did *not* fully replace. So the channel earns its place. Good.

But two findings changed the conversation:

**Organic partially backfilled the lost volume — and much more so for branded.** When paid search went dark, a chunk of the "lost" quote volume reappeared through organic search, for free. In the all-search market that recapture was modest. In the branded-only market it was roughly *half* — confirming the suspicion that a large share of branded paid-search spend was buying clicks the company would have won organically anyway. That's a direct, evidence-based case for reallocating budget from branded toward non-brand search, where the incremental value is real.

**Attribution was wrong in both directions.** The company's last-touch model was significantly *overstating* paid search's contribution to quotes (it was grabbing high-intent users who'd have converted regardless) while *understating* its contribution to sales (it was missing the assisted, lower-funnel conversions). The channel was fundamentally more of a *sales* engine than a *quote* engine — the opposite of how it was being optimised. Any bid strategy tuned to the last-touch quote number was optimising against a misleading signal.

## From measurement to money

An incrementality read is only useful if it changes a decision. This one produced four:

- **Hold overall paid-search budget at its current share** — my marginal-efficiency model showed spend was sitting right at the diminishing-returns inflection point, where the next dollar starts costing more than the channel average.
- **Shift budget from branded to non-brand search**, with a clear hypothesis and a follow-up measurement window to confirm the efficiency gain.
- **Stop optimising to last-touch cost-per-quote**, and feed the true incremental coefficients into the marketing-mix model so its saturation curves stopped being built on a biased input.
- **Replicate in additional states** before applying the coefficients nationally — because one market in one competitive environment is a directional read, not a universal law.

I also grounded the numbers in the live competitive context using auction-insight data: the cost environment had shifted as competitors entered and exited the auction, so I flagged that the coefficients were calibrated to *current* conditions and would need refreshing if the competitive picture changed. Context like that is the difference between a number and a *trustworthy* number.

## The lesson

The instinct in marketing analytics is to defend the channels that look good. The more valuable instinct is to *interrogate* them — especially the trusted ones — because that's where the hidden waste lives. Branded paid search looked untouchable on the dashboard. A well-designed experiment showed half of it was, in one market, effectively redundant. That's not an argument to cut the channel; it's an argument to spend the same money smarter.

Causal measurement doesn't just tell you what works. It tells you what you were fooling yourself about.

---

*Companion posts: the [social-channel geo holdout](01-meta-incrementality-geo-holdout.md) and [selecting valid control groups for programmatic tests](03-programmatic-dsp-incrementality.md).*
