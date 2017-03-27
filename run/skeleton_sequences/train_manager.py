import sys
from run.skeleton_sequences.run_train import train_val_test_runs
from run.run_manager import manage

sys.path.append('/home/lear/erleroux/src/skeleton_sequences')
from tensorflow_runs.argument_generator import main_argv, run_prefix_suffix


from itertools import product


runs = []

""" COPY AREA"""
run_prefix = 'urnn_grid'
idxs = [[0], [1], [0], [0]]

restore = False
restore_run_dir = 'gpu_rnn_1'
restore_checkpoint_filename = '10000'

# Training setting
for idx in product(*idxs):
    argv1 = main_argv(*idx)
    argv1.extend(['run_prefix=' + run_prefix, 'training_steps=20000', 'top_n_to_test=5',
                  'summary_flush_rate=100', 'checkpoint_rate=1000'])

    # Training hyperparameters
    # TODO: add type of prediction, and regularization parameter
    for batch_size, learning_rate in product([256], [1e-3]):
        argv2 = argv1[:] + ['batch_size=' + str(batch_size), 'learning_rate=' + str(learning_rate)]

        # Model hyperparameters
        for rnn_units, rnn_layers, rnn_type in product([100], [1, 2], ['lstm', 'gru']):
            argv3 = argv2[:]
            argv3.extend(['rnn_units=' + str(rnn_units), 'rnn_layers=' + str(rnn_layers), 'rnn_type=' + rnn_type])

            # Restore settings
            if restore:
                argv3.append('restore_run_dir=' + restore_run_dir)
                argv3.append('restore_checkpoint_filename=' + restore_checkpoint_filename)
            """ END COPY AREA """

            # Extend the list of runs
            runs.extend(train_val_test_runs(argv3, run_prefix, run_prefix_suffix(argv3), machine='gpu'))
# print(len(runs) / 3)
manage(runs)
