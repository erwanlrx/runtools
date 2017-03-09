from run.run_meta import RunGPU, RunCPU
import os
import sys

PYTHON_DEEPLAB_DIR = '/home/lear/erleroux/Documents/deeplab/python'


class RunDeeplabCPU(RunCPU):

    def __init__(self):
        RunCPU.__init__(self)
        self.path_exe = os.path.join(PYTHON_DEEPLAB_DIR, 'main.py')

    @property
    def run_options(self):
        return RunCPU.oarsub_options + '-pncore=32 -l "nodes=1,walltime=12:0:0"'


class RunDeeplabTrainGPU(RunGPU):

    def __init__(self):
        RunGPU.__init__(self)
        self.path_exe = os.path.join(PYTHON_DEEPLAB_DIR, 'interface.py')

    def run_options(self):
        return RunGPU.oarsub_options(self) + '-p "gpumem > 9200" -l "walltime=12:0:0"'


class RunDeeplabTestGPU(RunGPU):

    def __init__(self):
        RunGPU.__init__(self)
        self.path_exe = os.path.join(PYTHON_DEEPLAB_DIR, 'interface.py')

    def run_options(self):
        return RunGPU.oarsub_options(self) + '-p "gpumem > 3200" -l "walltime=12:0:0"'


if __name__ == '__main__':
    mode = sys.argv[1]
    translation_dictionary = {'ta': 'train', 'te': 'test', 'pa': 'post-train', 'pe': 'post-test'}
    #Auxiliary_functions.user_yes_no_query('Mode to be used: \n-' + ' \n-'.join([v for k, v in translation_dictionary.items() if k in mode]) + '\n')
    argv = sys.argv[2:]
    argv_stage = list(argv)
    index_stage = 6
    if 'ta' in mode:
        argv_stage[index_stage] = '0'
        RunDeeplabTrainGPU().launch(argv_stage)
    if 'te' in mode:
        argv_stage[index_stage] = '1'
        RunDeeplabTestGPU().launch(argv_stage)
    if 'pa' in mode:
        argv_stage[index_stage] = '0'
        postprocess_argv = argv_stage[:-1] + ['all', 'all']
        RunDeeplabCPU().launch(postprocess_argv)
    if 'pe' in mode:
        argv_stage[index_stage] = '1'
        postprocess_argv = argv_stage[:-1] + ['fc8', 'all']
        RunDeeplabCPU().launch(postprocess_argv)



