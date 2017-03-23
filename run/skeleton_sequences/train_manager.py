import sys

sys.path.append('/home/lear/erleroux/src/skeleton_sequences')
from tensorflow_runs.argument_manager_generator import get_argv_list, get_run_prefix_suffix

from run.run_manager import manage
from itertools import product
from run.skeleton_sequences.run_train import train_val_test_runs

runs = []

""" COPY AREA"""
run_prefix = 'gpu_rnn_train_validate'
idxs = [[0], [1], [0], [0]]

restore = False
restore_run_dir = 'gpu_rnn_1'
restore_checkpoint_filename = '1000'

for idx in product(*idxs):
    # Looping on all the desired
    argv_list = list()
    argv_list.extend(get_argv_list(*idx))
    argv_list.append('run_prefix=' + run_prefix)
    argv_list.append('training_steps=1000')

    for batch_size, learning_rate in product([128], [1e-2]):
        extended_argv_list = argv_list[:]
        extended_argv_list.append('batch_size=' + str(batch_size))
        extended_argv_list.append('learning_rate=' + str(learning_rate))

        if restore:
            extended_argv_list.append('restore=True')
            extended_argv_list.append('restore_run_dir=' + restore_run_dir)
            extended_argv_list.append('restore_checkpoint_filename=' + restore_checkpoint_filename)
        """ END COPY AREA """

        # Extend the list of runs
        _, run_prefix_suffix = get_run_prefix_suffix(extended_argv_list)
        runs.extend(train_val_test_runs(extended_argv_list, job_name=run_prefix + run_prefix_suffix))
manage(runs)
