import os

from run.run_machine import RunCPU
import os.path as op

from settings import DOCUMENTS

TIPHYC_PATH = op.join(DOCUMENTS, "tiphyc_wp3")
local_interpreter = op.join(TIPHYC_PATH, "venv/bin/python3")


class AbstractRunTipHyc(RunCPU):
    def __init__(self, run_argv, job_name):
        RunCPU.__init__(self, run_argv)
        self.interpreter = local_interpreter
        self.path_exe = os.path.join(TIPHYC_PATH, 'experiment/{}.py'.format(job_name))
        self.job_name = job_name

    @property
    def oarsub_options(self):
        return RunCPU(self).oarsub_options + ' -l "nodes=1/core=4,walltime=10:0:0"'


class RunCalibrationWendling2019(AbstractRunTipHyc):

    def __init__(self, run_argv):
        super().__init__(run_argv, "main_wendling_2019_obs")


if __name__ == '__main__':
    RunCalibrationWendling2019([]).run()
