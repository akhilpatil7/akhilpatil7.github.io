---
title: "One Customer, Many Footprints: Building a Unified Lead Dataset"
date: 2026-03-10
tags: [data-engineering, entity-resolution, analytics, funnel-analysis, opportunity-sizing, sql]
excerpt: "A prospect might touch a company online, get a call from the sales center, and arrive through a lead broker — and show up as three unrelated rows in three systems. I built the foundational dataset that stitched those footprints into one customer, then used it to quantify exactly how much opportunity was leaking out of the funnel."
---

## The invisible problem: the same person, counted three times

In a direct-to-consumer insurance business, a single shopper leaves footprints in several disconnected systems. They start a quote online. A few days later the sales center calls them back. Maybe they originally arrived through a third-party lead broker. Each of those systems records them independently — different IDs, different schemas, no shared key. To the data, one indecisive human looks like three unrelated events.

That fragmentation quietly breaks everything downstream. You can't measure a true funnel, you double-count, and — most expensively — you can't see the people who fell out of the process and are sitting there as untapped opportunity. Nobody could answer the basic question: *of everyone who entered our funnel, who did we sell, who did we suppress, who is the call center still working, and who did we simply leave on the table?*

I led the foundational work to build the dataset that could answer it.

## Step one: resolve the entity

The heart of the project is **entity resolution** — collapsing many rows across many systems into one record per real person. There's no shared customer key across the online platform, the call-center system, and the lead-broker feed, so I built one from **personally identifying attributes**: name, date of birth, and normalized address (with fallbacks when the primary address was missing). Records that matched on this composite identity were rolled up under a single prospect-level key.

This is the unglamorous, high-leverage part of data work. Get the match logic too loose and you merge two different people; too strict and you fail to link the same person and the fragmentation persists. Tuning that boundary — and handling the messy realities of missing fields, nicknames, and moved addresses — is where the dataset earns its trust.

On top of the identity spine, I unioned and field-mapped the three sources into one schema, carrying forward the full timeline: first quote, rating events, sale, call-center dispositions, and broker metadata.

## Step two: give every lead a status

A unified record is only useful if it answers "what happened to this person?" So I built a **categorization layer** that assigned every prospect to exactly one bucket through a priority waterfall:

1. **Sold** — matched to a policy or a positive sale disposition (further split by which channel and carrier closed it).
2. **Suppression** — legitimately out of play (already a customer, ineligible, declined, or on a do-not-contact list).
3. **Call center actively working** — an open task or a "still in progress" disposition (waiting on documents, scheduled call-back, still shopping).
4. **Opportunity / retargeting** — everyone left: people who entered the funnel, weren't sold, weren't suppressed, and weren't being worked. *These are the leads worth money that nobody was chasing.*

The waterfall order matters — a lead can look like several things at once, and resolving that ambiguity consistently is what makes the categories trustworthy.

## Step three: put a number on the leak

With every lead classified, I could finally quantify the funnel's leaks. I mapped the **knockout points** — the specific places prospects drop out (abandoning before seeing a premium, being declined by underwriting rules at each rating stage, abandoning after a re-rate, not being called back by the contact center) — and sized the opportunity at each one.

Then I built a **priority matrix**, scoring each leak on *opportunity size* against *effort to address*, so the business could triage. Instead of a vague "we lose a lot of leads," the output was a ranked, quantified list: *here are the biggest pools of recoverable prospects, here's roughly how many are in each, and here's which ones are cheap to go after.* That reframed the conversation from anecdote to a prioritized action list — and directly seeded a downstream lead-monetization effort for the prospects who couldn't be sold a policy but still had value.

## Why this was foundational, not just analytical

The word I keep coming back to is *foundational*. This dataset wasn't the end — it was the ground floor. Once it existed, a dozen other analyses became possible almost for free: true funnel conversion, channel attribution, contact-center performance, and the opportunity sizing above. A later iteration extended it to track lead-broker leakage and prioritization, and to test hypotheses about which lead characteristics predicted conversion.

That's the quiet lesson of data work: the highest-leverage thing you can build is often not a model or a dashboard, but the **clean, unified dataset that makes every future model and dashboard trustworthy.** Entity resolution isn't flashy, but it's the difference between analytics built on one customer and analytics built on three ghosts of the same one.

## What I'd do differently

I'd formalize the identity-matching with a probabilistic record-linkage approach (scoring match confidence rather than applying deterministic rules), which handles the fuzzy edges — typos, nicknames, stale addresses — more gracefully and gives every merge a confidence score you can audit. And I'd move the whole pipeline from periodic rebuilds toward an incremental, monitored refresh so the "foundational dataset" stays fresh without a manual lift.

---

*This dataset underpinned much of my direct-channel analytics work, including the cross-sell foundation in the [Auto–Home bundle project](07-auto-home-bundle-cross-sell.md).*
