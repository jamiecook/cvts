#!/bin/bash

eval `python ../cvts/settings.py`
umask 222
cp README-work-folder.md "$CVTS_WORK_PATH"/README.md
cp README-config-folder.md "$CVTS_CONFIG_PATH"/README.md
cp README-output-folder.md "$CVTS_OUT_PATH"/README.md
