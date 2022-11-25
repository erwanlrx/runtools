from run.run_machine import RunCPU
import os
from settings import DOCUMENTS

# Enable to parallelize, and accelerate the creation of datasets
SKELETON_SEQUENCE_DATASET_WRITER_PATH = os.path.join(DOCUMENTS, 'src/skeleton_sequences/tensorflow_datasets')


class RunDataset(RunCPU):
    def __init__(self, run_argv):
        RunCPU.__init__(self, run_argv)
        self.path_exe = os.path.join(SKELETON_SEQUENCE_DATASET_WRITER_PATH, 'preprocessed_dataset_writer.py')
        self.job_name = 'validation_test_joint'
        self.interpreter = 'python3'
        self.librairies_to_install = ['python3-scipy']

    @property
    def oarsub_options(self):
        return RunCPU(self).oarsub_options + ' -l "nodes=1/core=32,walltime=20:0:0"'


if __name__ == '__main__':
    RunDataset([]).run()
