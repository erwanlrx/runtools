from __future__ import absolute_import
from run.run_meta import RunMeta
from settings import settings


class RunGPU(RunMeta):
    def __init__(self, run_argv):
        RunMeta.__init__(self, run_argv)
        self.machine_name = settings['GPU_MACHINE']


class RunCPU(RunMeta):
    def __init__(self, run_argv):
        RunMeta.__init__(self, run_argv)
        self.machine_name = settings['CPU_MACHINE']


class RunNormal(RunMeta):
    def __init__(self, run_argv):
        RunMeta.__init__(self, run_argv)
        self.machine_name = settings['MACHINE']
