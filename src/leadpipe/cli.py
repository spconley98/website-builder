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
from .config import load_settings, targets_path_for_profile
from .llm import LLMError, generate
from .sources import google_places
from .store import DEFAULT_PROFILE, LeadStore, normalize_profile

app = typer.Typer(help="Local-AI lead pipeline — find businesses with no website, rate by photo availability.")
console = Console()
DEFAULT_LEAD_LIMIT = 20


def _targets_or_exit(area: str | None, industry: str | None, radius: str | None, profile: str):
    settings = load_settings(targets_path_for_profile(profile))
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


def _store_for_profile(profile: str) -> LeadStore:
    try:
        return LeadStore.for_profile(profile)
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(code=1) from e


def _profile_or_exit(profile: str) -> str:
    try:
        return normalize_profile(profile)
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(code=1) from e


def _refresh_reports(store: LeadStore, profile: str) -> None:
    reports.write_reports(store, profile=profile)
    reports.write_shared_reports()
    console.print("[dim]Profile + shared reports refreshed in reports/[/dim]")


@app.command()
def check(
    google: bool = typer.Option(
        False,
        "--google",
        help="Also make a tiny Google Places request to verify the key/API toggle.",
    ),
):
    """Check local setup: keys, Ollama model, and optional Google Places access."""
    settings = load_settings()
    console.print("[bold]leadpipe setup check[/bold]")

    console.print(f"  Google Places key: {'set' if settings.google_places_api_key else '[yellow]missing[/yellow]'}")
    console.print(f"  Firecrawl key: {'set' if settings.firecrawl_api_key else '[yellow]missing[/yellow]'}")
    console.print(f"  LLM model: {settings.llm_model}")
    console.print(f"  LLM base URL: {settings.llm_base_url}")

    try:
        response = generate(
            "Reply with exactly: OK",
            system="You are a setup smoke test. Reply with exactly OK.",
            temperature=0.0,
            settings=settings,
        )
        console.print(f"  Ollama smoke test: [green]ok[/green] ({response})")
    except LLMError as e:
        console.print(f"  Ollama smoke test: [red]failed[/red] — {e}")
        raise typer.Exit(code=1)

    if google:
        try:
            hits = google_places.search_businesses("Round Rock, TX", "coffee shops")
            console.print(f"  Google Places smoke test: [green]ok[/green] ({len(hits)} result(s))")
        except google_places.PlacesError as e:
            console.print(f"  Google Places smoke test: [red]failed[/red] — {e}")
            raise typer.Exit(code=1)

    console.print("[green]Setup check complete.[/green]")


@app.command()
def find(
    area: str | None = typer.Option(None, help='e.g. "Austin, TX" — overrides targets.yaml for one run'),
    industry: str | None = typer.Option(None, help='e.g. "restaurants" — used with --area'),
    radius: str | None = typer.Option(None, help='e.g. "5km" — used with --area'),
    profile: str = typer.Option(DEFAULT_PROFILE, help="Owner profile whose agents may write this run: sean or matt"),
    limit: int = typer.Option(
        DEFAULT_LEAD_LIMIT,
        min=1,
        max=20,
        help="Maximum Google Places candidates per industry. Default safety cap is 20.",
    ),
):
    """Run Lead Finder on prompt only — default cap is 20 candidates per industry."""
    profile = _profile_or_exit(profile)
    targets = _targets_or_exit(area, industry, radius, profile)
    store = _store_for_profile(profile)
    console.print(f"[bold]Lead Finder[/bold] — {len(targets)} target(s), profile={profile}, limit={limit}")
    _print_report(pipeline.run_stage("find", store, targets, limit=limit))
    _refresh_reports(store, profile)


@app.command()
def prioritize(
    area: str | None = typer.Option(None, help="restrict to leads found in this area"),
    industry: str | None = typer.Option(None, help="restrict to this industry"),
    radius: str | None = typer.Option(None),
    profile: str = typer.Option(DEFAULT_PROFILE, help="Owner profile whose leads may be prioritized: sean or matt"),
):
    """Run Lead Prioritizer on prompt only — this stage uses Firecrawl credits."""
    profile = _profile_or_exit(profile)
    targets = _targets_or_exit(area, industry, radius, profile)
    store = _store_for_profile(profile)
    console.print(f"[bold]Lead Prioritizer[/bold] — {len(targets)} target(s), profile={profile}")
    _print_report(pipeline.run_stage("prioritize", store, targets))
    _refresh_reports(store, profile)


@app.command()
def run(
    area: str | None = typer.Option(None, help="override targets.yaml for one run"),
    industry: str | None = typer.Option(None),
    radius: str | None = typer.Option(None),
    profile: str = typer.Option(DEFAULT_PROFILE, help="Owner profile whose agents may write this run: sean or matt"),
    limit: int = typer.Option(
        DEFAULT_LEAD_LIMIT,
        min=1,
        max=20,
        help="Maximum Google Places candidates per industry. Default safety cap is 20.",
    ),
):
    """Run the full pipeline on prompt only (find -> prioritize) across every target."""
    profile = _profile_or_exit(profile)
    targets = _targets_or_exit(area, industry, radius, profile)
    store = _store_for_profile(profile)
    console.print(f"[bold]Full pipeline[/bold] — {len(targets)} target(s), profile={profile}, limit={limit}")
    _print_report(pipeline.run_all(store, targets, limit=limit))
    _refresh_reports(store, profile)


@app.command()
def report(
    profile: str = typer.Option(DEFAULT_PROFILE, help="Owner profile to render: sean or matt"),
    shared: bool = typer.Option(True, "--shared/--no-shared", help="Also regenerate shared Sean/Matt reports."),
):
    """Regenerate profile + shared clickable Markdown reports from current stores."""
    profile = _profile_or_exit(profile)
    store = _store_for_profile(profile)
    all_path, prioritized_path = reports.write_reports(store, profile=profile)
    console.print(f"Wrote {all_path.relative_to(reports.ROOT)}")
    console.print(f"Wrote {prioritized_path.relative_to(reports.ROOT)}")
    if shared:
        shared_all_path, shared_prioritized_path = reports.write_shared_reports()
        console.print(f"Wrote {shared_all_path.relative_to(reports.ROOT)}")
        console.print(f"Wrote {shared_prioritized_path.relative_to(reports.ROOT)}")


if __name__ == "__main__":
    app()
