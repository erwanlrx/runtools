from distutils.util import strtobool
import sys
import subprocess as sp


# Call bash function from python
def cmd(command, print_command=False):
    if print_command:
        print(command)
    else:
        out = sp.check_output(command, shell=True)
        if isinstance(out, bytes):
            out = out.decode("utf-8")
        return out.split('\n')[:-1]


# Query the user to check parameters settings
def query(question):
    sys.stdout.write('%s [y/n]\n' % question)
    while True:
        try:
            return strtobool(raw_input().lower())
        except ValueError:
            sys.stdout.write('Please respond with \'y\' or \'n\'.\n')


# Kill multiple process of the same kind
def killall(process_name):
    processus = cmd('ps aux | grep ' + process_name)
    processus = [ p for p in processus if 'grep ' not in p]
    print('Listing all the process...')
    for process in processus:
        print(' '.join(process.split()[10:]))
    query('\n Are you sure that you want to delete all the processus above ?')
    for process in processus:
        pid = process.split()[1]
        command = 'kill -9 ' + str(pid)
        print(command)
        cmd(command)


