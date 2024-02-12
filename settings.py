import os
import os.path as op

# Personnal settings
LOGIN_LOCAL = 'administrateur'
LOGIN_ONLINE = 'lerouerw'


def replace_user(s):
    return s.replace(LOGIN_LOCAL, LOGIN_ONLINE)


# Directory settings
DOCUMENTS = '/home/administrateur/Documents'
PROJECT_PATH = os.path.join(DOCUMENTS, 'runtools')
LINK_PATH = op.join(DOCUMENTS, 'links')
OARSUB_DIRNAME = os.path.join(LINK_PATH, 'oarsub')
SCRIPT_DIRNAME = os.path.join(LINK_PATH, 'script')

# Cluster settings
MACHINE = 'dahu.ciment'
GPU_MACHINE = 'edgar'
MAX_DEFAULT_JOBS = {GPU_MACHINE: 2, MACHINE: 10}
