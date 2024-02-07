#!/usr/bin/python3

import os
import subprocess
import argparse
from pathlib import Path
from utils import exec_cmd

SCRIPT_OUTPUT_NAME = "idle-governor-events.txt"
RES_OUTPUT_NAME = "c-state-idle-residency.json"
SYS_PATH = "/sys/devices/system/cpu/cpuidle/"

def switch_gov(gov: str):
    '''Switches the Idle Governor of a System to gov'''
    cmd = f"echo {gov} | sudo tee /sys/devices/system/cpu/cpuidle/current_governor"
    print(f"{os.path.basename(__file__)} will execute \"{cmd}\" now")
    subprocess.run(cmd, shell=True, check=True)


def get_perf_idle_samples(gov: str, workload: str, cpu: int, power: str):
    '''Uses perf to get recordings of task events while executing workload'''
    cmds = []
    cmds.append(f'sudo perf record -C {cpu} '
    '-e sched:sched_switch,power:cpu_frequency,power:cpu_idle,irq:irq_handler_entry,'
    'timer:hrtimer_cancel,power:cpu_idle_miss '
    f'-o {gov}/perf.data -- {workload}')
    cmds.append(f"sudo chown {os.getuid()}:{os.getgid()} {gov}/perf.data")
    cmds.append(f"perf script -i {gov}/perf.data -s {power} -- "
        "--mode idle-governor --file-out")
    cmds.append(f"mv {SCRIPT_OUTPUT_NAME} {gov}/{SCRIPT_OUTPUT_NAME}")
    cmds.append(f"mv {RES_OUTPUT_NAME} {gov}/{RES_OUTPUT_NAME}")
    for cmd in cmds:
        exec_cmd(cmd)

def main():
    '''Applies a workload to a core, while recording the perf events'''
    parser = argparse.ArgumentParser(description='Records perf data from available Idle Governors.')
    parser.add_argument('-w', '--workload', help='Specify workload file (e.g. mini-bench-cpu.py)',
                        required=True)
    parser.add_argument('-c', '--cpu', help='Core to run workload and record perf data',
                        required=True)
    parser.add_argument('-p', '--power', help='Point to Power-Stat module power-statistics.py',
                        required=True)
    args = parser.parse_args()
    cpu = args.cpu
    power = args.power
    workload = f'taskset --cpu-list {cpu} ./{args.workload}'
    with open(SYS_PATH + "available_governors", encoding='utf-8') as avail_file:
        avail_gov = avail_file.read().split()
    with open(SYS_PATH + "current_governor", encoding='utf-8') as cur_file:
        used_gov = cur_file.read().strip()
    try:
        for gov in avail_gov:
            Path(gov).mkdir(parents=True, exist_ok=True)
            get_perf_idle_samples(gov, workload, cpu, power)
    finally:
        print(f"Switching back to original Idle Governor: {used_gov}")
        switch_gov(used_gov)

if __name__ == "__main__":
    main()
