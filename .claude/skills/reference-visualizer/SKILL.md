---
name: reference-visualizer
description: >
  website-builder reference-library visualizer. When a new doc is added to
  docs/_reference-library/, proactively OFFERS (asks first) to generate a NotebookLM mind map +
  infographic visualization in the established 3-tier framework. Trigger when a new reference doc
  appears, or user says "visualize reference library", "make mind map", "generate visualization",
  "/reference-visualizer", "approve pending", or "process pending approvals".
---

# Reference Visualizer — website-builder

> **Provenance:** This visualization framework was **created and used by Sean** across the existing
> reference-library docs (AI Build Bible, Custom SDKs Bible, the Comprehensive_* guides, Master
> Skills Catalog). It is the established, owner-blessed pattern for this project. Follow it exactly.

Generates two companions for any text doc in `docs/_reference-library/`, using the shared NotebookLM
brain notebook:

- `(Mind Map) <DocBaseName>/<DocBaseName>.md` — NotebookLM mind map, JSON converted to nested bullets
- `(Visualization) <DocBaseName>/<DocBaseName>.png` — NotebookLM infographic (professional / portrait)

**Notebook:** website-builder-brain · **ID:** `bd83690f-e997-46c5-b054-6ff3139e11d6`

---

## Step 0 — Detect & OFFER (proactive, but ALWAYS ask first)

This skill runs in **proactive-offer** mode. Whenever you add or notice a new `.md` in
`docs/_reference-library/` that is missing its `(Mind Map)` and/or `(Visualization)` companion
folders, you must **offer** to generate them.

**HARD RULE — never generate without an explicit yes.** NotebookLM artifact generation takes minutes
and adds sources to the shared notebook; do not run it silently.

Offer like this, listing the exact doc(s):
> "New reference doc detected: `<DocName>`. Want me to generate its mind map + visualization
>  (same framework Sean uses for the rest of the library)? **Yes / No / Unsure**."

### Branch on the response
- **Yes** → run Steps 1–5.
- **No / not now** → do nothing. Confirm skipped.
- **Unsure** (Matt or anyone not Sean, or anyone who says "not sure / ask Sean / later") → **DO NOT
  generate.** Log it to the Pending Approvals queue (Step 6) and tell them it's saved for Sean's review.

`<DocBaseName>` = the file name with a leading `(Raw Text) ` prefix removed and `.md` stripped.
Example: `(Raw Text) Master_Skills_Catalog.md` → `Master_Skills_Catalog`.

---

## Step 1 — Set notebook context
```powershell
py -m notebooklm use bd83690f-e997-46c5-b054-6ff3139e11d6
```

## Step 2 — Add the doc as a source (capture the source ID)
```powershell
py -m notebooklm source add "./docs/_reference-library/(Raw Text) <DocBaseName>.md"
# → "Added source: <SOURCE_ID>"
```
> Syntax note: content is POSITIONAL; notebook is `-n/--notebook`. There is NO `--file`/`--notebook-id`.

## Step 3 — Generate the mind map (capture the note ID)
```powershell
py -m notebooklm generate mind-map -s <SOURCE_ID>
# → "Note ID: <NOTE_ID>"
```
> Gotcha: `generate mind-map` has **NO `--wait` flag** — passing it errors. It returns immediately.

Then pull the note and convert JSON → nested bullets. `note get` output is JSON wrapped in a 3-line
`ID:/Title:/Content:` header — **strip the header before `json.loads`**. Use a temp Python script
(Windows bash heredoc quoting is flaky):

```python
# convert_one.py  — args: <NOTE_ID> <DocBaseName>
import json, re, sys, os, subprocess
note_id, base = sys.argv[1], sys.argv[2]
raw = subprocess.run(["py","-m","notebooklm","note","get",note_id],
                     capture_output=True, text=True, encoding="utf-8").stdout
data = json.loads(raw[raw.find("{"):])  # strip header
def bullets(n, d=0):
    out=["  "*d + "- " + n["name"]]
    for c in n.get("children",[]): out += bullets(c, d+1)
    return out
folder = rf"docs\_reference-library\(Mind Map) {base}"
os.makedirs(folder, exist_ok=True)
open(os.path.join(folder, base+".md"), "w", encoding="utf-8").write(
f"""# {data['name']}

> Mind map generated from companion text doc: `../(Raw Text) {base}.md`
> Open with **Markmap** plugin in Obsidian for an interactive visual mind map view.

---

""" + "\n".join(bullets(data)) + "\n")
print("wrote", folder)
```
Run: `py convert_one.py <NOTE_ID> <DocBaseName>` then delete the temp script.

## Step 4 — Generate + download the infographic
```powershell
py -m notebooklm generate infographic -s <SOURCE_ID> --style professional --orientation portrait
# → "Started: <ARTIFACT_ID>"
py -m notebooklm artifact wait <ARTIFACT_ID> --timeout 600
py -m notebooklm download infographic -a <ARTIFACT_ID> "docs\_reference-library\(Visualization) <DocBaseName>\<DocBaseName>.png" --force
```
(Create the `(Visualization) <DocBaseName>` folder first if needed.)

## Step 5 — Report
List both created files. Remind: the source + artifacts are also in the shared `website-builder-brain`
notebook, so **Matt** can click/expand the mind map there and ask NotebookLM what each node means.

---

## Step 6 — Pending Approvals queue (the "Unsure" branch)

File: `docs/_reference-library/_PENDING_APPROVALS.md` (underscore sorts to top). Create with this
header if it doesn't exist:
```markdown
# Pending Approvals — Reference Visualizations

Docs awaiting **Sean's** approval before mind map + visualization are generated.
Sean: say "approve pending" / "process pending approvals" to action these.

- [ ] <example>
```
Append one line per deferred doc:
```
- [ ] <DocBaseName> — requested by <user> on <YYYY-MM-DD> — awaiting Sean's approval
```
Tell the requester: "Logged to Pending Approvals for Sean to review — nothing generated yet."

### When Sean says "approve pending" / "process pending approvals"
1. Read `_PENDING_APPROVALS.md`, list the unchecked `- [ ]` items.
2. Confirm with Sean which to generate (still ask — Sean may approve some, not all).
3. For each approved item, run Steps 1–5.
4. Mark it done: flip `- [ ]` → `- [x]` and append ` — generated <YYYY-MM-DD>`.

Only **Sean** can approve. If anyone else asks to process the queue, decline and note it needs Sean.
