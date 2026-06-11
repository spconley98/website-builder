# Reports

These Markdown files are generated Obsidian views of the lead stores.

- `Sean - AI Leads.md`
- `Sean - Prioritized Leads.md`
- `Sean - Website Briefs.md`
- `Matt - AI Leads.md`
- `Matt - Prioritized Leads.md`
- `Matt - Website Briefs.md`
- `Shared - AI Leads.md`
- `Shared - Prioritized Leads.md`
- `Shared - Website Briefs.md`

Do not hand-edit report contents. Regenerate them with:

```powershell
uv run leadpipe report --profile sean
uv run leadpipe report --profile matt
```

Shared reports are read-only views built from `data/sean/leads.jsonl` and `data/matt/leads.jsonl`.
Website Brief reports are draft build/sales intelligence and need human review before outreach.
