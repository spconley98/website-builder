# Data

Profile-owned lead stores live here.

- `sean/leads.jsonl` — source of truth for Sean's lead data.
- `matt/leads.jsonl` — source of truth for Matt's lead data.

There is no shared writable `data/leads.jsonl` anymore. Shared visibility comes from generated reports
under `reports/`, which are deduped by `place_id` across profile stores.

Agents may update their assigned profile store only:

```powershell
uv run leadpipe find --profile sean ...
uv run leadpipe find --profile matt ...
```

Do not hand-edit JSONL unless Sean explicitly asks for a repair. Use leadpipe commands whenever
possible so validation, deduping, and status rules stay intact.
