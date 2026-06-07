"""leadpipe — the Matt-friendly entry point (ARCHITECTURE.md §8).

    leadpipe find --area "Austin, TX" --industry restaurants   # one stage, one-off
    leadpipe prioritize                                         # next stage on existing leads
    leadpipe run                                                 # full pipeline, batch from targets.yaml
    leadpipe report                                              # regenerate the clickable views

CLI flags override targets.yaml for a quick experiment; omit them to run the
whole repeatable batch list (ARCHITECTURE.md §8 — config file vs flags).
"""
from __future__ import annotations

import typer
from rich.console import Console

from . import pipeline, reports
from .config import load_settings
from .store import LeadStore

app = typer.Typer(help="Local-AI lead pipeline — find businesses with no website, rate by photo availability.")
console = Console()


def _targets_or_exit(area: str | None, industry: str | None, radius: str | None):
    settings = load_settings()
    targets = pipeline.resolve_targets(settings, area=area, industry=industry, radius=radius)
    if not targets:
        console.print(
            "[yellow]No targets given and config/targets.yaml is empty.[/yellow]\n"
            "Either pass --area (and optionally --industry/--radius), "
            "or add entries to config/targets.yaml."
        )
        raise typer.Exit(code=1)
    return targets


def _print_report(report: pipeline.RunReport) -> None:
    for line in report.summary().splitlines():
        console.print(f"  {line}")
    total_errors = sum(len(r.errors) for r in report.results)
    if total_errors:
        console.print(f"[yellow]{total_errors} issue(s) — re-run to retry; nothing crashed.[/yellow]")
        for r in report.results:
            for e in r.errors:
                console.print(f"    [dim]{r.agent}:[/dim] {e}")


@app.command()
def find(
    area: str | None = typer.Option(None, help='e.g. "Austin, TX" — overrides targets.yaml for one run'),
    industry: str | None = typer.Option(None, help='e.g. "restaurants" — used with --area'),
    radius: str | None = typer.Option(None, help='e.g. "5km" — used with --area'),
):
    """Run Lead Finder — search an area/industry, store businesses with no website."""
    targets = _targets_or_exit(area, industry, radius)
    store = LeadStore()
    console.print(f"[bold]Lead Finder[/bold] — {len(targets)} target(s)")
    _print_report(pipeline.run_stage("find", store, targets))
    reports.write_reports(store)
    console.print("[dim]Reports refreshed in reports/[/dim]")


@app.command()
def prioritize(
    area: str | None = typer.Option(None, help="restrict to leads found in this area"),
    industry: str | None = typer.Option(None, help="restrict to this industry"),
    radius: str | None = typer.Option(None),
):
    """Run Lead Prioritizer — rate existing 'found' leads by photo availability."""
    targets = _targets_or_exit(area, industry, radius)
    store = LeadStore()
    console.print(f"[bold]Lead Prioritizer[/bold] — {len(targets)} target(s)")
    _print_report(pipeline.run_stage("prioritize", store, targets))
    reports.write_reports(store)
    console.print("[dim]Reports refreshed in reports/[/dim]")


@app.command()
def run(
    area: str | None = typer.Option(None, help="override targets.yaml for one run"),
    industry: str | None = typer.Option(None),
    radius: str | None = typer.Option(None),
):
    """Run the full pipeline (find -> prioritize) across every target."""
    targets = _targets_or_exit(area, industry, radius)
    store = LeadStore()
    console.print(f"[bold]Full pipeline[/bold] — {len(targets)} target(s)")
    _print_report(pipeline.run_all(store, targets))
    reports.write_reports(store)
    console.print("[dim]Reports refreshed in reports/[/dim]")


@app.command()
def report():
    """Regenerate the clickable Markdown reports from the current store (no agents run)."""
    store = LeadStore()
    all_path, prioritized_path = reports.write_reports(store)
    console.print(f"Wrote {all_path.relative_to(reports.ROOT)}")
    console.print(f"Wrote {prioritized_path.relative_to(reports.ROOT)}")


if __name__ == "__main__":
    app()
