from __future__ import absolute_import
from run.run_machine import RunCPU
import os, sys
from settings import settings

RUN_PATH = os.path.join(settings['HOME'], 'src/tools/run')


class RunExample(RunCPU):
    def __init__(self, run_argv):
        RunCPU.__init__(self, run_argv)
        self.path_exe_run = os.path.join(RUN_PATH, 'example.py')
        self.job_name = 'example'

    @property
    def oarsub_options(self):
        return super().oarsub_options + '-pncore=1 -l "nodes=1,walltime=1:0:0"'


if __name__ == '__main__':
    run_example_argv = sys.argv[1:]
    RunExample(run_argv=run_example_argv).run()
