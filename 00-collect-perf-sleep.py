#!/usr/bin/python3

import os
import subprocess
from pathlib import Path

def switch_gov(gov):
    cmd = f"echo {gov} | sudo tee /sys/devices/system/cpu/cpuidle/current_governor"
    print(f"{os.path.basename(__file__)} will execute \"{cmd}\" now")
    subprocess.run(cmd, shell=True, check=True)


def get_perf_idle_samples(gov):
    cmd = f"sudo perf record -a -e sched:sched_switch,power:cpu_frequency,power:cpu_idle,irq:irq_handler_entry,timer:hrtimer_cancel,power:cpu_idle_miss -o {gov}/perf.data -- sleep 1"
    print(f"{os.path.basename(__file__)} will execute \"{cmd}\" now")
    subprocess.run(cmd, shell=True, check=True)
    cmd = f"sudo chown {os.getuid()}:{os.getgid()} {gov}/perf.data"
    subprocess.run(cmd, shell=True, check=True)
    cmd = f"perf script -i {gov}/perf.data -s ~/Worky/PM/Scripts/linux-kernel-perf/tools/perf/scripts/python/power-statistics.py -- --mode idle-governor > {gov}/idle.txt"
    print(f"{os.path.basename(__file__)} will execute \"{cmd}\" now")
    subprocess.run(cmd, shell=True, check=True)

SYS_PATH = "/sys/devices/system/cpu/cpuidle/"

def main():
    with open(SYS_PATH + "available_governors") as avail_file:
        avail_gov = avail_file.read().split()
    with open(SYS_PATH + "current_governor") as cur_file:
        used_gov = cur_file.read().strip()
    try:
        for gov in avail_gov:
            Path(gov).mkdir(parents=True, exist_ok=True)
            get_perf_idle_samples(gov)
    finally:
        print(f"Switching back to original Idle Governor: {used_gov}")
        switch_gov(used_gov)

if __name__ == "__main__":
    main()
