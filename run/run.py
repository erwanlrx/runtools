from run_meta import RunCPU
import sys, os

""""
Usage Example generating a script calling run_test.py with [parameters]:
    python run.py test [parameters]
"""""


class Run(RunCPU):

    def __init__(self, path_exe_run):
        RunCPU.__init__(self)
        self.path_exe_run = os.path.join(self.HOME, self.run_dirname, 'run_' + path_exe_run + '.py')
        self.debugging_mode = True

    def run_options(self):
        return RunCPU.oarsub_options(self) + '-pncore=1 -l "nodes=1,walltime=100:0:0"'

if __name__ == '__main__':
    argv = list()
    # job_name
    argv.append(sys.argv[2])
    # job_mode for run_master is never in best effort
    argv.append('0')
    # Extend with common arguments for run_*.py file
    print(sys.argv[2:])
    argv.extend(sys.argv[2:])
    Run(sys.argv[1]).run(argv)
