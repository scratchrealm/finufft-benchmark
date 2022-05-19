import altair
import platform
import psutil
from datetime import datetime
import figurl as fig
from finufft_benchmark.BenchmarkJob import BenchmarkJob
from finufft_benchmark.BenchmarkJobGroup import BenchmarkJobGroup


def run_benchmark():
    report = fig.Report()
    report.add_markdown(unindent('''
    # FINUFFT benchmark
    '''))
    report.add_markdown(get_system_markdown())

    for transform_type in [1, 2]:
        for nthreads in [1, 4]:
            #######################################################################
            num_uniform_points = 1e6
            num_reps = 4
            eps = 1e-4
            group = BenchmarkJobGroup(
                label = f'Type {transform_type} 3D FINUFFT with varying #n.u. points; #u.={sci(num_uniform_points)}, eps={sci(eps)}, nthreads={nthreads}',
                jobs = [
                    BenchmarkJob(
                        label=f'#n.u.={sci(num_nonuniform_points)}',
                        transform_type=transform_type,
                        num_uniform_points=num_uniform_points,
                        num_nonuniform_points=num_nonuniform_points,
                        eps=eps,
                        num_reps=num_reps,
                        nthreads=nthreads
                    )
                    for num_nonuniform_points in [1e4, 1e5, 1e6, 2e6, 5e6, 8e6, 1e7]
                ]
            )
            group.run()
            report.add_markdown(unindent(f'''
                ## Type {transform_type} 3D FINUFFT - varying num. nonuniform points - {nthreads} thread(s)

                * Num. uniform points: `{sci(num_uniform_points)}`
                * Num. repetitions: `{num_reps}`
                * Epsilon: `{sci(eps)}`
                * Num. threads: `{nthreads}`
            '''))
            layout = report.add_hboxlayout()
            layout.add_altair_chart(
                create_chart1(group, point_type='nonuniform', pps=False)
            )
            layout.add_altair_chart(
                create_chart1(group, point_type='nonuniform', pps=True)
            )

            #######################################################################
            num_nonuniform_points = 1e6
            num_reps = 4
            eps = 1e-4
            group = BenchmarkJobGroup(
                label = f'Type {transform_type} 3D FINUFFT with varying #u. points; #n.u.={sci(num_nonuniform_points)}, eps={sci(eps)}, nthreads={nthreads}',
                jobs = [
                    BenchmarkJob(
                        label=f'#u.={sci(num_uniform_points)}',
                        transform_type=transform_type,
                        num_uniform_points=num_uniform_points,
                        num_nonuniform_points=num_nonuniform_points,
                        eps=eps,
                        num_reps=num_reps,
                        nthreads=nthreads
                    )
                    for num_uniform_points in [1e4, 1e5, 1e6, 2e6, 5e6, 8e6, 1e7]
                ]
            )
            group.run()
            report.add_markdown(unindent(f'''
                ## Type {transform_type} 3D FINUFFT - varying num. uniform points - {nthreads} thread(s)

                * Num. nonuniform points: `{sci(num_nonuniform_points)}`
                * Num. repetitions: `{num_reps}`
                * Epsilon: `{sci(eps)}`
                * Num. threads: `{nthreads}`
            '''))
            layout = report.add_hboxlayout()
            layout.add_altair_chart(
                create_chart1(group, point_type='uniform', pps=False)
            )
            layout.add_altair_chart(
                create_chart1(group, point_type='uniform', pps=True)
            )

    url = report.url(label='FINUFFT benchmark')
    print(url)
    # https://figurl.org/f?v=http://localhost:3000&d=ipfs://bafkreig7yr3ahtnscvm6kdbf2hxizkq54d6rkyti62dhywszn6yy3mryo4&label=FINUFFT%20benchmark

    return url

def sci(x: float):
    a = '{:e}'.format(x)
    return a.split('e')[0].rstrip('0').rstrip('.') + 'e' + a.split('e')[1]

def unindent(x: str):
    lines = x.splitlines()
    if len(lines) == 0: return x
    j = 0
    while j < len(lines) and len(lines[j]) == 0:
        j = j + 1
    first_line = lines[j]
    i = 0
    while i < len(first_line) and first_line[i] == ' ': i = i + 1
    return '\n'.join([
        line[i:]
        for line in lines
    ])

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

def get_system_markdown():
    uname = platform.uname()
    cpufreq = psutil.cpu_freq()
    svmem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return unindent(f'''
    ## System information
    
    ```
    System: {uname.system}
    Node name: {uname.node}
    Release: {uname.release}
    Version: {uname.version}
    Machine: {uname.machine}
    Processor: {uname.processor}
    Physical cores: {psutil.cpu_count(logical=False)}
    Total cores: {psutil.cpu_count(logical=True)}
    CPU freq. (min/max/current): {cpufreq.max:.2f}/{cpufreq.min:.2f}/{cpufreq.current:.2f} Mhz
    
    Memory
    Total: {get_size(svmem.total)}
    Available: {get_size(svmem.available)}
    Used: {get_size(svmem.used)}

    SWAP
    Total: {get_size(swap.total)}
    Free: {get_size(swap.free)}
    Used: {get_size(swap.used)}

    Date: {datetime.now()}
    ```

    ''')

def create_chart1(group: BenchmarkJobGroup, *, point_type: str, pps: bool):
    data = []
    key = 'num_nonuniform_points' if point_type == 'nonuniform' else 'num_uniform_points'
    for job in group._jobs:
        results = job.results
        for result in results:
            num_points = job.args[key]
            value = result['elapsed'] if not pps else num_points / result['elapsed']
            data.append({
                'num_points': job.args[key],
                'value': value
            })
    title = f'Elapsed time vs num. {point_type} points' if not pps else f'Points per second vs num. {point_type} points'
    return altair.Chart(
        data=altair.Data(values=data)
    ).mark_circle().encode(
        x=altair.X(
            'num_points:Q',
            scale=altair.Scale(type="log"),
            title=f'Num. {point_type} points'
        ),
        y=altair.Y(
            'value:Q',
            scale=altair.Scale(type="log"),
            title='Elapsed time (sec)' if not pps else 'Points per second'
        )
    ).properties(
        title=title
    )