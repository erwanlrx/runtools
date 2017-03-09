from run.run_meta import RunMeta
from pytools.tools import cmd

""" Class of functions that take a list of RunObject as input """


def manage(runs, sleep_duration=1):
    runs_waiting_previous_jobs = runs  # type: list[RunMeta]
    runs_waiting_max_default_jobs = []  # type: list[RunMeta]
    while runs_waiting_previous_jobs != [] or runs_waiting_max_default_jobs != []:
        print('loop')
        # runs waiting because of previous jobs
        selected_runs = []
        for run in runs_waiting_previous_jobs:
            print('loop1')
            if run.previous_jobs_ended:
                print('Switch list', run.job_name)
                selected_runs.append(run)
        for run in selected_runs:
            runs_waiting_previous_jobs.remove(run)
            runs_waiting_max_default_jobs.append(run)
        # runs waiting because of max default jobs
        selected_runs = []
        for run in runs_waiting_max_default_jobs:
            if run_avaible(run.machine_name):
                selected_runs.append(run)
                run.run()
        for run in selected_runs:
            runs_waiting_max_default_jobs.remove(run)
        # sleeping
        cmd('sleep %i' % sleep_duration)

# TODO The manager is going to be the one doing the visualization somewhere


def run_avaible(machine):
    return True


def visualizes(runs):
    # Get a summary of the result
    # or get a summary of why it crashed
    pass
