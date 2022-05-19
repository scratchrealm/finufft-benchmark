from typing import List
from .BenchmarkJob import BenchmarkJob

class BenchmarkJobGroup:
    def __init__(self, *, jobs: List[BenchmarkJob], label: str) -> None:
        self._jobs = jobs
        self._label = label
    @property
    def jobs(self):
        return self._jobs
    @property
    def label(self):
        return self._label
    def run(self):
        print('********************************************************')
        print(f'Job group {self._label}')
        for jj, job in enumerate(self.jobs):
            print(f'Job {jj + 1} of {len(self.jobs)}: {job.label}')
            job.run()
    def to_dict(self):
        return {
            'label': self._label,
            'jobs': [j.to_dict() for j in self._jobs]
        }