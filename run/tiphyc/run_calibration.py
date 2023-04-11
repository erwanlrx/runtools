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
        return RunCPU(self).oarsub_options + ' -l "core=64,walltime=40:0:0"'


class RunCalibrationWendling2019(AbstractRunTipHyc):

    def __init__(self, run_argv):
        super().__init__(run_argv, "trajectory", "main_wendling_2019")


class RunCalibrationWendling2022(AbstractRunTipHyc):

    def __init__(self, run_argv):
        super().__init__(run_argv, "trajectory", "main_wendling_2022")

class RunIndicatorComputation(AbstractRunTipHyc):

    def __init__(self, run_argv):
        super().__init__(run_argv, "event_indicator", "main_save_stability_data")

    @property
    def oarsub_options(self):
        return RunCPU(self).oarsub_options + ' -l "core=16,walltime=40:0:0"'


if __name__ == '__main__':
    short_sha = subprocess.check_output(['git', '--git-dir={}/.git'.format(TIPHYC_PATH),
                                         'rev-parse', '--short', 'HEAD']).decode('ascii').strip()
    for i in list(range(3, 5))[:]:
        idx_watershed = str(i)
        # RunCalibrationWendling2022([idx_watershed]).run()
        RunIndicatorComputation([short_sha, idx_watershed]).run()
