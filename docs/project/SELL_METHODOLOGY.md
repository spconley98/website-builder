---
type: reference
contributors: [sean]
status: active
created: 2026-06-10
updated: 2026-06-10
topic: sell-methodology
tags: [sales, positioning, nate-herk]
related: ["[[ARCHITECTURE]]", "[[MEMORY]]"]
---

# Sell Methodology — turning no-website leads into website sales

> Distilled from the NotebookLM `NATE HERK GUIDE` reports and adapted to *this*
> project's actual job: leadpipe finds local businesses with **no website**; this doc
> is the positioning layer for the **downstream website-build/sell repo** and the
> selling voice baked into the Website Intelligence briefs (Agent 3).
> Reference only — it does not change pipeline logic. See [[ARCHITECTURE]] for the
> pipeline, `agents/website_intelligence.py` for where the ANGLE/CONTENT framing lives.

## The core value story (use this everywhere)
A leadpipe lead is, by definition, a business that **already earns discovery views** on
its Google listing but **owns no website**. Those views convert poorly and leak to
competitors who *do* have a site. The pitch is never "you need a website" — it is:

> "You're already being found. Right now those clicks dead-end or go to a competitor.
> An owned site converts the traffic you already have into direct, credible inquiries."

This reframes a cost ("build me a website") into leverage ("capture demand you're
already paying for in time/attention but not capturing").

## Nate Herk frameworks → our adaptation

### The 3 leverage tests → lead qualification
Nate uses these to qualify automation work; we repurpose them to qualify *which leads
are worth pursuing and what to say*:
- **Smart-Intern test** → would a basic owned web presence obviously help a smart intern
  running this business? If yes, it's a clean pitch.
- **Drudgery audit** → what manual work (answering the same phone questions, re-sending
  hours/pricing, chasing directions) would a site offload? Name it in the pitch.
- **Constraint identification** → "if your inbound doubled tomorrow, what breaks first?"
  surfaces the bottleneck a site solves (booking, trust, after-hours capture).

### AIOS / "mentor not vending machine" framing → consultative sell
Position the offer as installing a durable owned asset, not a one-off deliverable.
The site is the business's own "front door," independent of any single directory/platform.

### Leverage-billed pricing posture (for the future sell repo)
Anchor price to the value of captured inquiries, not hours. A handful of recovered jobs
per month dwarfs a build fee. Keep it simple and outcome-anchored; avoid hourly framing.

### 7 Tier-1 domains → what the future sell repo should encode
When the build/sell repo exists, wire it to the domains that matter for *this* business
type: Customer (reviews/inquiries), Revenue (jobs booked), Comms (lead routing),
Calendar (booking), Knowledge (services/credentials). Revenue + Customer come first —
they are the proof the site is working.

## How this shows up in leadpipe today
- **Website Intelligence briefs**: `_INTELLIGENCE_SYSTEM` instructs the model to make the
  `ANGLE` a concrete ROI/leverage point (convert existing listing views → direct
  inquiries) and `CONTENT` to capture proof/trust material (reviews, credentials, service
  area). The conservative fallback brief carries the same voice.
- **Human review still required**: briefs are draft sales judgment, not cleared outreach
  copy (AGENTS.md §6 Website Brief review). This doc is the rubric a reviewer applies.

## Boundaries
- leadpipe does **not** do outreach, CRM, pricing, or site building — that's the future
  separate repo. This doc seeds that repo's positioning; it does not pull that scope into
  leadpipe.
- Keep claims fact-grounded: never invent business facts in a brief to make the angle
  land harder (fact/judgment separation — see [[past_mistakes]]).
