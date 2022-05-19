import os
import click
from .run_benchmark import run_benchmark


@click.group(help="finufft-benchmark client")
def cli():
    pass

@click.command(help="Run the benchmark script")
def run():
    run_benchmark()

cli.add_command(run)