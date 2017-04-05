from run.run_machine import RunCPU
import os, sys
from settings import HOME

# Enable to parallelize, and accelerate the creation of datasets
SKELETON_SEQUENCE_DATASET_WRITER_PATH = os.path.join(HOME, 'src/skeleton_sequences/tensorflow_datasets')
PYTHON_INTERPRETER = 'python3'


class RunDataset(RunCPU):
    def __init__(self, run_argv):
        RunCPU.__init__(self, run_argv)
        self.path_exe = os.path.join(SKELETON_SEQUENCE_DATASET_WRITER_PATH, 'preprocessed_dataset_writer.py')
        self.job_name = 'dataset'
        self.python_interpreter = PYTHON_INTERPRETER

    @property
    def oarsub_options(self):
        return RunCPU(self).oarsub_options + ' -l "nodes=1/core=8,walltime=10:0:0"'


if __name__ == '__main__':
    RunDataset([]).run()
