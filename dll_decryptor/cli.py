from __future__ import annotations

import sys
from pathlib import Path

import click
from rich.console import Console

from dll_decryptor.pipeline.runner import PipelineRunner
from dll_decryptor.utils.log import setup_logging

console = Console()


@click.group()
@click.option("--verbose", is_flag=True, help="Enable debug logging.")
def cli(verbose: bool) -> None:
    setup_logging(verbose=verbose)


@cli.command()
@click.argument("target", type=click.Path(exists=True, path_type=Path))
@click.option("--out", default="output", type=click.Path(path_type=Path))
@click.option("--scheme", default=None, help="Force a decryptor scheme.")
def decrypt(target: Path, out: Path, scheme: str | None) -> None:
    """Run the full ingest -> analyze -> decrypt -> dump pipeline."""
    runner = PipelineRunner(output_dir=out, forced_scheme=scheme)
    result = runner.run(target)
    if result.recovered:
        console.print(f"[green]recovered[/green] -> {result.output_path}")
    else:
        console.print("[yellow]no decryptor matched[/yellow]")
        sys.exit(2)


@cli.command()
@click.argument("target", type=click.Path(exists=True, path_type=Path))
def analyze(target: Path) -> None:
    """Print section entropy and detected scheme for a DLL."""
    from dll_decryptor.pipeline.analyze.entropy import section_report

    for row in section_report(target):
        console.print(row)


if __name__ == "__main__":
    cli()