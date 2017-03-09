from example.example import RunExample
from run.run_manager import manage
import sys


def single_run(argv):
    RunExample(argv).run()


def double_run(argv):
    # Defining runs
    root_run = RunExample(argv)
    child_run = RunExample(argv)
    runs = [root_run, child_run]
    # Defining dependencies
    child_run.add_previous_run(root_run)
    # Running
    manage(runs)


def fork_run(argv):
    # Defining runs
    root_run = RunExample(argv)
    child1_run = RunExample(argv)
    child2_run = RunExample(argv)
    runs = [root_run, child1_run, child2_run]
    # Defining dependencies
    child1_run.add_previous_run(root_run)
    child2_run.add_previous_run(root_run)
    # Running
    manage(runs)


if __name__ == '__main__':
    single_run(sys.argv[1:])
