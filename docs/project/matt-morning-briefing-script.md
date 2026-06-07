# Matt Morning Briefing — Monologue Script

> Single male host, first-person as an AI rendition of Sean, speaking to Matt. Paste into ChatGPT (or
> any TTS) to generate the audio. Keep the opening and closing lines verbatim.

---

Hi Matt, this is Sean. Well... an AI rendition of Sean's instruction, but I'm going to speak as if I am him. Chances are I'm currently asleep — I had a little too much to drink last night, I fell asleep, woke up hungover this morning, started working on this, and I thought I'd fill you in.

So pour yourself a coffee and just listen. You don't need to take notes — everything I mention is written down and waiting for you. I just want you to hear the story of it, so when you open this thing up it actually makes sense instead of looking like a pile of folders some maniac made at 4 a.m.

Here's what I'm going to walk you through, start to finish:

- One — the **vision**. What we're building, and why it's actually a smart little money machine.
- Two — **everything I set up** last night, step by step, so you know what all these files are.
- Three — **your next steps**, which are just setup on your end. Nothing to build yet.
- And four — the **resources** I made so you can follow along and get inspired — the NotebookLM brain and the Obsidian vault, and the mind maps and visuals inside them.
- Then I'll close with a little honest reflection on what's still missing, so future-us doesn't trip over the same gaps.

Alright. Let's get into it.

## The vision

Here's the whole idea in plain English. There are local businesses everywhere — plumbers, roofers, taco trucks, landscapers, nail salons — that make real money but have **no website**. They're basically invisible online, or they're living entirely on a Facebook page. That's our opening.

We're building a **pipeline** — think of it like a little assembly line of AI workers, where each worker does one job and hands its work to the next one. We feed the line a place and an industry, like "restaurants in Austin, Texas," and it goes to work.

The first worker is the **Lead Finder**. Its whole job is to go out, find every business matching what we asked for, and figure out which ones don't have a website. That last part is the gold — a business with no website is a business we can sell one to. It writes each one down: name, industry, location.

The second worker is the **Lead Prioritizer**. It takes that list and digs deeper. For each business, it goes looking for how much of their work is already photographed online — their Yelp page, their Google listing — because here's the insight: if a plumber already has fifty photos of beautiful finished bathrooms on Yelp, we can build them a gorgeous website *fast*, because the content already exists. We just collect it and drop it in. So the Prioritizer gives every business a **one-to-five rating** based on how much photo material is out there, and it saves the clickable links — straight to the Yelp and Google pages — so you or I can just click, look, and save the images. Higher rating means easier money.

And the engine that does all this thinking? **Local AI.** I've got an RTX 3090, and we'll run the models right on my machine through a tool called Ollama. That means the grunt work — reading, summarizing, rating — costs us basically nothing and stays totally private. No per-month AI bills eating our profit.

The endgame: the pipeline hands us a ranked list of easy, photo-rich businesses with no website. We build them a clean site — and we already know how to do that part, we've both built sites before — and we sell it to them. Rinse, repeat. We've got plans for more workers down the line, like one that drafts outreach, but those two are the start.

One important thing I want you to hold onto: **this project is just the lead pipeline.** The actual website-building — the templates we clone, the branding, all that — that's going to be a *separate* project later. This repo does one job and does it well: find and rank the leads. Don't let the name "website-builder" fool you into thinking we're building websites in here yet.

## What I worked on last night

Okay, here's the part where I tell you what all these files actually are, because you're going to open the repo and see a lot, and I don't want you overwhelmed.

First, I made the **GitHub repo** and added you as a collaborator with full write access. So you'll have an invite waiting — accept it, and we're working out of the same place.

Then I set up something I'm pretty proud of: a **constitution** for the project. Here's the problem it solves. We're not just using one AI — we're going to use Claude, and Codex, and Gemini, depending on the task. If each of those reads a different rulebook, we get chaos. So I made one master file called `AGENTS.md` that *every* AI reads first, no matter which one it is. It's the single front door. There are two little pointer files, `CLAUDE.md` and `GEMINI.md`, but all they do is say "go read `AGENTS.md`." One source of truth, so nothing drifts out of sync. That file holds who we are, the rules, the conventions, all of it.

Next, I built a **reference library**. Over my whole journey messing with AI building, I've collected these big documents — an "AI Build Bible," guides on tools, frameworks, skills, MCP servers, all of it. I copied the good ones in and organized them. But — and this is important — I slapped a big disclaimer on every single one: **this is reference material, not the plan.** Just because a tool is listed in there does *not* mean we're using it. It's a menu of ideas to pull from, nothing more. I don't want you seeing "LangGraph" in a doc and thinking we committed to it. We didn't. It's inspiration.

Now here's a fun part. For that reference library, I didn't just dump text. For each document, I had NotebookLM generate two extra things: a **mind map**, which breaks the doc into a visual tree of bullet points, and a **visualization**, which is a polished infographic poster of the whole thing. So every reference doc exists in three flavors — the raw text, the mind map, and the infographic. I even built a custom **skill** — basically a saved instruction set for the AI — called `reference-visualizer` that automates this. When a new doc gets added to the library, it offers to make the mind map and visual automatically. But I built in a rule: it always **asks first** before doing it. And if you're ever unsure and say "not sure, ask Sean," it logs your request to a pending-approvals list and waits for me to approve it. So you're never blocked, and I'm never surprised. There's another skill too, called `context-transfer`, that wraps up each work session cleanly — it updates our notes, and importantly it tags **who did what**, so we always know whether you or I worked on something.

I also wrote a **Master Skills Catalog** — a big organized list of every AI skill I've got, plus a bunch of recommended ones from Anthropic, from community collections, and from the people I follow like Karpathy and Jack Roberts. For each one, plain English: what it does, why it matters, and where to download it with copy-paste instructions. So if we ever need a new capability, that catalog is our shopping list.

On the tooling side, I wired in **Firecrawl**, which is a web-scraping service our agents can use to read web pages. Fair warning — the account's out of credits at the moment, so it authenticates but won't actually scrape until we top it up. And I set everything up so our secret API keys never, ever get committed to the shared repo — they stay local on each of our machines. I'll come back to that in your steps.

I also went down a little research rabbit hole. I found this thing called Firecrawl's "Open Agent Builder" — a drag-and-drop visual tool for building AI workflows — and I genuinely wondered if we should use it instead of building our own thing. I dug into it and concluded: no. It's built for scraping-and-extraction pipelines, not for the kind of agent setup we're doing. What we actually needed wasn't a fancy visual builder — it was that constitution, the front door, so any agent walking in knows the rules. So that's what I built instead.

And the big one: last night I sat down and did a **deep planning session** on the actual architecture — how the pipeline should be built. I used a skill called "grill-me" that interrogates every decision one at a time until there's no ambiguity left. We went through it all: we're building in **Python**, because that's the language local AI and agents live in. The pipeline is **lightweight** — each agent is a simple, independent module, and they hand work to each other through files, which keeps it dead simple and easy to inspect. The data lives in one master file that the agents read and write, and every business is de-duplicated by a stable Google ID so we never count the same place twice. We use the **Google Places** service to actually find businesses and check for websites — because "does this business have a website" needs to be a hard fact, not an AI guess — and the local AI is reserved for the *thinking*: classifying, summarizing, rating. There's a clean command-line interface so you can just type a command like "find restaurants in Austin" and it runs. All of that is written up in a document called `ARCHITECTURE.md`, and it's **approved** — we're not guessing when we build.

Then I committed and pushed everything, so the second you accept your invite and pull the repo, it's all there.

## Your next steps

Here's the good news: **your only job right now is to get set up.** You are not building anything yet. I'll say that a few times because I mean it.

Walk through this in order. There's a checklist file called `ONBOARDING_MATT.md` that has every detail, but here's the spirit of it.

Accept your two invites — the **GitHub** one, and the **NotebookLM** share I sent to your email. Those get you into the shared spaces.

Then install a few apps. **Git** and the GitHub command-line tool so you can pull the repo. **Python**, and a tool called `uv` that manages it. **Ollama** — that's the local-AI runner — and note, you'll want your own decent GPU for it to be fast, same as my 3090. Don't pull a specific AI model yet, though, because *I* still need to pick which one we're standardizing on — I'll tell you, then you grab it. Install **Obsidian** — I'll explain why in a second — and your code editor with whichever AI extension you use.

Then, your **own API keys**. This is important: we each use our *own* keys, never shared. You'll get your own Google Places key from Google Cloud, and your own Firecrawl key. They go in a local file that's set up to never be uploaded to the repo, so there's zero risk of leaking them. There's a template file already in there showing you exactly what it looks like — you just copy it and paste your keys in. One quirk to remember: after you set up that file, you have to **restart** your AI tool for it to notice the new connection. It won't show up mid-session.

And that's it. That's the whole job for now. Get set up, and then — and I cannot stress this enough — **do not start building anything past setup until I give you the green light.** The architecture's locked and approved, but I want us starting the actual build *together*, not coming back to find the structure half-built in a direction I didn't expect. When in doubt, the answer is "not yet, ask Sean."

## The resources — use these

Now let me point you at the two things I built specifically so you're never lost.

The first is the **NotebookLM notebook** — I named it "website-builder-brain." Think of it as the project's memory that you can actually *talk to*. All our key documents are loaded in there as sources. And here's the magic: because I generated those mind maps and infographics, you can open it and instead of reading a wall of text, you can look at a **visual map** of how the whole project connects, or expand a node on a mind map and have NotebookLM explain exactly what it is and why it's there. So when you want the big picture, or you're hunting for inspiration on how to structure something, that's where you go. Oh — and one house rule: the notebook is the one thing we *share*, so whenever you add something to it, **put your name on it**, like tag the source as "Matt's." Keeps it clear who added what.

The second is the **Obsidian vault**. Obsidian is a free app that turns a folder of notes into a connected web you can actually see — it draws a graph of how every document links to every other one. I pointed it at our project folder, so the whole repo *is* the vault. When you open it, start at the file called `_HOME.md` — it's the map of the whole place, with links to everything: the constitution, the architecture, your onboarding, the reference library, all of it. Between the NotebookLM brain and the Obsidian vault, you've got both the talk-to-it version and the see-it-all version. You will not be lost.

## What's still missing — my honest reflection

Now, last thing, because I was thinking about this as I built it. If I'm being honest with myself — if a total stranger walked into this repo tomorrow knowing *nothing* about what I did last night, where would they still get stuck? Because you kind of *are* that person this morning. So here's what I think we still need to add, and I'm writing it down so we actually do it:

One — a **glossary**. I've thrown around words like "MCP," "skill," "constitution," "place_id," "scaffold," "agent." Those are obvious to me at 4 a.m. but not to someone fresh. We need a one-page plain-English dictionary of these terms.

Two — a **"how to actually run it" guide**, for once we've built it. Right now everything is *about* the project; there's nothing yet that says "type this command and watch a lead list appear." The moment the pipeline exists, that quickstart is the most important page for a newcomer.

Three — the **"why," not just the "what."** I documented all our decisions, but a newcomer benefits from the reasoning — like *why* Google Places instead of letting the AI just browse, *why* one constitution file instead of three. I captured some of that in the architecture doc, but we should make sure the reasoning is loud, because that's what stops someone from "fixing" something that was a deliberate choice.

Four — a clear **status board** of what's pending. There are a few things in limbo right now: Firecrawl's out of credits, I haven't picked the AI model yet, your invites are still unaccepted. A newcomer needs a single glance at "here's what's done, here's what's waiting, here's what's blocked," so they don't go chasing something that isn't ready.

And five — honestly, *this* briefing is part of the answer. The thing a new person needs most isn't more documents — it's the *story* of how it all fits together and why it exists. Which is exactly what I tried to give you here. So maybe the lesson is: every big session should end with one of these.

That's everything, Matt. The vision, what I built, what you do next, where to look, and what we still owe ourselves. You're caught up — more caught up than I'll be when I actually wake up.

Have a good morning, crumb. I'll be awake soon... signing off.
