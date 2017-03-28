from run.run_machine import RunGPU, RunCPU
import sys, os

SKELETON_SEQUENCE_TRAIN_PATH = '/home/lear/erleroux/src/skeleton_sequences/tensorflow_main'
PYTHON_INTERPRETER = 'python3'


def train_val_test_runs(train_run_argv, evaluation_run_argv, job_name, machine='gpu', only_evaluating=False):
    validation_run_argv = evaluation_run_argv + ['evaluation_name=validation']
    test_run_argv = evaluation_run_argv + ['evaluation_name=test']
    if machine == 'gpu':
        train_run = RunGPUTrain(train_run_argv, job_name)
        validation_run = RunGPUEvaluation(validation_run_argv, job_name)
        test_run = RunGPUEvaluation(test_run_argv, job_name)
    else:
        train_run = RunCPUTrain(train_run_argv, job_name)
        validation_run = RunCPUEvaluation(validation_run_argv, job_name)
        test_run = RunCPUEvaluation(test_run_argv, job_name)
    # Add dependencies
    test_run.add_previous_run(validation_run)
    if only_evaluating:
        return [validation_run, test_run]
    else:
        validation_run.add_previous_run(train_run)
        return [train_run, validation_run, test_run]


class RunGPUTrain(RunGPU):
    def __init__(self, run_argv, job_name):
        RunGPU.__init__(self, run_argv)
        self.python_interpreter = PYTHON_INTERPRETER  # tensorflow installed with python3
        self.path_exe = os.path.join(SKELETON_SEQUENCE_TRAIN_PATH, 'train.py')
        self.job_name = job_name

    @property
    def oarsub_options(self):
        return RunGPU(self).oarsub_options + ' -l "walltime=12:0:0" '


class RunCPUTrain(RunCPU):
    def __init__(self, run_argv, job_name):
        RunCPU.__init__(self, run_argv)
        self.python_interpreter = PYTHON_INTERPRETER  # tensorflow installed with python3
        self.path_exe = os.path.join(SKELETON_SEQUENCE_TRAIN_PATH, 'train.py')
        self.job_name = job_name

    @property
    def oarsub_options(self):
        return RunCPU(self).oarsub_options + ' -l "nodes=1/core=4,walltime=2:0:0"'


class RunGPUEvaluation(RunGPU):
    def __init__(self, run_argv, job_name):
        RunGPU.__init__(self, run_argv)
        self.python_interpreter = PYTHON_INTERPRETER  # tensorflow installed with python3
        self.path_exe = os.path.join(SKELETON_SEQUENCE_TRAIN_PATH, 'evaluation.py')
        self.job_name = job_name

    @property
    def oarsub_options(self):
        return RunGPU(self).oarsub_options + ' -l "walltime=12:0:0"'


class RunCPUEvaluation(RunCPU):
    def __init__(self, run_argv, job_name):
        RunCPU.__init__(self, run_argv)
        self.python_interpreter = PYTHON_INTERPRETER  # tensorflow installed with python3
        self.path_exe = os.path.join(SKELETON_SEQUENCE_TRAIN_PATH, 'evaluation.py')
        self.job_name = job_name

    @property
    def oarsub_options(self):
        return RunCPU(self).oarsub_options + ' -l "nodes=1/core=4,walltime=2:0:0"'
