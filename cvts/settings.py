import os

WORK_PATH = os.path.sep + os.path.join('datasets', 'work', 'lw-cvts', 'work')
RAW_PATH = os.path.join(WORK_PATH, 'raw')
OUT_PATH = os.path.join(WORK_PATH, 'output')
CONFIG_PATH = os.path.join(WORK_PATH, 'config')
MM_PATH = os.path.join(OUT_PATH, 'mm')
SEQ_PATH = os.path.join(OUT_PATH, 'seq')
BOUNDARIES_PATH = os.path.join(WORK_PATH, 'boundaries')

VALHALLA_CONFIG_FILE = os.path.join(WORK_PATH, 'config', 'valhalla.json')

DEBUG = False

for p in (OUT_PATH, CONFIG_PATH, MM_PATH, SEQ_PATH):
    if not os.path.exists(p):
        os.makedirs(p)

if __name__ == '__main__':
    # this won't work on windows
    print(';'.join('export CVTS_{}={}'.format(v, eval(v)) for v in (
        'WORK_PATH',
        'RAW_PATH',
        'OUT_PATH',
        'CONFIG_PATH',
        'MM_PATH',
        'SEQ_PATH',
        'BOUNDARIES_PATH',
        'VALHALLA_CONFIG_FILE')))
