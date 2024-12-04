import os
import shutil
import json
import click
import yaml
from .run_benchmark import run_benchmark


@click.group(help="finufft-benchmark client")
def cli():
    pass


@click.command(help="Run the benchmark script")
@click.option("--config", default="", help="Config file name")
@click.option('--output', default='finufft-benchmark.json', help='Output file name')
def run(config: str, output: str):
    if config:
        config_fname = config
    else:
        dirname = os.path.dirname(os.path.abspath(__file__))
        config_fname = f"{dirname}/default_config.yml"

    with open(config_fname, "r") as f:
        config0 = yaml.safe_load(f)
    x = run_benchmark(config0)
    print(f'Writing output to {output}')
    with open(output, "w") as f:
        json.dump(x, f, indent=2)


@click.command(
    help="Create a template configuration file config.yml in working directory"
)
def create_config():
    dirname = os.path.dirname(os.path.abspath(__file__))
    config_fname = f"{dirname}/default_config.yml"
    fname = "config.yml"
    if os.path.exists(fname):
        raise Exception(f"File already exists: {fname}")
    shutil.copyfile(config_fname, fname)
    print(f"Config file created: {fname}")


cli.add_command(run)
cli.add_command(create_config)
