import os, sys
from random import randint
from pytools.tools import cmd
from settings import settings

"""
General pipeline of the run method:
    -A bash script is generated
    -Wait for previous jobs to be ended
    -If previous jobs have not crashed:
        -A job is launched to process the bash script we just generated
        -Wait while the job is not done
        -If the job failed (detected if the script is still there, because if no exception the script should delete itself)
         then in that case, the stderr is sent by email
        -If the job was a success, data are extracted from stdout and stderr

General organisation:
    -job_dirname is defined as settings['HOME']/settings['OAR_DIRNAME']/job_name
    -Bash Script are stored in job_dirname/settings['SCRIPT_DIRNAME']
    -stdout and stderr files for oarsub are stored in job_dirname/setting['OARSUB_DIRNAME']
"""


class RunMeta(object):
    def __init__(self, run_argv):
        self.run_argv = run_argv
        # Organization settings
        self.job_name = None
        # Run settings
        self.machine_name = None
        self.besteffort = False
        self.path_exe_run = None
        self.path_exe_monitor = None
        self.previous_jobs = []  # type: list[RunMeta]
        self.oarstat_check_frequency = 5
        # Internal settings (do not override these field)
        self.job_crashed = False
        self.job_id = None
        self.script_filename_key = None

    def run(self):
        # Dependency wrt previous jobs
        # wait for previous jobs to end
        while not self.previous_jobs_ended:
            cmd('sleep %i' % self.oarstat_check_frequency)
        # check if previous jobs have crashed or not
        for jobs in self.previous_jobs:
            if jobs.job_crashed:
                self.job_crashed = True
                break

        if not self.job_crashed:
            # Script generation
            self.generate_script()

            # Job management
            # run a job with oarsub (its job_id is retrieved)
            self.job_id = cmd(self.oarsub_command)[-1].split('=')[-1]
            # wait for the job to end
            while not self.job_ended:
                cmd('sleep %i' % self.oarstat_check_frequency)

            # Job study
            # check if job ended well (i.e., script should have deleted itself)
            # TODO: check if in  a killed besteffort, that the script is not deleted
            if os.path.exists(self.script_filename):
                # delete the bash script
                cmd('rm ' + self.script_filename)
                # send a report of the crash by mail
                command_mail = 'cat ' + os.path.join(self.oarsub_dirname, self.job_id + '_stderr.txt')
                command_mail += ' | mail -s "Failure report of ' + self.job_name + '" ' + settings['EMAIL']
                cmd(command_mail)
                # declare job as crashed to avoid running following jobs
                self.job_crashed = True
            else:
                self.job_done = True
                # final monitoring
                self.monitoring()
                # TODO Philippe lui copie les fichier OAR a une destination correspond au model que l on a en entraine,
                # TODO proposer surement l empalcement du fichier ou le fichier doit etre copie
                # TODO in the process let the path to the OAR files to come back process them again if needed
                # self.path_exe_parse()

    def generate_script(self):
        """
        Generate an executable bash script containing a list of commands
        :param argv: parameters for the script to run
        """
        # build script_dirname if it has not yet been created
        if not os.path.exists(self.script_dirname):
            os.makedirs(self.script_dirname)
        # create script_filename file
        cmd('touch ' + self.script_filename)
        # building the list of commands for the script
        commands = list()
        # launch a python exe
        print(self.path_exe_run)
        commands.append('python ' + self.path_exe_run + ' ' + ' '.join(self.run_argv))
        # script file delete itself when finished
        commands.append('rm ' + self.script_filename + '\n')
        # write into the bash script
        with open(self.script_filename, 'w') as f:
            for command in commands:
                print(command)
                f.write('{0} \n'.format(command))
        # give the permission to the bash script to execute
        cmd('chmod +x ' + self.script_filename)

    @property
    def job_dirname(self):
        assert self.job_name is not None
        return os.path.join(settings['HOME'], settings['OAR_DIRNAME'], self.job_name)

    @property
    def script_filename(self):
        """
        A script filename must match a single run object
        Therefore each script_filename_nb must be different and have an individual key
        A natural way to define keys would be to iterate
        However, if two jobs with the same job_name create the same key at the time, it would crash
        that's the reason I decided to use a random number to define the key
        :return: a string specifying the path to the bash script
        """
        if self.script_filename_key is None:
            # initializing the script_filename_key
            self.script_filename_key = 0
            while os.path.exists(self.get_script_filename):
                self.script_filename_key = randint(0, 10000)
        return self.get_script_filename

    @property
    def get_script_filename(self):
        return os.path.join(self.script_dirname,
                            str(self.script_filename_key) + '.sh')

    @property
    def job_ended(self):
        ended = True
        if self.job_crashed:
            return ended
        else:
            oarstat_lines = cmd("ssh " + self.machine_name + " ' oarstat ' ")
            for line in oarstat_lines:
                if self.job_id in line:
                    ended = False
                    break
            return ended

    @property
    def previous_jobs_ended(self):
        ended = True
        for jobs in self.previous_jobs:
            if jobs.job_ended:
                ended = False
                break
        return ended

    """  """

    @property
    def oarsub_command(self):
        # Connect to the appropriate machine
        command = "ssh " + self.machine_name + " ' oarsub "
        # Add the running options for oarsub
        command += self.oarsub_options
        # Naming the job
        command += ' --name="' + self.job_name + '"'
        # Build the oarsub directory
        if not os.path.exists(self.oarsub_dirname):
            os.makedirs(self.oarsub_dirname)
        # Redirecting the stdout and stderr
        stdnames = ['out', 'err']
        stdfiles = [os.path.join(self.oarsub_dirname, '%jobid%_std' + stdname + '.txt') for stdname in stdnames]
        for stdname, stdfile in zip(stdnames, stdfiles):
            command += ' --std' + stdname + '="' + stdfile + '"'
        # Finally add the script to launch
        command += ' "' + self.script_filename + '"'
        command += " '"
        print(command)
        return command

    @property
    def oarsub_options(self):
        options = ''
        if self.besteffort:
            options += '-t besteffort -t idempotent'
        return options + ' '

    @property
    def oarsub_dirname(self):
        return os.path.join(self.job_dirname, settings['OARSUB_DIRNAME'])

    @property
    def script_dirname(self):
        return os.path.join(self.job_dirname, settings['SCRIPT_DIRNAME'])