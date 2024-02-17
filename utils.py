#!/usr/bin/env python3
import os
import shlex
import subprocess


def exec_cmd(cmd: str, shell=False):
    cmd = shlex.split(cmd)
    print(f"{os.path.basename(__file__)} will execute \"{cmd}\" now")
    subprocess.run(cmd, shell=shell, check=True)


# need sudo rights to access msr device
def read_msr(msr, cpu=0):
    msr_f = os.open(f'/dev/cpu/{cpu}/msr', os.O_RDONLY)
    os.lseek(msr_f, msr, os.SEEK_SET)
    msr_val = os.read(msr_f, 8)
    return int.from_bytes(msr_val, byteorder='little')
