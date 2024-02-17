#!/usr/bin/env python3
""" Analyze Governor

This script requires the input of collect-governor-data.py
It then creates graphs for each governor with the post processing visualizations.


USAGE:

Call this script after collect-governor-data.py and using:
    ./analyze-governor-data.py -v {PATH_TO_VIS}

Example:
    ./analyze-governor-data.py -v ../perf-power-analyzer-post/images/idle-governor
"""

from pathlib import Path
import argparse
import os
import shutil
import utils

DATA_FILE = 'idle-governor-events.txt'
RES_FILE = 'c-state-idle-residency.json'
PKG_FILE = 'pkg-c-state.json'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Visualizes data from collect-governor-data.py')
    parser.add_argument('-g', '--governor', help='Specify concrete governor to analyze')
    parser.add_argument('-v', '--visualization', help='Specify location of visualization dir')
    parser.add_argument('-e', '--extended', help='Include C-State for Package Level',
                        default = False, action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    govs = args.governor
    vis = args.visualization
    extended = args.extended
    if govs is None:
        govs = [f for f in os.listdir('.') if os.path.isdir(f) and not f.startswith(('__', '.'))]
    print('Backing up old files')
    files = [DATA_FILE, RES_FILE]
    if extended:
        files.append(PKG_FILE)
    for file in files:
        utils.exec_cmd(f'mv {vis}/{file} {vis}/{file}.old')
    for gov in govs:
        for file in files:
            utils.exec_cmd(f'cp {gov}/{file} {vis}/{file}')
        utils.exec_cmd(f'make -C {vis}')
        if os.path.isdir(vis + '/' + gov):
            shutil.rmtree(vis + '/' + gov)
        Path(vis + '/' + gov).mkdir(parents=True, exist_ok=True)
        utils.exec_cmd(f'mv {vis}/*.png {vis}/{gov}/', shell=True)
        utils.exec_cmd(f'mv {vis}/scatter {vis}/{gov}/')
