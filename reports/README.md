# Reports

These Markdown files are generated Obsidian views of the lead stores.

- `Sean - AI Leads.md`
- `Sean - Prioritized Leads.md`
- `Matt - AI Leads.md`
- `Matt - Prioritized Leads.md`
- `Shared - AI Leads.md`
- `Shared - Prioritized Leads.md`

Do not hand-edit report contents. Regenerate them with:

```powershell
uv run leadpipe report --profile sean
uv run leadpipe report --profile matt
```

Shared reports are read-only views built from `data/sean/leads.jsonl` and `data/matt/leads.jsonl`.
