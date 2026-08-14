---
title: "Deciding Where — and With Whom — to Spend: A Media Targeting Toolkit"
date: 2026-05-22
tags: [marketing-analytics, geo-targeting, hypothesis-testing, feature-weighting, vendor-evaluation, statistics]
excerpt: "Two questions sit under every programmatic budget: which micro-markets to target, and which vendor to trust. I built a reusable framework for the first — a weighted zip-ranking index — and used device-level significance testing to settle the second."
---

Programmatic advertising gives you an enormous amount of control and, with it, an enormous amount of rope. You can target down to the zip code and buy through competing vendors on competing devices. The flip side is that most of that granularity is decided by habit. I built two pieces of analytical machinery to replace habit with evidence: a **zip-ranking framework** for *where* to spend, and a **device-level significance test** for *how* to spend it.

## Part 1 — A weighted index for ranking micro-markets

The targeting question at the zip level is: out of thousands of zip codes, which handful actually deserve budget? "High population" is naïve (big and unprofitable is still unprofitable). "High close rate" alone is naïve too (a great rate on a tiny, thin zip is noise). The right answer blends several signals with deliberate weights.

I built a transparent **performance index** per zip that combined internal performance and quality signals into a single rank:

- **Close rate** — the dominant driver, carrying the largest weight, because ultimately we're buying conversions.
- **Quote demand per capita** — is there active shopping intent here?
- **Customer-value proxies** — scaled measures of the lifetime-value quality of the quotes and sales a zip produces, so we favour zips that yield *good* customers, not just many.
- **Target-market share** — the share of a zip's activity that falls in our preferred customer segments.
- **A decline-rate penalty** — the one *negative* term, docking zips that generate a lot of ineligible or declined traffic (expensive dead ends).

Two design choices made it robust:

1. **Min-max scaling** of the value and population signals, so features on different native scales could be combined without one silently dominating.
2. **A population floor** — zips below a minimum population are zeroed out entirely, because a spectacular-looking rate on a handful of quotes is a mirage.

**From ranking to selection.** I sorted zips by the index, took a running cumulative sum of population, and selected the top-ranked zips that together captured a target share (~70%) of the population — a principled cutoff that grabs the best markets while retaining enough reach to matter. The remainder became the natural control/exclusion pool. That single mechanism did double duty: it picked targeting lists *and* fed the treatment/control splits for the geo experiments I ran later.

The result was a **reusable, auditable framework** — point it at a new state, and it produces a ranked, defensible targeting list with the weights and cutoffs all visible and adjustable, rather than a black box or a gut call.

## Part 2 — Settling a vendor question with a significance test

The second question was operational: within a programmatic vendor's delivery, **which device types are actually worth buying?** The dashboards showed device-level differences, but differences on a dashboard are not the same as *real* differences — small samples produce fake gaps all the time.

So I treated it as a proper statistics problem. For each channel–device combination (display / native / video × desktop / phone / tablet), I computed the funnel-efficiency metrics — click-through, quote-conversion, and cost-per-quote — and then ran **two-proportion Z-tests on the conversion rates between device pairs**, reporting Z-scores, p-values, and significance flags at the 5% level.

That turned "tablet looks weak" into "tablet's conversion deficit is **statistically significant** (p < 0.05), and its cost-per-quote is several times worse than desktop's." Desktop was the efficient workhorse, phone a solid second, and tablet a genuine drag — not just noise. On the strength of that test, tablet was pulled from prospecting campaigns and retained only for cheaper retargeting. A concrete spend decision, backed by a hypothesis test rather than a glance at a bar chart.

I packaged the whole thing as an **automated performance-read tool**: it parses each creative's structured naming convention into dimensions (product, tactic, targeting, placement), buckets creatives into performance tiers by percentile, and produces the funnel and significance read on a fresh data pull — so the analysis is repeatable every reporting period instead of rebuilt by hand.

## Part 3 — Choosing between vendors, fairly

The same discipline settled a head-to-head between two programmatic vendors. Rather than compare their blended numbers (which conflate targeting, spend level, and audience), I split the market into two comparable geographies using the zip-ranking framework above, ran each vendor in its own geo, and compared like-for-like on volume and efficiency. The challenger vendor came out ahead as a volume driver, and the recommendation to shift toward it rested on a controlled comparison rather than a sales pitch.

## The throughline

Both halves of this toolkit express the same belief: **granular decisions deserve explicit, testable logic.** A weighted index makes the "where to target" decision transparent and adjustable instead of intuitive. A two-proportion Z-test makes the "which device" decision rigorous instead of impressionistic. And splitting a market into matched geographies makes a "which vendor" decision a controlled comparison instead of an argument. None of it is exotic — it's the discipline of writing the decision rule down, weighting it on purpose, and testing whether the differences you're acting on are real.

---

*This zip-ranking framework also fed the treatment/control selection in my [programmatic incrementality tests](03-programmatic-dsp-incrementality.md).*
