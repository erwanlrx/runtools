from __future__ import absolute_import
import os, sys
from random import randint
from tools.tools import cmd

"""
General pipeline of the run method:
    -A bash script is generated
    -A job is launched to process the script we just generated
    -Wait while the job is not done
    -If the job failed (detected if the script is still there, because if no exception the script should delete itself)
     then in that case, the stderr is sent by email
    -If the job was a success, data are extracted from stdout and stderr
"""


class RunMeta(object):

    def __init__(self):
        self.email = 'erwan.le-roux@inria.fr'
        # Organization settings
        self.HOME = '/home/lear/erleroux'
        self.run_dirname = 'src/deepoar/run'
        self.oar_dirname = 'OAR'
        self.oar_path = None
        self.scripts_dirname = 'Scripts'
        self.script_filename = None
        # Job setting
        self.job_mode = None
        self.job_name = None
        self.job_id = None
        self.job_done = False
        self.debugging_mode = False
        # Run settings
        self.machine_name = None
        self.path_exe_run = None
        self.path_exe_monitor = ''
        self.path_exe_parse = None

    def run(self, argv):
        """
        :param argv[0]:  run_mode
        :param argv[1]:  script_filename
        :param argv[2:]:  parameters to launch the experiment
        :return:
        """
        "Script Generation"
        self.job_name = argv[0]
        self.job_mode = argv[1]
        # generate a bash script containing all the desired commands
        if self.debugging_mode:
            self.generate_script(argv[2:])
        else:
            self.generate_script(argv[2:] + ['1'])

        "Job management"
        # oarsub bash command launches a job and its job_id is retrieved
        self.job_id = cmd(self.oarsub_command())[-1].split('=')[-1]
        # wait for the job to end
        while not self.job_ended(self.job_id):
            cmd('sleep 5')

        "Job study"
        # check if job ended well, i.e., bash script should have deleted itself
        if os.path.exists(self.script_filename):
            # delete the script
            cmd('rm ' + self.script_filename)
            # send a report of the crash by mail
            # TODO no crash for run_* files maybe, voir si cela arrive, si il y a 2 crash recus a chaque fois
            command_mail = 'cat ' + os.path.join(self.oar_path, self.job_id + '_stderr.txt')
            command_mail += ' | mail -s "Failure report of ' + self.job_name + '" ' + self.email
            cmd(command_mail)
            # raise an exception to stop related jobs
            raise Exception('Failure')
        else:
            self.job_done = True # verifier le fonctionnement dans le cas d un besteffort kill est ce que le script continue de tourner?
            #process les OAR file
            # TODO Philippe lui copie les fichier OAR a une destination correspond au model que l on a en entraine,
            # TODO proposer surement l empalcement du fichier ou le fichier doit etre copie
            # TODO in the process let the path to the OAR files to come back process them again if needed
            #self.path_exe_parse()

    def generate_script(self, argv):
        """
        Generate a executable script containing commands
        :param argv: parameters for the script to run
        """
        # a script filename MUST match a single run object
        # to define diverse filenames we use the job_name + parameters + a random number if necessary
        self.script_filename = os.path.join(self.HOME, self.scripts_dirname, self.job_name + '_'.join(argv) + '.sh')
        while os.path.exists(self.script_filename):
            self.script_filename = os.path.join(self.HOME, self.scripts_dirname, self.job_name +
                                                str(randint(0, 10000)) + '_'.join(argv) + '.sh')
        cmd('touch ' + self.script_filename)
        # building the list of commands for the script
        commands = list()
        # print way to monitor OAR files at the first line of stdout file
        # TODO encoding for path_exe_monitor, what should be printed? peut etre mettre une expression regulière
        commands.append('echo ' + self.path_exe_monitor)
        # launch a python exe in a non-debugging mode
        print(self.path_exe_run)
        commands.append('python ' + self.path_exe_run + ' ' + ' '.join(argv))
        # script file delete itself when finished
        commands.append('rm ' + self.script_filename + '\n')
        with open(self.script_filename, 'w') as f:
            for command in commands:
                print(command)
                f.write('{0} \n'.format(command))
        cmd('chmod +x ' + self.script_filename)

    def oarsub_command(self):
        # Connect to the appropriate machine
        command = "ssh " + self.machine_name + " ' oarsub "
        # Add the running options for oarsub
        command += self.oarsub_options()
        # Naming the job
        command += ' --name="' + self.job_name + '"'
        # Build the OAR directory
        self.oar_path = os.path.join(self.HOME, self.oar_dirname, self.job_name)
        if not os.path.exists(self.oar_path):
            os.makedirs(self.oar_path)
        # Redirecting the stdout and stderr
        stdnames = ['out', 'err']
        stdfiles = [os.path.join(self.oar_path, '%jobid%_std' + stdname + '.txt') for stdname in stdnames]
        for stdname, stdfile in zip(stdnames, stdfiles) :
            command += ' --std' + stdname +'="' + stdfile + '"'
        # Finally add the script to launch
        command += ' "' + self.script_filename + '"'
        command += " '"
        print(command)
        return command

    def oarsub_options(self):
        return {'0': '', '1': '-t besteffort -t idempotent'}[self.job_mode] + ' '

    def job_ended(self, job_id):
        oarstat_lines = cmd("ssh " + self.machine_name + " ' oarstat ' ")
        ended = True
        for line in oarstat_lines:
            if job_id in line:
                ended = False
        return ended


class RunGPU(RunMeta):

    def __init__(self):
        RunMeta.__init__(self)
        self.machine_name = "edgar"


class RunCPU(RunMeta):

    def __init__(self):
        RunMeta.__init__(self)
        self.machine_name = "clear"


class RunNormal(RunMeta):

    def __init__(self):
        RunMeta.__init__(self)
        self.machine_name = "aquarius"
