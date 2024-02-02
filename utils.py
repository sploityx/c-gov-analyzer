#!/usr/bin/env python3
import os
import subprocess

def exec_cmd(cmd: str):
    print(f"{os.path.basename(__file__)} will execute \"{cmd}\" now")
    subprocess.run(cmd, shell=True, check=True)
