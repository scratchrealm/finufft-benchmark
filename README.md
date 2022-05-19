# finufft-benchmark

Run a [FINUFFT](https://finufft.readthedocs.io/en/latest/) benchmarking script and generate a shareable [figurl](https://github.com/scratchrealm/figurl) report.

[See this example report](https://figurl.org/f?v=gs://figurl/figurl-report&d=ipfs://bafkreicybk7hhraqemizo7msk6qgvqdwsetq4e4wj67dswkopjjji4ddke&label=FINUFFT%20benchmark)

This project uses [kachery-cloud](https://github.com/scratchrealm/kachery-cloud) and [figurl](https://github.com/scratchrealm/figurl2).

> **IMPORTANT**: Figurl and kachery-cloud are intended for collaborative sharing of data for scientific research. They should not be used for other purposes.

## Installation and setup

It is recommended that you use a conda environment with Python >= 3.8 and numpy.

[Install FINUFFT](https://finufft.readthedocs.io/en/latest/install.html) in this environment with Python support.

```bash
# clone this repo
git clone <this-repo>

# install this package in editable mode
cd finufft-benchmark
pip install -e .
```

Configure your [kachery-cloud](https://github.com/scratchrealm/kachery-cloud) client (only do this once on your computer)

```bash
kachery-cloud-init
# follow the instructions to associate your client with your Google user name on kachery-cloud
```

## Basic usage

```bash
finufft-benchmark run

# This will print a shareable URL link to the report
# Example output:
# https://figurl.org/f?v=gs://figurl/figurl-report&d=ipfs://bafkreicybk7hhraqemizo7msk6qgvqdwsetq4e4wj67dswkopjjji4ddke&label=FINUFFT%20benchmark
```