import sys
from run.skeleton_sequences.run_train import train_val_test_runs
from run.run_manager import manage

sys.path.append('/home/lear/erleroux/src/skeleton_sequences')
from tensorflow_runs.argument_generator import main_argv, run_prefix_suffix


from itertools import product


runs = []

""" COPY AREA"""
run_prefix = 'restore_gpu_drop_clip'
idxs = [[0], [1], [0], [0]]

restore = True
restore_run_dir = 'gpu_drop_clip-learning_rate0.005-dropout_prob0.5-clip_gradient_norm1-rnn_units100-rnn_layers3-rnn_typelstm_1'
restore_checkpoint_filename = '5000'

# Training setting
for idx in product(*idxs):
    argv1 = main_argv(*idx)
    argv1.extend(['training_steps=20000', 'top_n_to_test=5',
                  'summary_flush_rate=100', 'checkpoint_rate=1000'])

    # Training hyperparameters
    # TODO: add type of prediction, and regularization parameter
    for batch_size, learning_rate, dropout_prob, clip_gradient_norm in product([256], [1e-4], [0.5], [1]):
        argv2 = argv1[:] + ['batch_size=' + str(batch_size), 'learning_rate=' + str(learning_rate)]
        argv2 += ['dropout_prob=' + str(dropout_prob), 'clip_gradient_norm=' + str(clip_gradient_norm)]

        # Model hyperparameters
        for rnn_units, rnn_layers, rnn_type in product([100], [3], ['lstm']):
            argv3 = argv2[:]
            argv3.extend(['rnn_units=' + str(rnn_units), 'rnn_layers=' + str(rnn_layers), 'rnn_type=' + rnn_type])

            """ END COPY AREA """

            # Extend the list of runs
            # Train argv
            train_run_argv = argv3 + ['run_prefix=' + run_prefix]
            if restore:
                train_run_argv.append('restore_run_dir=' + restore_run_dir)
                train_run_argv.append('restore_checkpoint_filename=' + restore_checkpoint_filename)
            # Evaluation argv
            job_name = run_prefix + run_prefix_suffix(argv3)
            evaluation_run_argv = argv3 + ['run_prefix=' + job_name]
            runs.extend(train_val_test_runs(train_run_argv, evaluation_run_argv, job_name,
                                            machine='gpu', only_evaluating=True))
# print(len(runs) / 3)
manage(runs)
