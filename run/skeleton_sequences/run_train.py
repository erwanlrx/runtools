from run.run_machine import RunGPU
import sys, os

SKELETON_SEQUENCE_TRAIN_PATH = '/home/lear/erleroux/src/skeleton_sequences/tensorflow_train'


class RunTrain(RunGPU):
    def __init__(self, run_argv):
        RunGPU.__init__(self, run_argv)
        self.python_interpreter = 'python 3.5'  # tensorflow installed with python3
        self.path_exe = os.path.join(SKELETON_SEQUENCE_TRAIN_PATH, 'train.py')

    @property
    def oarsub_options(self):
        return RunGPU(self).oarsub_options + '-p "gpumem > 3200" -l "walltime=12:0:0"'


class RunTest(RunGPU):
    pass


def train_val_test_runs(sys_argv):
    runs = []

    # if the network was not stopped before, train until the end

    # validate each checkpoint that are created

    # only if I didn't not suppress the training (because I realized it was not learning well enough)
    # finally run on the test set,
    # whatever checkpoint that add the best score
    # on the validation set

    return runs


if __name__ == '__main__':
    pass
