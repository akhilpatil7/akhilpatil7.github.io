---
title: "Cutting a Seven-Figure Vendor Bill — and Debugging the Fallout"
date: 2026-02-20
tags: [analytics, cost-reduction, telephony, root-cause-analysis, dashboards, data-quality]
excerpt: "A vendor was quietly earning a seven-figure annual fee to route inbound calls to the right agents. The company decided to bring it in-house. I supported the migration analytics — and when the internal call volumes came back looking alarmingly low, I found out why before anyone panicked."
---

## The setup: paying a middleman to answer the phone

For a business that sells over the phone, inbound-call routing is critical plumbing. When a prospect calls a number from an ad, something has to decide *which* agent — with which skills, for which campaign — should pick up. A third-party vendor was providing that routing layer, and charging a **seven-figure annual fee** for the privilege.

The company decided it could do this itself. Modern telephony supports internal routing through call-distribution nodes (in the jargon, VDNs) mapped to skills and campaigns — so instead of one vendor number funnelling everything, the business could publish its own campaign numbers and route calls internally. Cut out the middleman, keep the capability, save the fee. I supported the analytics behind the migration.

## Migration analytics: mapping the old world to the new

The messy reality of a cutover like this is the mapping. Every one of the vendor's reserved phone numbers had to be traced to its internal replacement number, then to the routing node, then to the campaign it served — so that when traffic moved, we could prove it landed where it should. I built and maintained that mapping and the reporting around it, cross-checking, campaign by campaign, that call volume was migrating from the vendor's numbers to the internal ones as each was decoupled.

That cross-check is what makes a migration safe. It's easy to flip a switch; it's hard to *prove* nothing fell through the cracks. The number-by-number reconciliation was the proof.

## The scare: "our volumes dropped"

Then the alarming part. After the switch, the internally captured call volume looked materially lower than before. On its face, that's a five-alarm fire — did we just break our own phone system and start losing calls (and sales) the day we fired the vendor?

This is the moment where an analyst either adds value or adds panic. I dug into the root cause instead of accepting the headline, and found that the drop was **a measurement artifact, not a real loss of calls:**

1. **Internal capture started late.** Our internal system only began recording certain call metrics from a specific go-live date. Any comparison that reached back before that date was comparing "fully captured" to "not yet captured" — a guaranteed apparent decline that had nothing to do with actual call volume.
2. **We were only capturing selective routing nodes.** The internal data was recording a subset of the inbound routing nodes, not all of them. So even after go-live, the internal numbers *undercounted* by construction — the calls were arriving and being handled; they just weren't all being logged in the new pipeline yet.

In other words, the calls were fine. The *instrumentation* was incomplete. That distinction was the entire story — and getting it wrong would have meant either reversing a good cost decision or chasing a problem that didn't exist.

## Building the instrument properly

The fix was to make the measurement trustworthy. I built a **Call Metrics Dashboard** that joined the internal call-node data to the campaign definitions and tracked call-center campaign performance and volumes on the new internal routing — with the known capture-start date and the covered-node caveats built directly into the logic, so the numbers couldn't lie by omission. Once the instrument counted what was actually happening, the "drop" resolved and the true picture — that the insourcing had preserved call handling while eliminating the vendor fee — became visible and defensible.

## Why it mattered

Two kinds of value came out of this. The obvious one: the migration eliminated a **seven-figure recurring vendor cost** while keeping the routing capability in-house. The subtler, and arguably more important, one: when the data got scary, the response was *diagnosis*, not reaction. A worse-handled version of this project ends with leadership doubting the whole cost-saving move because "the volumes tanked." Instead, the finding was precise — the calls were never lost, the meter just wasn't fully wired up yet — and the fix was to complete the instrumentation.

That's a lesson I carry into every project: **a surprising number is a question, not an answer.** Before you act on a scary metric, make sure the metric is actually measuring what you think it is. Half the "crises" in analytics are really data-capture gaps wearing a costume.

## What I'd do differently

I'd insist on the measurement pipeline being complete and validated *before* the cutover, not built out in parallel with it — running the internal capture alongside the vendor for an overlap period so there's a clean apples-to-apples baseline from day one. The migration was the right call; the only real problem was that the meter went in slightly after the switch, and that's exactly the kind of gap that turns a win into a fire drill.

---
