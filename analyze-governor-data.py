#!/usr/bin/env python3
""" Analyze Governor

This script requires the input of collect-governor-data.py
It then creates graphs for each governor with the post processing visualizations.


USAGE:

Call this script after collect-governor-data.py and using:
    ./analyze-governor-data.py
"""

from pathlib import Path
import argparse
import os
import shutil
import utils

DATA_FILE = 'idle-governor-events.txt'
JSON_FILE = 'c-state-idle-residency.json'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Visualizes data from collect-governor-data.py')
    parser.add_argument('-g', '--governor', help='Specify concrete governor to analyze')
    parser.add_argument('-v', '--visualization', help='Specify location of visualization dir')
    args = parser.parse_args()
    govs = args.governor
    vis = args.visualization
    if govs is None:
        govs = [f for f in os.listdir('.') if os.path.isdir(f) and not f.startswith(('__', '.'))]
    print('Backing up old files')
    if os.path.isfile(f'{vis}/{DATA_FILE}'):
        utils.exec_cmd(f'mv {vis}/{DATA_FILE} {vis}/{DATA_FILE}.old')
    if os.path.isfile(f'{vis}/{JSON_FILE}'):
        utils.exec_cmd(f'mv {vis}/{JSON_FILE} {vis}/{JSON_FILE}.old')
    for gov in govs:
        utils.exec_cmd(f'cp {gov}/{DATA_FILE} {vis}/{DATA_FILE}')
        utils.exec_cmd(f'cp {gov}/{JSON_FILE} {vis}/{JSON_FILE}')
        utils.exec_cmd(f'make -C {vis}')
        if os.path.isdir(vis + '/' + gov):
            shutil.rmtree(vis + '/' + gov)
        Path(vis + '/' + gov).mkdir(parents=True, exist_ok=True)
        utils.exec_shell_cmd(f'mv {vis}/*.png {vis}/{gov}/')
        utils.exec_cmd(f'mv {vis}/scatter {vis}/{gov}/')
