---
title: "An Early-Warning System for Marketing KPIs (Without Crying Wolf)"
date: 2026-01-30
tags: [statistics, statistical-process-control, control-limits, anomaly-detection, dashboards, alerting]
excerpt: "The hardest part of an alerting system isn't detecting change — it's detecting the change that matters without drowning everyone in false alarms. Here's how I built control limits for daily marketing KPIs that respected how the data actually behaves."
---

## The goal: notice trouble on day one, not at the month-end review

Marketing performance can deteriorate quietly. Cost-per-sale drifts up, a conversion rate sags, and by the time it surfaces in a monthly review, weeks of spend have already gone sideways. The business wanted an **early-warning system**: automated alerts that fire when a core KPI — cost-per-sale, close rate, quote-completion rate — moves outside its normal range for a given state, so someone can look *today* rather than at the next steering meeting.

The naïve version of this is easy and useless: pick a fixed threshold, alert when it's crossed. It fails immediately, because "normal" isn't a fixed number — it varies by state, by metric, and it's noisy day to day. Set the threshold too tight and you cry wolf until everyone mutes the alerts; too loose and you miss the real problems. The entire craft is in defining "abnormal" correctly.

## Borrowing from the factory floor: control limits

I framed the problem as **statistical process control (SPC)** — the same discipline manufacturing uses to tell a machine that's genuinely drifting from one that's just wobbling within its normal tolerance. The core object is a **control limit**: an upper and lower bound on a metric, beyond which a reading is flagged as a signal rather than noise.

The subtlety — and where most naïve implementations go wrong — is *how* you set those limits. The textbook approach (mean ± a few standard deviations) assumes the data is roughly bell-shaped. But **daily marketing KPIs are not normally distributed.** Daily cost-per-sale is skewed, spiky, and bounded — a low-volume day can produce an extreme value that a normal-based limit would either over-flag or fail to bracket. Applying the textbook formula to that data would generate exactly the false-alarm storm that gets alerting systems switched off.

## Matching the method to the distribution

So I used **two different methods depending on how the data actually behaved:**

**Daily view — empirical percentile limits.** For raw daily metrics, which are non-normal, I set the limits empirically from the observed distribution — using high and low percentiles rather than assuming a bell curve. Crucially, I *tuned* those percentiles against the number of breaches actually observed over the prior two quarters, so the alert rate was calibrated to a sensible volume. This is the key idea: I didn't pick limits from a formula and hope; I picked them to produce an alert cadence the team could actually act on, then checked them against history.

**Rolling 7-day view — the Empirical Rule.** A 7-day rolling average smooths out the daily spikiness and, by the logic of averaging, behaves much more like a normal distribution. So for that view, the classical approach *is* appropriate — I set limits at mean ± 2 standard deviations (the ~95% Empirical Rule band). Same philosophy (bracket the normal range), correct tool for a distribution that had become approximately normal.

Using the *right* method for each view is the whole point. A single one-size-fits-all rule would have been wrong for at least one of them.

## Keeping it honest over time

Two operational touches made it durable:

- **State-specific limits.** Each state has its own cost structure and behaviour, so every state got its own bounds rather than a shared, wrong-for-everyone threshold. In some cases the logic was tightened to trigger on genuinely impossible readings (for instance, a zero where zero should never occur).
- **A monthly refresh discipline.** "Normal" drifts as the business changes, so I re-estimated the thresholds every quarter/month rather than letting stale limits slowly turn into noise. An early-warning system that isn't maintained becomes an early-warning system everyone ignores.

The alerts themselves were delivered automatically off a monitoring dashboard, so the whole thing ran without a human watching a screen — it watched the screen and tapped someone on the shoulder only when a metric genuinely stepped out of line.

## Why it mattered

The deliverable turned KPI monitoring from a *reactive*, look-back-monthly ritual into a *proactive*, same-day signal — and did it without the false-alarm fatigue that kills most alerting systems. The reason it worked is unglamorous but fundamental: I let the shape of the data dictate the statistics, calibrated the sensitivity against real history, and committed to maintaining it. Detecting anomalies is easy; detecting the *right* anomalies, at a volume people will actually respond to, is the real problem — and that's a statistics problem, not a dashboard problem.

## What I'd do differently

Percentile-and-refresh limits are robust but static within a period. I'd move toward methods that model the time-series structure directly — seasonality and day-of-week effects — so the bands flex with predictable weekly patterns instead of treating every day as a draw from one distribution. Adding a "consecutive breaches" or trend rule (à la the classic SPC run rules) would also catch slow drifts that never trip a single-day limit but matter just as much as a sudden spike.

---
