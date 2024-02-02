#!/usr/bin/python3

import os
import subprocess
from pathlib import Path

def exec_cmd(cmd):
    print(f"{os.path.basename(__file__)} will execute \"{cmd}\" now")
    subprocess.run(cmd, shell=True, check=True)

def switch_gov(gov):
    cmd = f"echo {gov} | sudo tee /sys/devices/system/cpu/cpuidle/current_governor"
    print(f"{os.path.basename(__file__)} will execute \"{cmd}\" now")
    subprocess.run(cmd, shell=True, check=True)


def get_perf_idle_samples(gov, workload):
    SCRIPT_OUTPUT_NAME = "idle-governor-events.txt"
    RES_OUTPUT_NAME = "c-state-idle-residency.json"
    POWER_STAT = '~/Worky/PM/linux-kernel-perf/tools/perf/scripts/python/power-statistics.py'
    cmd = f"sudo perf record -a -e sched:sched_switch,power:cpu_frequency,power:cpu_idle,irq:irq_handler_entry,timer:hrtimer_cancel,power:cpu_idle_miss -o {gov}/perf.data -- {workload}"
    exec_cmd(cmd)
    cmd = f"sudo chown {os.getuid()}:{os.getgid()} {gov}/perf.data"
    exec_cmd(cmd)
    cmd = f"perf script -i {gov}/perf.data -s {POWER_STAT} -- --mode idle-governor --csv --file-out"
    exec_cmd(cmd)
    cmd = f"mv {SCRIPT_OUTPUT_NAME} {gov}/{SCRIPT_OUTPUT_NAME}"
    exec_cmd(cmd)
    cmd = f"mv {RES_OUTPUT_NAME} {gov}/{RES_OUTPUT_NAME}"
    exec_cmd(cmd)

SYS_PATH = "/sys/devices/system/cpu/cpuidle/"

def main():
    workload = 'python3 /home/woody/Worky/PM/asset_aq/perf-power-analyzer-post/assets/mini-bench-cpu.py'
    with open(SYS_PATH + "available_governors") as avail_file:
        avail_gov = avail_file.read().split()
    with open(SYS_PATH + "current_governor") as cur_file:
        used_gov = cur_file.read().strip()
    try:
        for gov in avail_gov:
            Path(gov).mkdir(parents=True, exist_ok=True)
            get_perf_idle_samples(gov, workload)
    finally:
        print(f"Switching back to original Idle Governor: {used_gov}")
        switch_gov(used_gov)

if __name__ == "__main__":
    main()
