#!/usr/bin/env python3
import os
import shlex
import subprocess

def exec_cmd(cmd: str):
    cmd = shlex.split(cmd)
    print(f"{os.path.basename(__file__)} will execute \"{cmd}\" now")
    subprocess.run(cmd, check=True)

def exec_shell_cmd(cmd: str):
    print(f"{os.path.basename(__file__)} will execute \"{cmd}\" now")
    subprocess.run(cmd, shell=True, check=True)
