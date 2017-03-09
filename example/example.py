from pytools.tools import cmd
from run.run_machine import RunCPU
import os, sys
from settings import HOME

EXAMPLE_PATH = os.path.join(HOME, 'src/tools/example')


class RunExample(RunCPU):
    def __init__(self, run_argv):
        RunCPU.__init__(self, run_argv)
        self.path_exe_run = os.path.join(EXAMPLE_PATH, 'example.py')
        self.job_name = 'example'

    @property
    def oarsub_options(self):
        return RunCPU(self).oarsub_options + ' -l "nodes=1/core=1,walltime=1:0:0"'


if __name__ == '__main__':
    cmd('sleep 20')
