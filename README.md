# finufft-benchmark

> :warning: Under construction

Run a [FINUFFT](https://finufft.readthedocs.io/en/latest/) benchmarking script and generate a shareable [figurl](https://github.com/scratchrealm/figurl2) report.

[See this example report](https://figurl.org/f?v=gs://figurl/figurl-report&d=ipfs://bafkreicjsyiqyg5wy6e5cddf2tufxtzbegmitwsj4v3fkqtilzz4slojhe&label=FINUFFT%20benchmark)

The idea is to provide an easy means of benchmarking the FINUFFT library on any computer and generating a report in the form of a figurl link, suitable for sharing and archiving.

This project uses [kachery-cloud](https://github.com/scratchrealm/kachery-cloud) and [figurl](https://github.com/scratchrealm/figurl2).

> **IMPORTANT**: Figurl and kachery-cloud are intended for collaborative sharing of data for scientific research. They should not be used for other purposes.

## Installation and setup

Should work on both Linux and Mac OS.

It is recommended that you use a conda environment with Python >= 3.8 and numpy.

Step 1: [Install FINUFFT](https://finufft.readthedocs.io/en/latest/install.html) in this environment with Python support.

Step 2: Install finufft-benchmark

```bash
# clone this repo
git clone <this-repo>

# install this package in editable mode
cd finufft-benchmark
pip install -e .
```

Step 3: Configure your [kachery-cloud](https://github.com/scratchrealm/kachery-cloud) client (only do this once on your computer)

```bash
kachery-cloud-init
# follow the instructions to associate your client with your Google user name on kachery-cloud
```

## Basic usage

From a terminal

```bash
finufft-benchmark run

# This will print a shareable URL link to the report
# Example output:
# https://figurl.org/f?v=gs://figurl/figurl-report&d=ipfs://bafkreicjsyiqyg5wy6e5cddf2tufxtzbegmitwsj4v3fkqtilzz4slojhe&label=FINUFFT%20benchmark
```

## Customizing the benchmarking script

To customize the benchmarking with your own parameters, you can pass in a configuration file:

```bash
finufft-benchmark run --config config.yml
```

To generate a template config file:
```bash
finufft-benchmark create-config

# This will create a config.yml file in your working directory
# Edit this file as needed
```

Here is an [example config file](./finufft_benchmark/default_config.yml).

Jobs are organized into groups of the following plot types
* varying-uniform-points
* varying-nonuniform-points
* varying-nthreads

The following parameters can be controlled
* transform_type: 1 or 2 (3 not supported yet)
* plot_type: see above
* epsilon: e.g, 1.e-6
* num_uniform_points: number of uniform points (or list if plot type is varying-uniform-points)
* num_nonuniform_points: number of nonuniform points (or list if plot type is varying-nonuniform-points)
* nreps: number of repetitions per data point
* nthreads: number of threads (or list if plot type is varying-nthreads)