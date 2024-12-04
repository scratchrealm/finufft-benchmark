import time
import math
from typing import Union
import numpy as np
import finufft


class BenchmarkJob:
    def __init__(
        self,
        *,
        label: str,
        transform_type: int,  # 1 or 2
        num_uniform_points: int,
        num_nonuniform_points: int,
        eps: float,
        num_reps: int,
        nthreads: Union[int, None],
    ) -> None:
        self._label = label
        self._args = {
            "transform_type": transform_type,
            "num_uniform_points": num_uniform_points,
            "num_nonuniform_points": num_nonuniform_points,
            "eps": eps,
            "num_reps": num_reps,
            "nthreads": nthreads,
        }
        self._results = None

    @property
    def label(self):
        return self._label

    @property
    def args(self):
        return self._args

    @property
    def results(self):
        return self._results

    def to_dict(self):
        return {"label": self._label, "args": self._args, "results": self._results}

    def run(self):
        self._results = _run_benchmark_job(**self._args)


def _run_benchmark_job(
    *,
    transform_type: int,
    num_uniform_points: int,
    num_nonuniform_points: int,
    eps: float,
    num_reps: int,
    nthreads: Union[int, None],
):
    n0 = int(np.ceil(num_uniform_points ** (1.0 / 3)))
    uniform_grid_size = [n0, n0, n0]
    [ms, mt, mu] = uniform_grid_size
    nj = int(num_nonuniform_points)
    xj = np.random.rand(nj) * 2 * math.pi - math.pi
    yj = np.random.rand(nj) * 2 * math.pi - math.pi
    zj = np.random.rand(nj) * 2 * math.pi - math.pi
    if transform_type == 1:
        cj = np.random.rand(nj) + 1j * np.random.rand(nj)
        fk = np.zeros([ms, mt, mu], dtype=np.complex128)
    elif transform_type == 2:
        cj = np.zeros([nj], dtype=np.complex128)
        fk = np.random.rand(ms, mt, mu) + 1j * np.random.rand(ms, mt, mu)
    else:
        raise Exception(f"Unexpected transform type: {transform_type}")
    iflag = 1

    opts = {}
    if nthreads is not None:
        opts["nthreads"] = nthreads

    results = []
    for j in range(num_reps):
        timer = time.time()
        if transform_type == 1:
            finufft.nufft3d1(xj, yj, zj, cj, fk.shape, fk, eps, iflag, **opts)
        elif transform_type == 2:
            finufft.nufft3d2(xj, yj, zj, fk, cj, eps, iflag, **opts)
        else:
            raise Exception(f"Unexpected transform type: {transform_type}")
        elapsed = time.time() - timer
        results.append({"elapsed": elapsed})
    return results
