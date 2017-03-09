from run.run_meta import RunMeta
from pytools.tools import cmd

""" Class of functions that take a list of RunObject as input """


def manage(runs, sleep_duration=10):
    runs_waiting_previous_jobs = runs  # type: list[RunMeta]
    runs_waiting_max_default_jobs = []  # type: list[RunMeta]
    while runs_waiting_previous_jobs != [] and runs_waiting_max_default_jobs != []:
        # runs waiting because of previous jobs
        for run in runs_waiting_previous_jobs:
            if run.previous_jobs_ended:
                runs_waiting_previous_jobs.remove(run)
                runs_waiting_max_default_jobs.append(run)
        # runs waiting because of max default jobs
        for run in runs_waiting_max_default_jobs:
            if run_avaible(run.machine_name):
                run.run()
        # sleeping
        cmd('sleep %i' % sleep_duration)


def run_avaible(machine):
    pass


def visualizes(runs):
    # Get a summary of the result
    # or get a summary of why it crashed
    pass
