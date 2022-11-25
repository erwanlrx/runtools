import os
import os.path as op

# Personnal settings
LOGIN = 'lerouerw'

# Directory settings
DOCUMENTS = '/home/{}/Documents'.format(LOGIN)
PROJECT_PATH = os.path.join(DOCUMENTS, 'runtools')
LINK_PATH = op.join(DOCUMENTS, 'links')
OARSUB_DIRNAME = os.path.join(LINK_PATH, 'oarsub')
SCRIPT_DIRNAME = os.path.join(LINK_PATH, 'script')

# Cluster settings
MACHINE = 'dahu.ciment'
GPU_MACHINE = 'edgar'
MAX_DEFAULT_JOBS = {GPU_MACHINE: 2, MACHINE: 10}


