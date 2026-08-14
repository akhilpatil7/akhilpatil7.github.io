---
title: "Finding the Cross-Sell Hiding in Your Own Book"
date: 2026-03-24
tags: [analytics, cross-sell, data-integration, power-query, customer-analytics]
excerpt: "Every insurer knows bundling auto and home policies is valuable. Far fewer can actually see, at the customer level, who's bundled, who's eligible, and where the untapped growth sits. I built the dataset that made that visible — and automated it so it stayed that way."
---

## Everyone believes in bundling. Almost nobody can measure it.

"Bundle your auto and home and save" is one of the oldest ideas in insurance, and for good reason — bundled customers are more profitable and far stickier. So you'd think a carrier would have a crisp, current view of its own bundling: who has both policies, who *could*, and which channels are converting the opportunity.

In practice, that view is hard to produce, because auto and home live in different product systems with different customer keys. Knowing that "Jane Smith" has an auto policy and that "J. Smith" at a slightly different address string has a home policy — and that they're the *same household* — is a data-integration problem before it's an analytics one. Without solving it, "how are we doing on bundling?" gets answered with a shrug and a guess.

I built the foundational dataset that answered it properly, and the analytics on top of it.

## Joining two products into one household view

The core task was linking auto sales to home policies at the **household/party level**. I joined the two product populations on shared party identifiers *and* an address match, then defined a bundle with a deliberate, defensible rule: an auto buyer who also had a home policy in force **within a 45-day window** of the auto purchase. The time window matters — it distinguishes genuine bundling behaviour from an unrelated home policy the household happened to hold years earlier.

Onto that joined spine I layered the signals that turn a match into an insight:

- **Eligibility flags** — which auto customers are actually eligible for a home, condo, or renters product (derived from location and credit criteria), so "opportunity" meant *reachable* opportunity, not fantasy.
- **A credit-quality exhibit** comparing customers' auto-side and home-side insurance credit profiles — because the two products score credit differently, and that gap explains a lot about who bundles.
- **A customer-value proxy** on the bundled book, so we could see not just *how much* bundling was happening but *what quality* of customer it produced.

## What the data revealed

Three findings changed how the business saw its own bundling:

**Bundling was concentrated in one channel.** The overwhelming majority of bundling happened through the human sales center rather than the online channel — the online path was barely converting the opportunity at all. That's a precise, actionable gap: the online experience wasn't surfacing the cross-sell, and the numbers proved it rather than merely suggesting it.

**The product mix was skewed.** Most "bundles" were auto-plus-renters rather than auto-plus-home. That reframed the ceiling: renters bundling is easier but lower-value, so the real growth story was in converting home-eligible auto customers, of whom a meaningful share were sitting unbundled.

**Quality had a wrinkle.** The bundled book's value proxy sat slightly *below* the book average — traceable to the renters skew. Without the customer-value layer, "bundling is up" would have read as unambiguously good; with it, the story got more honest and more useful.

## Automating it so it didn't rot

A one-time analysis of bundling is stale the month after you present it. So I built the refresh as an **automated Power Query pipeline** — the joins, the eligibility logic, and the rollups re-run on fresh data without an analyst rebuilding the workbook. Foundational datasets earn their keep by staying alive; a cross-sell view that's six months out of date is worse than none, because people trust it anyway.

## Why it mattered

The output mapped **growth potential by channel and product** — a concrete picture of how many eligible, unbundled auto customers existed and where the conversion was and wasn't happening. That turned "we should bundle more" into "here is the specific, sized, channel-by-channel opportunity, and here's the online gap that's leaving most of it on the table." It's the kind of work that only becomes possible once you've done the unglamorous integration underneath — and it's a reminder that some of the best growth opportunities aren't new customers at all, they're the ones already in your book that you simply couldn't see.

## What I'd do differently

I'd replace the deterministic address/party match with probabilistic household linkage to catch the fuzzy matches the strict join misses, and I'd extend the value proxy into a proper propensity-to-bundle model — ranking unbundled auto customers by their likelihood to convert — so the sales and marketing teams could work the list in priority order rather than by eligibility alone.

---

*The household-linkage approach here shares its DNA with my [unified lead dataset](06-lead-consumption-entity-resolution.md).*
