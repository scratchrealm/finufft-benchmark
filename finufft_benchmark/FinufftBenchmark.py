import figurl as fig

from typing import List
from .BenchmarkJobGroup import BenchmarkJobGroup


class FinufftBenchmark:
    def __init__(self, job_groups: List[BenchmarkJobGroup]) -> None:
        self._job_groups = job_groups
    def url(self, *, label: str):
        # Prepare the data for the figURL
        data = {
            'job_groups': [
                job_group.to_dict()
                for job_group in self._job_groups
            ]
        }

        # Prepare the figurl Figure
        F = fig.Figure(
            view_url='http://localhost:3000',
            data=data
        )
        url = F.url(label=label)
        return url