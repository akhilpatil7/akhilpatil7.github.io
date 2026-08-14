---
title: "Predicting Customer Value When You Barely Have Any Labels"
date: 2023-11-05
tags: [machine-learning, regression, survival-analysis, feature-engineering, genetic-algorithms, honest-modeling]
excerpt: "Sometimes the most honest, most senior thing a data scientist can do is admit the standard model doesn't work — and engineer a defensible answer anyway. This is the story of predicting a value metric for seven million people when fewer than two percent of them had a usable label."
---

## The problem that breaks the textbook

The task sounded routine: predict a **customer-value metric** — a proxy for how much long-term value an individual represents — for a large prospect population, so marketing could prioritize the high-value people.

The catch was the labels. The value metric can only be computed for people who became customers and built up policy history. My target population was roughly **seven million individuals** in a third-party demographic file — almost none of whom were existing customers. When I matched the demographic file against internal policy data to find people with a computable value label, I was left with a usable-label set **on the order of one percent of the population.** And that one percent wasn't a random sample; it was the self-selected slice of people who had already chosen to buy. Training on it and extrapolating to the other 99% is exactly the kind of thing that produces a confident, wrong model.

This is the situation the textbook doesn't cover. So the project became less about fitting a model and more about *being honest about what could and couldn't be predicted* — and still shipping something useful.

## Trying the obvious things (and watching them fail)

I didn't skip to a clever solution; I earned it by exhausting the standard ones and documenting why each fell short.

**Standard regression.** I engineered features from the demographic attributes and trained linear models, random forests, and support vector regressors on the labelled slice. The predictive power was essentially **nil — R² barely above zero.** The demographic attributes simply didn't carry enough signal about individual customer value, and the tiny, biased label set gave the models nothing to hold onto. A less careful analyst ships the random forest anyway and calls the near-zero R² a "baseline." I treated it as evidence.

**Survival analysis.** Because customer value is partly about *tenure*, and tenure is right-censored (many customers are still active, so you don't yet know how long they'll stay), I reframed it properly as a survival problem using Cox proportional-hazards and parametric survival models. This was more principled, and gave a modest concordance — but converting survival curves into a usable per-person value prediction still carried large error. Better reasoning, still not a trustworthy individual-level number.

The consistent verdict across every approach: **you cannot reliably predict this metric for an individual from this data.** That's not a failure to report quietly; it's the central finding, and pretending otherwise would have been the real failure.

## The custom model: predict the group, not the person

If individuals couldn't be predicted, *segments* could. People who look alike on the value-driving attributes tend to have similar value on average — even when any single person is unpredictable. So I built a **custom, segment-average model** grounded in that logic.

The construction was the interesting engineering:

1. **Reconstruct the value-driving factors.** Insurance value is driven by a known set of rating factors (credit band, coverage level, prior tenure, incident history, and so on). Those aren't directly present in a demographic file, so I engineered *proxies* for them by grouping, scaling, and combining ~65 demographic attributes into factor scores.

2. **Calibrate the proxies to reality with a genetic algorithm.** A proxy is only useful if it lines up with the real factor. To tune the cutoffs that mapped my engineered scores onto the actual rating levels, I used a **genetic algorithm** (an evolutionary optimizer) to search for the percentile boundaries that best reproduced the real factor distributions — a global search over a rugged space that grid search handled poorly.

3. **Assign value by segment average.** I partitioned the population into segments defined by these reconstructed factors — over a thousand of them — and assigned each person the *average observed value of the actual customers who fell into their segment.* For segments with no matched customers, I imputed from the nearest neighbouring segments by overall score.

The philosophy: don't claim to know an individual's value; place them in a well-defined peer group and assign the group's empirically observed average. Humble at the individual level, defensible at the level the business actually acts on.

## Validating honestly

The validation is where I think the maturity of the project shows. I tested the model at two levels and reported *both*:

- **At the individual level, it fails** — a paired test rejects equality; individual predictions are over-dispersed and often off. I said so plainly.
- **At the segment-mean level, it holds** — the predicted segment averages are statistically indistinguishable from the actual segment averages (differences not significant).

So the model does *exactly* what it claims and nothing more: it reproduces group averages, not individual values. For the use case — prioritizing *segments* of a prospect population for marketing — that's the right resolution. Stating both results, including the failing one, is what makes the tool trustworthy. A model whose limitations you've mapped precisely is far more useful than one whose limitations you're hiding.

## Why it mattered

The business got a usable, population-wide value estimate that fed audience targeting — plus something more valuable than any single number: **a clear, evidence-backed statement of the ceiling.** "Here's the best segment-level estimate we can defend, here's exactly why individual-level prediction isn't possible with this data, and here's what data we'd need to do better." That honesty is what lets stakeholders make good decisions instead of over-trusting a black box.

## What I'd do differently

The real fix is upstream: the individual-level problem is unsolvable mostly because of the low match rate and biased labels, so I'd invest in better identity matching to grow the labelled set, and I'd be candid that even then, third-party demographics may simply lack the signal for individual value. I'd also frame the segment model from the start as what it is — a calibrated look-up table with a genetic-algorithm-tuned mapping — rather than reaching for individual-level regressors first. Knowing when *not* to use a fancy model is its own skill.

---

*This project shares data lineage with my [customer-persona segmentation](10-customer-personas-clustering-pca.md); the personas were, in a sense, a coarser answer to the same value question.*
