---
title: "Where Should We Spend Next? Building a Market-Opportunity Index"
date: 2026-05-15
tags: [marketing-analytics, geo-analytics, index-design, tableau, sql, decision-support]
excerpt: "A media team was allocating budget across hundreds of geographic markets on gut and last-quarter's numbers. I built a single, normalized index — one number per market — that blends demand headroom, conversion efficiency, and customer loyalty into a live map of where the next advertising dollar works hardest."
---

## The problem: too many markets, not enough signal

A consumer insurance business advertises across hundreds of geographic markets — zip codes, counties, media markets, whole states. Each one has a different population, a different competitive picture, a different mix of how many customers are already there and how well they stick. The media team's recurring question is deceptively simple: **given a finite budget, which markets deserve more, and which are already tapped out?**

The honest answer, before this project, was "we look at last quarter's cost-per-sale and argue about it." That misses the point in two directions. A market can have a great cost-per-sale simply because it's small and saturated (no *headroom* left), or a mediocre one because it's large and under-penetrated (huge headroom you're barely touching). Raw performance numbers don't separate "efficient" from "opportunity."

I set out to compress that whole judgement into **one comparable number per market** — an index — refreshed daily and sliceable by geography and channel.

## The design principle: normalize everything to the footprint average

The core idea that makes the index usable is normalization. Every component is expressed **relative to the company's own overall average, which is pegged at 1.00.** A market that scores 1.25 on a component is 25% above the company average; 0.80 is 20% below.

Why this matters: it makes wildly different metrics — a close rate (a few percent), a penetration rate (a fraction of households), a retention rate (most of a policy book) — directly comparable and combinable. You stop asking "is a 7% close rate good?" and start asking "is this market above or below where we typically operate?" That's the question a media planner can actually act on.

## What goes into the index

I built the index from three families of signal, each answering a different strategic question:

**1. Headroom — is there room to grow here?**
Using census data on households that own vehicles as the addressable market, I measured **market penetration** (policies in force ÷ addressable households) and its inverse, **opportunity** (the un-penetrated share). A market can only reward more spend if there are still customers left to win.

**2. Efficiency — do we convert well here?**
A **close-rate index** (sales ÷ quotes, relative to the footprint average) captures how well demand converts once we generate it. High headroom with poor conversion is a trap; high headroom *and* strong conversion is where you lean in.

**3. Loyalty — do customers stay?**
Retention indices at both 90-day and one-year horizons (retained ÷ issued, relative to average) capture whether the customers a market produces actually stick — because acquiring customers who churn is expensive growth. I also layered in a **cross-sell/bundling opportunity** signal (where auto customers are eligible but not yet bundled with home), since a market's value isn't just new auto policies.

## Rolling it into one score — with weights the business controls

The headline **Enterprise Market Index** is a **weighted blend** of these component indices. Crucially, I didn't hard-code the weights. I exposed them as **parameters the media team can tune** — dialling up close-rate efficiency when the goal is profitability, or headroom when the goal is growth. To keep the tool honest, I built a validation check that flags the user if their weights don't sum to 100%, so the index can never be silently mis-specified.

The whole thing is **interactive by design**:
- A geography switch re-computes the index at zip, county, or media-market grain.
- A channel switch re-scopes it to the enterprise, direct, or partner channels.
- A traffic-light layer colours the top third of markets green, the middle amber, and the bottom third red — *"caution on incremental spend here."*

## Under the hood

The data pipeline is a daily-refreshed SQL build that assembles two rollups (county and media-market), each a full outer join of a **demographics layer** (addressable households, home eligibility, all census-weighted) and a **performance layer** (quotes, sales, declines, policies in force, and issued/retained counts at 90-day and one-year horizons) broken out by channel. I built in explicit data-quality checks that surface any geography present in one reference table but missing from another — because an index silently dropping markets is worse than an index that tells you it's incomplete. The presentation and the index math live in a Tableau layer using level-of-detail expressions to compute each "relative-to-average" ratio correctly regardless of the current filter.

## Why it mattered

The deliverable replaced "which markets *feel* hot?" with a **defensible, transparent, self-serve ranking** the media team could interrogate themselves. Instead of a monthly analyst request, they had a live map: sort by the index, read the colour, check which component is driving the score, and allocate accordingly. And because the weights are theirs to set, the tool adapts to whatever the quarter's strategy is — growth, efficiency, or retention — without an analyst rebuilding anything.

## What I'd sharpen next

Two things. First, low-volume markets are inherently volatile — a handful of quotes can swing a rate — so I'd add explicit volume-based confidence banding (or Bayesian shrinkage toward the footprint average) so planners don't overreact to noisy small markets. Second, the index describes *current* attractiveness; pairing it with the incrementality coefficients from my geo holdout tests would turn it from "where are we efficient today" into "where would the next dollar be *causally* most productive" — which is the question underneath the question.

---

*An index tells you where opportunity sits. To learn how I measured whether spend actually **causes** results, see the [geo holdout incrementality series](01-meta-incrementality-geo-holdout.md).*
