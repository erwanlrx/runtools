from __future__ import absolute_import
from run.run_meta import RunMeta
from settings import GPU_MACHINE, MACHINE


class RunGPU(RunMeta):
    def __init__(self, run_argv):
        RunMeta.__init__(self, run_argv)
        self.machine_name = GPU_MACHINE


class RunCPU(RunMeta):
    def __init__(self, run_argv):
        RunMeta.__init__(self, run_argv)
        self.machine_name = MACHINE
