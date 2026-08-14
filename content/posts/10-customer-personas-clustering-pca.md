---
title: "From Seven Million Households to Five Personas"
date: 2023-07-15
tags: [machine-learning, clustering, kmeans, pca, unsupervised-learning, customer-segmentation]
excerpt: "Turning millions of raw demographic records into a handful of marketing personas sounds like a clustering exercise. The interesting part was what happened when the clustering didn't work — and how principal component analysis rescued it."
---

## The task: make millions of strangers legible

Marketing to a universe of several million prospect households is impossible if you treat every household as unique and equally impossible if you treat them all the same. The useful middle ground is **personas** — a small number of coherent, recognizable customer types you can actually design messaging and offers around.

I was given a third-party demographic dataset covering roughly **seven million individuals** in a single state, with dozens of attributes each: age, income, wealth and spending indices, homeownership likelihood, education, household composition, and more. The goal was to distill that sprawl into a handful of data-driven personas — and then connect those personas to customer value, so marketing could lean into the segments worth the most.

## The honest first attempt — and why it failed

The natural approach is unsupervised clustering: standardize the features and run K-means to find natural groupings. I did exactly that. It didn't work well.

The clusters came out **mixed and overlapping — low separability.** When I profiled them, they weren't crisply different from each other; the algorithm was drawing boundaries through a fog rather than around genuine, distinct groups. This is a common and under-discussed failure mode: K-means will *always* return clusters, but returning clusters and finding real structure are not the same thing. Dozens of mostly-ordinal, partly-correlated demographic features create a high-dimensional space where distances get diluted and everything looks equidistant from everything else — the "curse of dimensionality" in practice.

The mature move here isn't to force a bad clustering into a slide deck. It's to ask *why* the structure isn't separating, and fix that first.

## The fix: reduce dimensions before you cluster

The problem was the geometry of the feature space, so I changed the space. Before clustering, I ran the standardized features through **Principal Component Analysis (PCA)** and clustered on the top few components instead of the raw features.

Why this helps is worth understanding rather than reciting. Many of the demographic attributes are correlated — income, wealth, spending, and homeownership all move together to some degree. PCA finds the underlying axes of *actual* variation (the directions along which households genuinely differ) and discards the redundant, noisy dimensions. Clustering on those condensed axes means K-means is measuring distance along the directions that carry real signal, instead of getting lost across dozens of overlapping, partly-redundant features.

The result was night and day: clustering on the principal components produced **visibly separable groups** — I could plot them in the reduced space and *see* distinct clouds where before there had been mush. The number of clusters was chosen deliberately, using an elbow analysis of within-cluster variance, landing on **five** well-separated personas.

## From clusters to characters

Numbered clusters don't brief a marketing team. So I profiled each one — comparing feature distributions across clusters to understand what actually made each distinct — and translated them into named, recognizable personas spanning the customer lifecycle: from younger, earlier-stage households ("Fledglings") through affluent and established segments up to older, settled ones ("Golden Age"). A persona is only useful when a marketer reads the name and immediately pictures the person; that translation step, from statistics to character, is where a clustering exercise becomes a marketing tool.

## Closing the loop: which personas are worth the most?

A segmentation that ignores value is just tidy demographics. So I linked the personas to a **customer lifetime-value proxy**, computing the average value of each persona. That surfaced a clear ordering — some personas were meaningfully more valuable than others — and let the business select the higher-value segments (which also aligned with the current customer mix) to push into an audience-activation test for targeted acquisition. The segmentation stopped being descriptive and became a *targeting* instrument.

## Why it mattered

The project delivered a compact, interpretable, value-ranked view of a seven-million-person market that marketing could actually act on. But the part I'm proudest of is the middle: recognizing that the first, "correct" clustering was quietly failing, understanding *why* (dimensionality and correlation), and reaching for PCA as the fix rather than shipping mush with confident labels. Unsupervised learning gives you no answer key — no accuracy score tells you the clusters are bad — so the discipline of *interrogating whether the structure is real* is the entire job.

## What I'd do differently

I'd quantify the separability rather than eyeball it — reporting silhouette scores across candidate cluster counts, and stating how much variance the retained principal components actually captured, so the "five personas" choice is defensible with numbers and not just an elbow plot. I'd also test a model that handles mixed categorical/continuous data natively (like Gaussian mixtures or k-prototypes) as a challenger, since one-hot-encoded demographics stretch K-means' Euclidean assumptions.

---

*I later tackled the much harder problem of predicting that value metric directly — see [predicting customer value with almost no labels](12-predicting-customer-value-no-labels.md).*
