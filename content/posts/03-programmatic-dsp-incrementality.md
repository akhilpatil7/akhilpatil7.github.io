---
title: "Two Roads to a Valid Control Group: Zip-Level Incrementality for Programmatic Ads"
date: 2026-06-20
tags: [incrementality, programmatic, mahalanobis-matching, clustering, synthetic-control, geo-experiments, causal-inference]
excerpt: "When you test a programmatic channel at the zip-code level, the entire experiment lives or dies on one thing: is your control group a real twin of your treatment? I ran two tests where the data situations were completely different — and each demanded a completely different way of building that twin."
---

## The hard part isn't the test. It's the twin.

I've written before about geo holdout tests — pause a channel in one area, keep a comparable area running, and use the divergence to measure the channel's true causal effect. The measurement math (difference-in-differences) is the easy part. The hard part, every single time, is constructing a **control group that is genuinely a twin of the treatment group.** If the control isn't a true counterfactual, every number that follows is decoration.

I ran two programmatic incrementality tests back to back — one for a channel in one state, one for a different channel in another. They shared a goal but almost nothing else: the data I had to work with was completely different in each case. So I used two different methods to build the control. This post is about *why the data situation should dictate the method* — and how each one works.

Both tests were run at the **zip-code level**, which is both a blessing and a curse: it gives you hundreds of small units to work with, but each one is noisy, so you can't just match single zips — you have to build *clusters* of zips into stable, comparable geographies.

---

## Road 1: A "statistical twin" via Mahalanobis matching

**The situation:** For one channel, I had almost no channel-specific history to lean on. Without a long track record to model a bespoke counterfactual, the most defensible move is to find a *matched twin* — a control cluster that looks statistically identical to the treatment cluster on the attributes that drive quoting behaviour.

Here's the pipeline I built:

**1. Grow candidate treatment zones.** Working inside a single county, I built a zip-adjacency graph (zips within a short distance of each other are "neighbours") and used a breadth-first search to grow contiguous patches of zips outward from the northern, southern, eastern, and western extremes — each patch constrained to a target population of roughly half a million, within a tight tolerance. Contiguity matters: a treatment geography scattered across a map is impossible to run cleanly and easy to contaminate.

**2. Build a valid donor pool.** For each candidate treatment patch, I excluded every zip within a minimum-distance buffer, so the control could never be geographically close enough to bleed advertising exposure into the treatment area. Spillover is one of the quietest ways a geo test lies to you.

**3. Match on statistical distance, not gut feel.** For every treatment/control candidate pair, I computed the **Mahalanobis distance** across a set of census and performance features — per-capita income, education, labour-force participation, quotes per capita, quote-completion rate, and close rate.

Why Mahalanobis instead of just "pick the closest-looking area"? Because the features are correlated and on wildly different scales. Income is in tens of thousands; a close rate is a fraction of one. A naïve distance would let income dominate and would double-count anything that moves with income (like education). Mahalanobis distance uses the inverse covariance matrix of the features to automatically **rescale each feature by its variance and discount correlated pairs** — so it measures how far apart two areas *really* are in the joint distribution, not in raw units. It's the difference between "these two zips have similar-looking numbers" and "these two zips are statistically the same kind of place." I added a small compactness penalty so the optimiser didn't reward a control patch that matched on paper but sprawled across the map.

**4. Validate before trusting.** A close statistical match on averages can still hide a divergent *trend*. So every top candidate pair went through a pre-period validation gate: the treatment and control had to move together week over week (a high correlation on weekly changes), have similar trend slopes, and be individually stable (low coefficient of variation). Only pairs that passed both the static match *and* the dynamic trend check survived.

The winner was the treatment/control pair with the smallest Mahalanobis distance *that also* tracked tightly in the pre-period — a genuine statistical twin, validated on both its profile and its behaviour over time.

---

## Road 2: A "synthetic twin" via clustering + optimisation

**The situation:** For the other channel, I had the opposite problem in a good way — a rich targeting history across a large, already-curated list of high-value zips. Here, rather than hunting for one matched twin, it made more sense to organise the whole market into natural groups and then *build* a synthetic control from them.

**1. Segment the market with clustering.** I engineered features for each zip and ran **K-means clustering**, using the silhouette score to guide how many clusters the data actually supported rather than picking a number arbitrarily. This grouped the zips into a handful of internally-similar, stable geographies.

**2. Choose the treatment cluster deliberately.** I selected the treatment cluster on a combination of stability, expected test duration, and the volume it would put in play — I wanted a cluster big and steady enough to give a decisive read without holding out so much spend that the business felt it.

**3. Build the synthetic control by optimisation.** For the control, I didn't use another single cluster. I solved a constrained optimisation (weights that are non-negative and sum to one) to find the **blend of the remaining clusters** whose combined pre-period trajectory best fit the treatment cluster's. The result was a synthetic twin — a specific weighted mix of several clusters — that shadowed the treatment cluster before the test began.

**4. Validate, and stress-test with placebos.** I checked the pre-period fit quality, and — as with every geo test I run — validated the machinery by **injecting a known artificial lift and confirming the model recovered it.** I also ran placebo tests (pretending untreated clusters were "treated" to see how often the method finds an effect where none exists), which is how you build confidence that a positive result is signal and not an artefact of the method.

---

## Same measurement, two very different stories

With valid twins in hand, both tests were read the same way — difference-in-differences across the full funnel (quote starts → completed quotes → sales), plus incremental cost-per metrics dividing spend by the volume each channel actually caused.

The findings were a study in contrasts, and taught a lesson that goes beyond either channel:

- **One channel was incremental all the way down the funnel**, strongest right at the sales line — a genuine full-funnel performer.
- **The other drove real volume at the top of the funnel but faded to almost nothing at sales** — it started quotes that didn't finish as purchases.

The tempting conclusion — "kill the second channel, scale the first" — is exactly the trap I flagged *against*. The efficient-looking channel had only been tested at a fraction of the other's spend, and cost-efficiency almost always erodes as you scale (you buy the cheapest, most responsive audiences first). Comparing a low-spend channel to a high-spend one and declaring a winner is comparing two things measured on different rulers. My recommendation was disciplined, not dramatic: **scale the promising channel in a controlled way and re-measure at comparable spend before reallocating** — and keep the other channel running while restructuring it toward conversion, rather than cutting the very baseline needed to judge it fairly.

## The takeaway

There is no single "correct" way to build a control group. The right method is the one your *data situation* can actually support:

- **Little channel history, need a defensible baseline fast → match a statistical twin** (Mahalanobis on the drivers, validated on trend).
- **Rich history across many units → segment and synthesise** (cluster, then optimise a weighted blend).

What doesn't change is the discipline around it: constrain geography so there's no spillover, validate the twin on both profile *and* behaviour, prove the method can recover a known effect before you trust it on an unknown one, and refuse to draw a comparison the experiment wasn't designed to support. The method flexes to the data. The rigour never does.

---

*Companion posts: the [social-channel geo holdout](01-meta-incrementality-geo-holdout.md) and the [paid-search cannibalisation test](02-paid-search-incrementality-cannibalization.md).*
