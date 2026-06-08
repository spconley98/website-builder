"""Tests for CLI safety rails around credit-backed stages."""
from __future__ import annotations

from typer.testing import CliRunner

from leadpipe import pipeline
from leadpipe.cli import app

runner = CliRunner()


def test_credit_backed_commands_require_firecrawl_guard():
    for command in ["prioritize", "run", "intelligence"]:
        result = runner.invoke(app, [command])

        assert result.exit_code == 1
        assert "Firecrawl credits" in result.output
        assert "--use-firecrawl" in result.output


def test_pipeline_stage_order_is_deterministic():
    assert list(pipeline.STAGES) == ["find", "prioritize", "intelligence"]
