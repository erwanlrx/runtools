import os

from run.run_machine import RunCPU
import os.path as op

from settings import DOCUMENTS

TIPHYC_PATH = op.join(DOCUMENTS, "tiphyc_wp3")
local_interpreter = op.join(TIPHYC_PATH, "venv/bin/python3.9")


class AbstractRunTipHyc(RunCPU):
    def __init__(self, run_argv, job_name):
        RunCPU.__init__(self, run_argv)
        self.interpreter = local_interpreter
        self.path_exe = os.path.join(TIPHYC_PATH, 'experiment/{}.py'.format(job_name))
        self.job_name = job_name

    @property
    def oarsub_options(self):
        return RunCPU(self).oarsub_options + ' -l "core=64,walltime=40:0:0"'


class RunCalibrationWendling2019(AbstractRunTipHyc):

    def __init__(self, run_argv):
        super().__init__(run_argv, "main_wendling_2019_obs")


class RunCalibrationWendling2022Obs(AbstractRunTipHyc):

    def __init__(self, run_argv):
        super().__init__(run_argv, "main_wendling_2022_obs")


class RunCalibrationWendling2022Simu(AbstractRunTipHyc):

    def __init__(self, run_argv):
        super().__init__(run_argv, "main_wendling_2022_simu")


if __name__ == '__main__':
    RunCalibrationWendling2022Simu(['0']).run()
    # RunCalibrationWendling2022Obs(['0']).run()
