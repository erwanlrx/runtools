from run_meta import RunCPU
import os, sys


class RunTest(RunCPU):

    def __init__(self):
        RunCPU.__init__(self)
        self.path_exe_run = os.path.join(self.HOME, self.run_dirname, 'test.py')

    def run_options(self):
        return RunCPU.oarsub_options(self) + '-pncore=1 -l "nodes=1,walltime=1:0:0"'

if __name__ == '__main__':
    print(sys.argv)
    RunTest().run(sys.argv[1:])