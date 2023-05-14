import os
import subprocess

from run.run_machine import RunCPU
import os.path as op

from settings import DOCUMENTS

TIPHYC_PATH = op.join(DOCUMENTS, "tiphyc_wp3")
local_interpreter = op.join(TIPHYC_PATH, "venv/bin/python3.9")


class AbstractRunTipHyc(RunCPU):
    def __init__(self, run_argv, analysis_folder, job_name):
        RunCPU.__init__(self, run_argv)
        self.interpreter = local_interpreter
        self.path_exe = os.path.join(TIPHYC_PATH, 'analysis/{}/{}.py'.format(analysis_folder, job_name))
        self.job_name = job_name

    @property
    def oarsub_options(self):
        return RunCPU(self).oarsub_options + ' -l "core=16,walltime=40:0:0"'


class RunCalibrationWendling2019(AbstractRunTipHyc):

    def __init__(self, run_argv):
        super().__init__(run_argv, "trajectory", "main_wendling_2019")


class RunCalibrationTipHycAnnual(AbstractRunTipHyc):

    def __init__(self, run_argv):
        super().__init__(run_argv, "trajectory", "main_tiphyc_annual")


class RunIndicatorComputation(AbstractRunTipHyc):

    def __init__(self, run_argv):
        super().__init__(run_argv, "stability_data", "main_save_stability_data")

    @property
    def oarsub_options(self):
        return RunCPU(self).oarsub_options + ' -l "core=16,walltime=40:0:0"'


def main_save_indicator():
    short_sha = subprocess.check_output(['git', '--git-dir={}/.git'.format(TIPHYC_PATH),
                                         'rev-parse', '--short', 'HEAD']).decode('ascii').strip()
    for i in range(5, 8):
        idx_watershed = str(i)
        for j in [0, 9][1:]:
            idx_final_year = str(j)
            RunIndicatorComputation([short_sha, idx_watershed, idx_final_year]).run()


def main_wendling2022_training():
    for i in range(3):
        idx_watershed = str(i)
        RunCalibrationTipHycAnnual([idx_watershed]).run()


if __name__ == '__main__':
    main_save_indicator()
    # main_wendling2022_training()
