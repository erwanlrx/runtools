from run.run_meta import RunMeta
from pytools.tools import cmd
from settings import MAX_DEFAULT_JOBS

""" Class of functions that take a list of RunMeta as input """


def manage(runs, sleep_duration=1):
    runs_waiting_previous_jobs = runs  # type: list[RunMeta]
    runs_waiting_max_default_jobs = []  # type: list[RunMeta]
    while runs_waiting_previous_jobs != [] or runs_waiting_max_default_jobs != []:
        # runs waiting because of previous jobs
        selected_runs = []
        for run in runs_waiting_previous_jobs:
            if run.previous_jobs_ended:
                selected_runs.append(run)
        for run in selected_runs:
            runs_waiting_previous_jobs.remove(run)
            runs_waiting_max_default_jobs.append(run)
        # runs waiting because of max default jobs
        selected_run = []
        for run in runs_waiting_max_default_jobs:
            if run_available(run.machine_name):
                # a single run is selected to avoid exceeding max default jobs
                selected_run.append(run)
                break
        for run in selected_run[:1]:
            run.run()
            runs_waiting_max_default_jobs.remove(run)
        # sleeping
        cmd('sleep %i' % sleep_duration)


def run_available(machine_name):
    oarstat_lines = cmd("ssh " + machine_name + " ' oarstat ' ")
    jobs_nb = 0
    for line in oarstat_lines:
        if 'erleroux' in line:
            jobs_nb += 1
    return jobs_nb < MAX_DEFAULT_JOBS[machine_name]


