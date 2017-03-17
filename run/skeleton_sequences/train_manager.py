from run.run_manager import manage
from itertools import product
from run.skeleton_sequences.run_train import train_val_test_runs

# The goal in the end is just to launch One Single manager
# one a big list of jobs

runs = []
run_prefix = 'first_run'
idxs = [[0], [0], [0], [0]]
restore = False
for idx in product(*idxs):
    # Looping on all the desired
    argv_list = list()
    argv_list.append('run_prefix=' + run_prefix)
    argv_list.append('split_name=train500')
    argv_list.extend(get_argv_list(*idx))

    for batch_size, learning_rate in product([20], [1e-4]):
        extended_argv_list = argv_list[:]
        extended_argv_list.append('batch_size=' + str(batch_size))
        extended_argv_list.append('learning_rate=' + str(learning_rate))

        if restore:
            checkpoint_filename = ''
            history_filename = ''
            history_argv = ['batch_size', 'learning_rate']
            # Add some restore_parameter
            extended_argv_list.append('restore=True')
            extended_argv_list.append('checkpoint_filename=' + checkpoint_filename)
            extended_argv_list.append('history_argv=' + '*'.join(history_argv))

        sys_argv = ' '.join(extended_argv_list)
        runs.append(train_val_test_runs(sys_argv))
manage(runs)
