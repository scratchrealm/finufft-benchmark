from typing import List
import platform
import psutil
import time
from finufft_benchmark.BenchmarkJob import BenchmarkJob
from finufft_benchmark.BenchmarkJobGroup import BenchmarkJobGroup


def run_benchmark(config: dict):
    config_groups = config["groups"]

    groups = []

    # Can't get table of contents working right now
    # because anchor links don't work inside Markdown react component
    # contents_md = '---\n'
    # for config_group in config_groups:
    #     label = config_group['label']
    #     contents_md = contents_md + f'* [{label}](#{"-".join(label.split(" "))})\n'
    # report.add_markdown(contents_md)

    for config_group in config_groups:
        label: str = config_group["label"]
        transform_type: int = config_group["transform_type"]
        plot_type: str = config_group["plot_type"]
        epsilon: float = config_group["epsilon"]
        if plot_type == "varying-nonuniform-points":
            num_uniform_points: int = config_group["num_uniform_points"]  # type: ignore
            num_nonuniform_points: List[int] = config_group["num_nonuniform_points"]  # type: ignore
            nthreads: int = config_group["nthreads"]  # type: ignore
        elif plot_type == "varying-uniform-points":
            num_nonuniform_points: int = config_group["num_nonuniform_points"]  # type: ignore
            num_uniform_points: List[int] = config_group["num_uniform_points"]  # type: ignore
            nthreads: int = config_group["nthreads"]  # type: ignore
        elif plot_type == "varying-nthreads":
            num_nonuniform_points: int = config_group["num_nonuniform_points"]
            num_uniform_points: int = config_group["num_uniform_points"]
            nthreads: List[int] = config_group["nthreads"]
        else:
            raise Exception(f"Unexpected plot type: {plot_type}")
        nreps = config_group["nreps"]

        if plot_type == "varying-nonuniform-points":
            jobs = [
                BenchmarkJob(
                    label=f"#n.u.={sci(num)}",
                    transform_type=transform_type,
                    num_uniform_points=num_uniform_points,
                    num_nonuniform_points=num,
                    eps=epsilon,
                    num_reps=nreps,
                    nthreads=nthreads,  # type: ignore
                )
                for num in num_nonuniform_points  # type: ignore
            ]
        elif plot_type == "varying-uniform-points":
            jobs = [
                BenchmarkJob(
                    label=f"#u.={sci(num)}",
                    transform_type=transform_type,
                    num_uniform_points=num,
                    num_nonuniform_points=num_nonuniform_points,
                    eps=epsilon,
                    num_reps=nreps,
                    nthreads=nthreads,  # type: ignore
                )
                for num in num_uniform_points  # type: ignore
            ]
        elif plot_type == "varying-nthreads":
            jobs = [
                BenchmarkJob(
                    label=f"#threads={num}",
                    transform_type=transform_type,
                    num_uniform_points=num_uniform_points,
                    num_nonuniform_points=num_nonuniform_points,
                    eps=epsilon,
                    num_reps=nreps,
                    nthreads=num,
                )
                for num in nthreads
            ]
        else:
            raise Exception(f"Unexpected plot type: {plot_type}")
        group = BenchmarkJobGroup(label=label, jobs=jobs)
        group.run()
        groups.append(group.to_dict())

    return {
        'system_info': get_system_info(),
        'groups': groups
    }


def sci(x: float):
    a = "{:e}".format(x)
    return a.split("e")[0].rstrip("0").rstrip(".") + "e" + a.split("e")[1]


def unindent(x: str):
    lines = x.splitlines()
    if len(lines) == 0:
        return x
    j = 0
    while j < len(lines) and len(lines[j]) == 0:
        j = j + 1
    first_line = lines[j]
    i = 0
    while i < len(first_line) and first_line[i] == " ":
        i = i + 1
    return "\n".join([line[i:] for line in lines])


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def get_system_info():
    uname = platform.uname()
    cpufreq = psutil.cpu_freq()
    svmem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return {
        "system": uname.system,
        "node": uname.node,
        "release": uname.release,
        "version": uname.version,
        "machine": uname.machine,
        "processor": uname.processor,
        "physical_cores": psutil.cpu_count(logical=False),
        "total_cores": psutil.cpu_count(logical=True),
        "cpu_freq_min": cpufreq.min,
        "cpu_freq_max": cpufreq.max,
        "cpu_freq_current": cpufreq.current,
        "memory_total": svmem.total,
        "memory_available": svmem.available,
        "memory_used": svmem.used,
        "swap_total": swap.total,
        "swap_free": swap.free,
        "swap_used": swap.used,
        "date": time.time()
    }
