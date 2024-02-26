#!/usr/bin/env python3
import glob
import os
import re
import shlex
import subprocess
import shutil


def exec_cmd(cmd: str, shell=False):
    cmd = shlex.split(cmd)
    print(f"{os.path.basename(__file__)} will execute \"{cmd}\" now")
    subprocess.run(cmd, shell=shell, check=True)


def mv_wildcard(source_folder : str, target_folder : str, wildcard : str):
    try:
        for file_path in glob.glob(f'{source_folder}/{wildcard}'):
            shutil.move(file_path, target_folder)
    except shutil.Error as exception:
        print(f'Error moving wildcard files: {exception}')


# need sudo rights to access msr device
def read_msr(msr, cpu=0):
    msr_f = os.open(f'/dev/cpu/{cpu}/msr', os.O_RDONLY)
    os.lseek(msr_f, msr, os.SEEK_SET)
    msr_val = os.read(msr_f, 8)
    return int.from_bytes(msr_val, byteorder='little')

def cstate_key(cstate):
    '''Alphanumeric sort for C-States'''
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', str(cstate))]
