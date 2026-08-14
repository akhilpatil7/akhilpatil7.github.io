---
title: "Predicting Churn, Then Reading the Reasons in the Call Notes"
date: 2023-05-20
tags: [machine-learning, churn-prediction, nlp, topic-modeling, lda, gradient-boosting, automl]
excerpt: "Predicting which new customers will cancel is useful. Knowing *why* each one is at risk — mined from unstructured call-center notes — is what makes the prediction actionable. This project did both, and taught me a lot about the difference between a good model and a useful one."
---

## Two questions, not one

When a newly signed customer cancels within their first 90 days, it's expensive — you paid to acquire them and got almost nothing back. So the business wanted to predict, early, which new policies were at high risk of cancelling, in order to intervene.

But a risk score on its own is only half a tool. If you know a customer is likely to cancel but not *why*, your only move is a generic "please stay" outreach, which mostly annoys people. The project that actually moves retention answers two questions together: **who is likely to churn, and what is each at-risk customer's specific problem** — so the outreach can address *their* issue. I built both halves.

## Half one: the churn model

The prediction problem is supervised classification. I assembled a training set from several years of newly issued policies, labelled by whether each survived to day 90, and engineered two feature sets: one from **policy attributes** alone (coverage, prior carrier, discounts, premium structure, how the policy was bought, driver and vehicle details), and a richer one that added signal from **call-center notes**.

The single most important discipline here was **preventing leakage.** A retention dataset is full of fields that secretly encode the answer — cancellation dates, reinstatement flags, survival-day counters. Leave any of them in and the model looks brilliant in testing and is worthless in production, because those fields don't exist yet at prediction time. I aggressively stripped every cancellation-related field, and even blanked call notes containing explicit cancellation keywords, so the model was forced to learn from *legitimate early signals* rather than cheat off the outcome.

I trained the classifier using an **automated machine-learning platform**, which searched model families and selected a gradient-boosted tree ensemble as the best performer, and I operationalized scoring through the platform's batch-prediction API so new policies could be scored automatically.

**On results, I'll be honest about the tradeoff**, because it's the interesting part. The model was **precise — roughly three in four policies it flagged as likely cancellations genuinely did cancel** — but its **recall was modest**: it only caught about a third of all cancellations. For a retention-intervention use case, that's actually a sensible operating point. High precision means you're not wasting expensive outreach (and annoying happy customers) on false alarms; you accept missing some churners in exchange for the ones you do flag being real. If the intervention were cheap and the cost of a miss high, I'd have pushed the threshold the other way. Choosing *where* on that precision–recall curve to sit is a business decision, not a modelling default — and being able to explain that tradeoff is more important than quoting a single accuracy number.

## Half two: reading the call notes with topic modeling

The "why" came from **unstructured call-center notes** — free text logged when customers called in. To turn thousands of messy notes into an actionable reason code, I used **Latent Dirichlet Allocation (LDA)**, a topic model that discovers themes as distributions over words and represents each document as a mixture of those themes.

The NLP pipeline mattered as much as the algorithm: lowercasing, tokenization, stop-word removal, lemmatization, and — importantly — a custom **abbreviation dictionary** to normalize the domain shorthand agents actually type (industry and product abbreviations that no generic cleaner would understand). Garbage tokens in, garbage topics out; the domain-specific cleaning is what made the topics coherent.

I evaluated topic-count choices with coherence and perplexity, but ultimately chose the number of topics for **business interpretability** — four clean, operational themes the retention team could act on: **underwriting issues, e-signature/onboarding friction, a discount/telematics-program concern, and payment problems.** A note was assigned a category only when the model was sufficiently confident (a probability threshold), so ambiguous notes weren't force-labelled.

## Bringing them together

The payoff was in the join. I scored new policies through the churn model, kept the predicted cancellations, and attached each one's **note-derived reason category** — producing a prioritized list that said not just *"this customer is at risk"* but *"this customer is at risk, and it looks like a payment issue"* (or an onboarding issue, or an underwriting one). That routed into **personalized retention outreach**: the payment-risk customers get a billing-focused message, the onboarding-friction customers get help finishing setup, and so on. A generic save-attempt became a targeted one.

I also built a **survival dashboard** tracking day-1-through-90 retention and drop-off, so the team could monitor the underlying cohorts the model was trained to protect.

## Why it mattered

The combination is the point. A churn score tells you *who*; topic modeling on the notes tells you *why*; together they enable outreach that's specific enough to actually work. Either half alone is a fraction as useful. And the project sharpened something I now believe strongly: a "good model" (high some-metric) and a "useful model" are different things. The useful version here was the *precise* one wired to a *reason code* and a *specific intervention* — not the one with the best number on a leaderboard.

## What I'd do differently

I'd push on recall with threshold tuning and class-imbalance techniques, and quantify the actual business value of the intervention (dollars of retained premium per outreach) rather than optimizing an abstract metric. On the NLP side, modern embedding-based topic models would likely produce cleaner, more stable themes than classical LDA — worth testing as a successor now that they're mature.

---

*This paired a classic supervised model with unsupervised NLP. For a purely unsupervised segmentation problem, see [building marketing personas](10-customer-personas-clustering-pca.md).*
