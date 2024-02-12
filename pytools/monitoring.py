import subprocess as sp
import os, sys
from pytools.tools import cmd
from settings import OARSUB_DIRNAME, MACHINE, LOGIN_ONLINE

""" Monitor only the master"""

if __name__ == '__main__':

    while 1:
        print_line = ' \nMonitoring... \n'
        for machine in [MACHINE]:
            try:
                jobs = cmd("ssh " + machine + " 'oarstat | grep " + LOGIN_ONLINE + "'")
            except sp.CalledProcessError as e:
                jobs = []
                print_line += 'No jobs running on ' + machine + '\n'
            if jobs != []:
                print_line += machine + ':' + '\n'
                for job in jobs:
                    # Monitoring only non interactive jobs
                    if (job.split(' ')[-2]).split('J=')[-1] != 'I':

                        # Extracting information and initializing a list for printing
                        job_id = job.split(' ')[0]
                        job_name = ''
                        if len(job.split('N=')) > 1 and len((job.split('N=')[1]).split(' (')) > 0:
                            job_name = (job.split('N=')[1]).split(' (')[0]
                        duration = (job.split(' R=')[0]).split(' ')[-1]
                        print_list = [job_name, job_id, duration]

                        # TODO:Let user write function to parse the OAR files, and display information during monitoring
                        # with this kind of stuff we can open the OAR file:
                        # os.path.join(OARSUB_DIRNAME, job_name, job_id + 'stderr')

                        print_line += '  '.join(print_list) + '\n'
        print(print_line)
        # Possibility to configure the refreshing time lapse
        if len(sys.argv) > 1:
            cmd('sleep ' + sys.argv[1])
        else:
            cmd('sleep 2')
