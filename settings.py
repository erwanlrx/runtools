import os

# Personnal settings
EMAIL = 'erwan.le-roux@inria.fr'
LOGIN = 'erleroux'
MACHINE = 'aquarius'

# Directory settings
HOME = '/home/lear/erleroux'
OAR_DIRNAME = os.path.join(HOME, 'OAR')
OARSUB_DIRNAME = os.path.join(OAR_DIRNAME, 'oarsub')
SCRIPT_DIRNAME = os.path.join(OAR_DIRNAME, 'script')

# INRIA settings
CPU_MACHINE = 'clear'
GPU_MACHINE = 'edgar'
MAX_DEFAULT_JOBS = {GPU_MACHINE: 1, CPU_MACHINE: 10}


