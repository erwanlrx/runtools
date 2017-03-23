from run.run_machine import RunGPU, RunCPU
import sys, os

SKELETON_SEQUENCE_TRAIN_PATH = '/home/lear/erleroux/src/skeleton_sequences/tensorflow_main'


def train_val_test_runs(run_argv, job_name, machine='gpu'):
    if machine == 'gpu':
        train_run = RunGPUTrain(run_argv, job_name)
        validation_run = RunGPUEvaluation(run_argv + ['evaluation_name=validation'], job_name)
        test_run = RunGPUEvaluation(run_argv + ['evaluation_name=test'], job_name)
    else:
        train_run = RunGPUTrain(run_argv, job_name)
        validation_run = RunGPUEvaluation(run_argv + ['evaluation_name=validation'], job_name)
        test_run = RunGPUEvaluation(run_argv + ['evaluation_name=test'], job_name)
    # Add dependencies
    validation_run.add_previous_run(train_run)
    test_run.add_previous_run(validation_run)
    return [train_run, validation_run]


class RunGPUTrain(RunGPU):
    def __init__(self, run_argv, job_name):
        RunGPU.__init__(self, run_argv)
        self.python_interpreter = 'python3.5'  # tensorflow installed with python3
        self.path_exe = os.path.join(SKELETON_SEQUENCE_TRAIN_PATH, 'train.py')
        self.job_name = job_name

    @property
    def oarsub_options(self):
        return RunGPU(self).oarsub_options + ' -l "walltime=12:0:0"  -p "gpumem > 3200"'


class RunCPUTrain(RunCPU):
    def __init__(self, run_argv, job_name):
        RunCPU.__init__(self, run_argv)
        self.python_interpreter = 'python3.5'  # tensorflow installed with python3
        self.path_exe = os.path.join(SKELETON_SEQUENCE_TRAIN_PATH, 'train.py')
        self.job_name = job_name

    @property
    def oarsub_options(self):
        return RunCPU(self).oarsub_options + ' -l "nodes=1/core=4,walltime=2:0:0"'


class RunGPUEvaluation(RunGPU):
    def __init__(self, run_argv, job_name):
        RunGPU.__init__(self, run_argv)
        self.python_interpreter = 'python3.5'  # tensorflow installed with python3
        self.path_exe = os.path.join(SKELETON_SEQUENCE_TRAIN_PATH, 'evaluation.py')
        self.job_name = job_name

    @property
    def oarsub_options(self):
        return RunGPU(self).oarsub_options + ' -l "walltime=12:0:0"'


class RunCPUEvaluation(RunCPU):
    def __init__(self, run_argv, job_name):
        RunCPU.__init__(self, run_argv)
        self.python_interpreter = 'python3.5'  # tensorflow installed with python3
        self.path_exe = os.path.join(SKELETON_SEQUENCE_TRAIN_PATH, 'evaluation.py')
        self.job_name = job_name

    @property
    def oarsub_options(self):
        return RunCPU(self).oarsub_options + ' -l "nodes=1/core=4,walltime=2:0:0"'
