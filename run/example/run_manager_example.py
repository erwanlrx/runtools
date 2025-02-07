import sys
from run.example.run_example import RunExample
from run.run_manager import manage


def single_run(argv):
    RunExample(argv).run()


def double_run(argv):
    # Defining runs
    root_run = RunExample(argv)
    root_run.job_name = 'root'
    child_run = RunExample(argv)
    child_run.job_name = 'child'
    runs = [root_run, child_run]
    # Defining dependencies
    child_run.add_previous_run(root_run)
    # Running
    manage(runs)


def fork_run(argv):
    # Defining runs
    root_run = RunExample(argv)
    root_run.job_name = 'root'
    child1_run = RunExample(argv)
    child1_run.job_name = 'child1'
    child2_run = RunExample(argv)
    child2_run.job_name = 'child2'
    runs = [root_run, child1_run, child2_run]
    # Defining dependencies
    child1_run.add_previous_run(root_run)
    child2_run.add_previous_run(root_run)
    # Running
    manage(runs)


if __name__ == '__main__':
    # single_run(sys.argv[1:])
    # double_run(sys.argv[1:])
    fork_run(sys.argv[1:])

