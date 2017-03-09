from run.run_machine import RunGPU, RunCPU
import os

PYTHON_DEEPLAB_DIR = '/home/lear/erleroux/Documents/deeplab/python'


class RunDeeplabCPU(RunCPU):

    def __init__(self):
        RunCPU.__init__(self)
        self.path_exe = os.path.join(PYTHON_DEEPLAB_DIR, 'main.py')

    @property
    def run_options(self):
        return RunCPU.oarsub_options + '-pncore=32 -l "nodes=1,walltime=12:0:0"'


class RunDeeplabTrainGPU(RunGPU):

    def __init__(self):
        RunGPU.__init__(self)
        self.path_exe = os.path.join(PYTHON_DEEPLAB_DIR, 'interface.py')

    def run_options(self):
        return RunGPU.oarsub_options(self) + '-p "gpumem > 9200" -l "walltime=12:0:0"'


class RunDeeplabTestGPU(RunGPU):

    def __init__(self):
        RunGPU.__init__(self)
        self.path_exe = os.path.join(PYTHON_DEEPLAB_DIR, 'interface.py')

    def run_options(self):
        return RunGPU.oarsub_options(self) + '-p "gpumem > 3200" -l "walltime=12:0:0"'



