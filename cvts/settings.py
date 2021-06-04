import os

DEBUG = False

def _get_path(var, must_exist=False):
    path = os.environ.get(
        'CVTS_{}_PATH'.format(var.upper()),
        os.path.join(WORK_PATH, var))

    if must_exist and not os.path.isdir(path):
        raise Exception('raw data directory ({}) does not exist'.format(path))

    return path

#: Default root directory
WORK_PATH       = os.environ.get(
    'CVTS_WORK_PATH', os.path.join(os.path.expanduser("~"), '.cvts'))
RAW_PATH        = _get_path('raw', True)
BOUNDARIES_PATH = _get_path('boundaries')
CONFIG_PATH     = _get_path('config')
OUT_PATH        = _get_path('output')

SEQ_PATH        = os.path.join(OUT_PATH, 'seq')
MM_PATH         = os.path.join(OUT_PATH, 'mm')
STOP_PATH       = os.path.join(OUT_PATH, 'stop')
SRC_DEST_PATH   = os.path.join(OUT_PATH, 'src_dest')
SPEED_PATH      = os.path.join(OUT_PATH, 'speed')

VALHALLA_CONFIG_FILE = os.path.join(CONFIG_PATH, 'valhalla.json')

for p in (CONFIG_PATH, OUT_PATH, SEQ_PATH, MM_PATH, STOP_PATH, SRC_DEST_PATH, SPEED_PATH):
    if not os.path.exists(p):
        os.makedirs(p)

if __name__ == '__main__':
    # this won't work on windows
    print(';'.join('export CVTS_{}={}'.format(v, eval(v)) for v in (
        'WORK_PATH',
        'RAW_PATH',
        'BOUNDARIES_PATH',
        'CONFIG_PATH',
        'OUT_PATH',
        'SEQ_PATH',
        'MM_PATH',
        'STOP_PATH',
        'SRC_DEST_PATH',
        'SPEED_PATH',
        'VALHALLA_CONFIG_FILE')))
