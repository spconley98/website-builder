# Config

Human-edited hunt lists live here.

- `targets.sean.yaml` — Sean's default batch hunt list.
- `targets.matt.yaml` — Matt's default batch hunt list.
- `targets.example.yaml` — starter/example targets only; do not use it as a shared working queue.

CLI flags override these files for one-off runs:

```powershell
uv run leadpipe find --profile sean --area "Round Rock, TX" --industry "coffee shops"
```

Agents must keep Sean and Matt target files separate unless Sean explicitly asks to merge or copy
targets between profiles.
