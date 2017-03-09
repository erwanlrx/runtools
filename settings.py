# TODO: Use the same argument reader as in Tensorflow to read the arguments

personnal_settings = {
    'EMAIL': 'erwan.le-roux@inria.fr',
    'MACHINE': 'aquarius',
    'HOME': '/home/lear/erleroux',
    'LOGIN': 'erleroux',
    'OAR_DIRNAME': 'OAR',
    'SCRIPT_DIRNAME': 'script',
    'OARSUB_DIRNAME': 'oarsub'
}

inria_settings = {
    'CPU_MACHINE': 'clear',
    'GPU_MACHINE': 'edgar'

}

# General settings dictionnary
settings = dict()
settings.update(personnal_settings)
settings.update(inria_settings)


