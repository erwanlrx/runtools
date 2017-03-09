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
GPU_MAX_DEFAULT_JOBS = 2


