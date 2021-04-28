import os

WORK_PATH       = os.path.sep + os.path.join('datasets', 'work', 'lw-cvts', 'work')
BOUNDARIES_PATH = os.path.join(WORK_PATH, 'boundaries')
RAW_PATH        = os.path.join(WORK_PATH, 'raw')
CONFIG_PATH     = os.path.join(WORK_PATH, 'config')
OUT_PATH        = os.path.join(WORK_PATH, 'output')
SEQ_PATH        = os.path.join(OUT_PATH,  'seq')
MM_PATH         = os.path.join(OUT_PATH,  'mm')
STOP_PATH       = os.path.join(OUT_PATH,  'stop')
SRC_DEST_PATH   = os.path.join(OUT_PATH,  'src_dest')

VALHALLA_CONFIG_FILE = os.path.join(CONFIG_PATH, 'valhalla.json')

DEBUG = False

for p in (CONFIG_PATH, OUT_PATH, SEQ_PATH, MM_PATH, STOP_PATH, SRC_DEST_PATH):
    if not os.path.exists(p):
        os.makedirs(p)

if __name__ == '__main__':
    # this won't work on windows
    print(';'.join('export CVTS_{}={}'.format(v, eval(v)) for v in (
        'WORK_PATH',
        'BOUNDARIES_PATH',
        'RAW_PATH',
        'CONFIG_PATH',
        'OUT_PATH',
        'SEQ_PATH',
        'MM_PATH',
        'STOP_PATH',
        'SRC_DEST_PATH',
        'VALHALLA_CONFIG_FILE')))
