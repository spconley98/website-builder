> ⚠️ **NOTE:** This document is **NOT** the official scaffold/structure of this project.
> It's a reference library — a catalog of every AI skill Sean has gathered (global, project-local,
> plugin) plus recommended skills from Anthropic docs, Andrej Karpathy's principles, and the Jack
> Roberts AI guides. Treat it as a lookup menu of options, NOT a commitment to use any of them.
> Just because a skill is listed here does not mean it's part of the actual build.

---

# Master Skills Catalog

**Maintainer:** Sean · **Last updated:** 2026-06-07
**Purpose:** One place where Sean *and* Matt can see every skill available, understand in plain
English what it does, why it matters, how to use it in a project, and — where the skill is just a
copy-paste from a public repo — exactly where to get it and how to install it.

---

## How AI "skills" work (plain-English primer)

A **skill** is just a folder containing a `SKILL.md` file (instructions written in markdown). When the
skill's trigger words come up, the agent (Claude Code, etc.) loads that file and follows it. Some skills
add extra files (`references/`, scripts). That's it — no magic. Three places a skill can live:

| Scope | Folder | Who sees it |
|---|---|---|
| **Global** | `C:\Users\<you>\.claude\skills\<name>\SKILL.md` | every project on your machine |
| **Project-local** | `<project>\.claude\skills\<name>\SKILL.md` | only that project (travels in the git repo) |
| **Plugin** | installed via a plugin marketplace | every project, namespaced like `vercel:deploy` |

### The 3 ways to install a skill

1. **Copy-paste from a public repo** (most community skills):
   ```powershell
   # clone the repo, then copy the one skill folder you want into your project
   git clone https://github.com/<owner>/<repo>.git temp-skills
   Copy-Item -Recurse "temp-skills\skills\<skill-name>" "C:\Users\mysis\website-builder\.claude\skills\"
   Remove-Item -Recurse -Force temp-skills
   ```
   Or even simpler — open the repo's `SKILL.md` on GitHub, copy the raw text, and paste it into a new
   file at `.claude\skills\<name>\SKILL.md`. **Tell the agent:** *"Create a new skill at
   `.claude/skills/<name>/SKILL.md` with this content: <paste>"*.

2. **Plugin marketplace** (official, managed): inside Claude Code run `/plugin`, browse the marketplace,
   install. Used for `caveman`, `vercel`, `frontend-design`.

3. **NotebookLM CLI skill installer** (for the genmedia/fal family): `py -m notebooklm skill ...`.

> **For Matt:** to get Sean's project-local skills, just `git pull` — anything under
> `.claude/skills/` in the repo comes with it. Global skills are per-machine; Matt installs those
> himself using the links in this doc.

---

# SECTION A — Sean's Global Skills (installed at `~/.claude/skills/`)

These are already live on Sean's machine for every project. Matt can replicate any of them with the
source links noted. Grouped by family to keep it readable.

## A1. The genmedia / fal.ai family (media generation)
**Source repo:** https://github.com/fal-ai-community/skills (install via `py -m notebooklm skill` or copy-paste the folder)

These all run on the **genmedia CLI**, a wrapper around 1200+ fal.ai model endpoints (image, video, audio, 3D).

| Skill | Plain English: what it does | Why it matters | Use it when… |
|---|---|---|---|
| **genmedia** | The foundation — search, run, and manage any of 1200+ AI media models from the command line | Every other fal skill runs through this; one tool instead of a dozen websites | You want to generate/edit images, video, audio programmatically |
| **fal-models-catalog** | A "which model should I use for X?" lookup | Stops you guessing; routes you to the best endpoint | You don't know which model fits the task |
| **fal-prompting** | Model-specific prompt-writing tips (Kling, GPT-Image, etc.) | Generic prompts give generic results; this tunes per model | Your outputs keep coming back bland |
| **fal-recipes** | Pre-built multi-step pipelines (make a commercial, restore a photo, lip-sync, etc.) | Skips the trial-and-error of chaining models | You want a finished result, not one API call |
| **fal-redesign** | Screenshots a website, has a vision model redesign it, outputs a build-spec | Turns "make it look better" into a concrete plan | Upgrading a bland site to award-tier design |
| **fal-regenerate-3d** | Builds an interactive 3D character-selector experience | Niche but powerful for hero sections | Building a 3D showpiece |
| **fal-gamedev** | 2D pixel-art game assets, sprite sheets, walk cycles | Game art without an artist | Making game sprites/backgrounds |
| **fal-workflow** | Author/run declarative multi-step media workflow JSON files | Repeatable, version-controlled media pipelines | Batch/production media jobs |
| **genmedia-workflow** | Same idea, planning→generation→delivery manifests | End-to-end deliverables | Multi-asset campaigns |
| **character-design** | Consistent characters across images/video (reference sheets, expressions) | Keeps a character looking the same shot-to-shot | Brand mascot, recurring character |
| **cinematography** | Cinematic shot/lighting/lens/camera-move prompts | Production-grade visual direction | Film-look images/video |
| **commercial** | Product photography, ads, e-commerce batches | Brand-safe product shots at scale | Product/ad imagery |
| **marketing** | Campaign-level asset matrices (paid social variants, banners) | A whole launch kit at once | Multi-channel campaign |
| **storytelling** | Multi-shot narrative video (storyboards, shot lists) | Sequence continuity for brand films | Narrative/social stories |
| **ugc** | Creator-style talking-head/testimonial/unboxing ads | Authentic-looking social ads | UGC ad content |
| **fan-cam** | Personalized sports broadcast fan-cam videos | Very niche novelty content | Sports fan reaction clips |
| **image-generator** | 3 coordinated prompts for scroll-stop product video (clean → exploded → transition) | Feeds scroll-driven hero animations | Apple-style product reveal |
| **model-routing** | Default endpoint IDs for the production skills above | Consistency across the media skills | Used automatically by the others |

## A2. Design / front-end skills

| Skill | What it does | Why | Use when |
|---|---|---|---|
| **impeccable** | Full UI/UX design + critique engine (hierarchy, a11y, motion, copy, tokens) | Turns "make it nicer" into specific, expert fixes | Designing or auditing any interface |
| **ui-ux-pro-max** | Design intelligence library: 50 styles, 21 palettes, 50 font pairings, 20 chart types, 9 stacks | Instant design-system decisions | Picking a look/feel, fonts, palette |
| **spline-3d-integration** | How to embed interactive Spline 3D scenes into React/Next | Real 3D without a 3D engineer | Adding a 3D hero/section |
| **3d-animation-creator** | Builds scroll-driven video websites (video scrubs as you scroll) | The mesmerizing Apple scroll effect, done for you | Scroll-stop landing pages |

## A3. Workflow / process skills

| Skill | What it does | Why | Use when |
|---|---|---|---|
| **grill-me** | Interviews you relentlessly about a plan until every branch is resolved | Stress-tests an idea before you build the wrong thing | Pinning down a fuzzy plan |
| **context-transfer** | Session wrap-up: health-check, MEMORY.md update, NotebookLM upload, commit (the one we customized for this project) | Clean handoffs so the next agent/teammate has full context | End of a work session |
| **website-intelligence** | Scrapes a client site + 5 competitors, writes a competitive report, then builds an informed site | Market-grounded builds instead of guesswork | New client website from scratch |
| **seo-strategy** | SEO planning skill | Search visibility baked in | Planning content/metadata |

## A4. AAS-WEBSITE brand skills (project-specific, but installed globally)
*These only matter for the Aerial Ag Solutions site — listed for completeness.*
- **aas-design** — locked AAS brand tokens & rules
- **aas-section-builder** — AAS section/component patterns (Next.js 16)
- **aas-seo-content** — AAS copy/content voice

---

# SECTION B — Project-Local Skills (and the dedupe)

Scanned every project folder under `C:\Users\mysis\`. Result: **almost every project-local skill is a
copy of a global skill** (AAS-WEBSITE's 21, VR-REDESIGN's `grill-me`, the `context-transfer` copies in
qal-study / blend-doctor / website-builder). To avoid duplication, those are **not re-listed** here —
see Section A.

**The only skills that exist locally but are NOT in the global set:**

| Skill | Found in | What it does | Why | Get it |
|---|---|---|---|---|
| **supabase** | `blend-doctor/.claude/skills/` | Guidance for working with Supabase (Postgres DB, auth, edge functions) from the agent | Backend-as-a-service without wiring it all by hand | https://github.com/supabase/agent-skills · `npx skills add supabase/agent-skills` |
| **supabase-postgres-best-practices** | `blend-doctor/.claude/skills/` | Postgres schema/query best-practice checklist | Avoids slow queries & bad schema decisions | Same Supabase agent-skills repo above |

> If website-builder ends up using Supabase (VR-REDESIGN already does), copy these two from
> `blend-doctor` rather than re-finding them:
> ```powershell
> Copy-Item -Recurse "C:\Users\mysis\blend-doctor\.claude\skills\supabase" "C:\Users\mysis\website-builder\.claude\skills\"
> Copy-Item -Recurse "C:\Users\mysis\blend-doctor\.claude\skills\supabase-postgres-best-practices" "C:\Users\mysis\website-builder\.claude\skills\"
> ```

---

# SECTION C — Installed Plugins (bundled skills)

Installed via the Claude Code plugin marketplace (`/plugin`). Each plugin ships several skills.

| Plugin | Skills it provides | What / why |
|---|---|---|
| **caveman** | caveman, caveman-commit, caveman-review, caveman-help, compress | Ultra-compressed "caveman" output to cut token usage ~75% while keeping technical accuracy |
| **vercel** | vercel:deploy, vercel:env, vercel:bootstrap, vercel:nextjs, vercel:ai-sdk, …(many) | Expert guidance + actions for deploying/managing on Vercel |
| **frontend-design** | frontend-design | Generates distinctive, non-generic production-grade UI |

Install a plugin: open Claude Code → `/plugin` → browse marketplace → install. Official directory:
https://github.com/anthropics/claude-plugins-official

---

# SECTION D — Recommended Skills From Official Documentation

Public, free, copy-paste-able. These are the highest-signal sources to pull *new* skills from.

### D1. Anthropic Official Skills
**Repo:** https://github.com/anthropics/skills
The official library — creative (art, music, design), technical (testing web apps, MCP server
generation), and enterprise workflow skills. Each is a self-contained `SKILL.md` folder.
```powershell
git clone https://github.com/anthropics/skills.git temp-anthropic-skills
# browse temp-anthropic-skills\skills\ , copy the ones you want:
Copy-Item -Recurse "temp-anthropic-skills\skills\<skill-name>" "C:\Users\mysis\website-builder\.claude\skills\"
Remove-Item -Recurse -Force temp-anthropic-skills
```

### D2. VoltAgent — awesome-agent-skills (⭐23.6k)
**Repo:** https://github.com/VoltAgent/awesome-agent-skills
1000+ **real** skills from actual engineering teams — Anthropic, Google Labs, Vercel, Stripe,
Cloudflare, Netlify, Trail of Bits, Sentry, Figma, Hugging Face — plus community. Compatible with
Claude Code, Codex, Gemini CLI, Cursor, Copilot, Windsurf. **Best single place to shop for skills.**

### D3. VoltAgent — awesome-openclaw-skills
**Repo:** https://github.com/VoltAgent/awesome-openclaw-skills
5,400+ skills filtered/categorized from the OpenClaw Skills Registry. Huge breadth; lower curation
than D2 — search, don't browse.

### D4. Claude Code Router (use cheaper / local models)
**Repo:** https://github.com/musistudio/claude-code-router
Not a skill — a **proxy** that sits between Claude Code and the model, letting you route requests to
DeepSeek, Gemini, OpenRouter, **Ollama (local)**, etc. Switch models live with `/model`. This is the
practical tool behind Jack Roberts' "80/20" routing idea (Section F).
```powershell
npm install -g @musistudio/claude-code-router
# then configure ~/.claude-code-router/config.json with your providers
```

---

# SECTION E — Karpathy-Recommended Principles & Skills

Andrej Karpathy (OpenAI co-founder, ex-Tesla AI). His mental models about LLM limitations are the
foundation many of the skills below are built on. *(Sourced from Sean's Jack Roberts notebooks.)*

### The Karpathy Principles (operating rules to make AI deterministic)
Paste these into a `claude.md` / `gemini.md` so the agent obeys them on every task:
- **Data First** — structure the data before writing logic.
- **Surgical Changes** — only touch the exact files/code you were asked to change.
- **Simplicity First** — minimal logic, no speculative abstractions.
- **Goal-Driven** — every change measured against the project's "North Star."
- **Per-Task Rhythm** — strict *explore → plan → code → commit*, no skipping steps.

> Copy-paste block to drop into your project constitution:
> ```
> OPERATING PRINCIPLES (Karpathy):
> 1. Data first — define data structures before logic.
> 2. Surgical changes — modify only what was explicitly requested.
> 3. Simplicity first — minimal logic, no speculative abstractions.
> 4. Goal-driven — measure every change against the North Star objective.
> 5. Per-task rhythm — explore, plan, code, commit. Never skip a step.
> ```

### "Graphify" (codebase knowledge graph)
**What:** Instead of making the agent read a codebase file-by-file (which bloats context and costs a
fortune), Graphify vectorizes the whole codebase into a queryable graph — every file is a "station,"
every import a "subway line." The agent "rides the lines" straight to what it needs.
**Why:** Claimed ~70× cheaper for codebase Q&A; bypasses context rot on big projects.
**Inspired by** Karpathy's tweet on how he builds knowledge bases.
**Get it:** distributed through the Jack Roberts paid community (no public repo confirmed). For a
public equivalent, see RAG/graph tools in Section D2 or use a vector DB (Pinecone) directly.

### "Super Skills" (self-improving, infinite-memory skills)
**What:** Skills that give an agent persistent memory so it "wakes up smarter each session," can score
its own output, and iteratively self-improve — instead of static files that forget everything.
**Why:** Static skills don't evolve with your business; Super Skills do.
**Get it:** Jack Roberts community (paid). Public analog: the "self-generating skills" pattern + a
memory MCP (Sean already runs one at `~/.claude/memory-mcp/`).

### Vibe Coding
Karpathy's framing that building software by stating intent in natural language is the future — for
beginners *and* top-tier engineers. Not a skill; a mindset that underpins this whole catalog.

---

# SECTION F — Jack Roberts-Recommended Skills & Frameworks

From the "Jack Roberts AI Guide" / "JACK AI UPDATED" notebooks. These are frameworks and workflows,
mostly distributed as copy-paste system prompts or through his community.

### Orchestration & context frameworks
| Name | Plain English | Why it matters |
|---|---|---|
| **GSD (Get Sh*t Done)** | Takes a vague idea → strict PRD → spins up a **fresh sub-agent with a clean context window for every atomic task** | Completely bypasses context rot; no single agent gets overloaded |
| **BLAST** | Master system prompt to build apps in 5 stages: Blueprint, Links (MCP), Architect, Stylize, Trigger | Deterministic app builds |
| **SITE / PAGES** | High-converting page workflow: Purpose, Interface, Text, Engine, Ship | Marketing-site quality |
| **The Ralph Loop** | Autonomous bash loop: reads a PRD, keeps spawning agent sessions for unfinished tasks until verified | Hands-off completion |
| **Agent Teams (Mission Control)** | Specialized sub-agents (UX researcher, architect…) reporting to a lead | Parallel, specialized work |
| **3-Tier Memory** | Core (permanent rules) + Conversational buffer (last ~50 msgs) + Semantic (Pinecone/NotebookLM) | Structured, durable memory |

### Context-management techniques (the "context rot" defense)
*Context rot = the LLM degrading as its window fills (effectiveness nose-dives past ~100–120k of a 200k window).*
- **Summary Swap** — before `/clear` or every 30–45 min, have the AI summarize progress/next-steps, paste that into a fresh window → token count resets, instructions stay sharp.
- **One Task Per Message** — break work into the smallest atomic pieces.
- **MCP Pruning** — every loaded MCP server eats context even when idle; keep <50 active, lazy-load, ruthlessly deactivate unused tools.
- **System-Prompt Truncation** — keep `claude.md` dense and short ("Queen's English"); it's re-read on every message.
- **Keep files < 500 lines** — smaller files = fewer tokens to read on each edit.
- **RAG over paste** — use a vector DB (Pinecone) or Graphify instead of pasting whole docs/codebases.

### Local-model / cost strategy
- **80/20 Routing** — delegate ~80% of routine coding to **free local models** (e.g. Google Gemma via Ollama) for privacy + cost; reserve the hard 20% for premium (Claude Opus). Implement with **Claude Code Router** (Section D4).
- **Hardware note** — heavy local models can melt a laptop; Roberts recommends a dedicated **Mac Mini** as an always-on 24/7 "gateway," or a ~$5/mo cloud VPS. Quantization (QLoRA 4-bit, GGUF for CPU-only) lets 7B models run on consumer hardware.

### Business / agency workflows
- **MONEY Framework** — Map niches, Obtain leads, Nail builds, Execute value, Yield recurring revenue.
- **CEO System (Daily Brief)** — 24/7 command center scraping industry data into a daily executive summary.
- **Content Factory** — scrape YouTube transcripts → auto-draft LinkedIn/X posts.
- **SEO Infrastructure skill** — auto-inject routing, metadata, sitemaps, robots.txt.

> **Where to get the Jack Roberts frameworks:** most are distributed as copy-paste documents inside
> his paid community (no public GitHub). The *techniques* above, however, are free to apply directly —
> just paste the relevant rules into your `claude.md`. Sean's existing reference docs
> (`(Raw Text) AI_BUILD_BIBLE.md`, `(Raw Text) Comprehensive_*`) contain the fuller write-ups.

---

## Sources
- [anthropics/skills](https://github.com/anthropics/skills)
- [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)
- [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)
- [VoltAgent/awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills)
- [musistudio/claude-code-router](https://github.com/musistudio/claude-code-router)
- [fal-ai-community/skills](https://github.com/fal-ai-community/skills)
- [supabase/agent-skills](https://github.com/supabase/agent-skills)
- Karpathy principles, Graphify, Super Skills, GSD/BLAST, context-rot techniques, 80/20 routing — Sean's Jack Roberts NotebookLM notebooks (`karpathy_query.txt`, `context_query.txt`, `gpu_query.txt`, `obsidian_query.txt`, `gatekeeper_query.txt`)
