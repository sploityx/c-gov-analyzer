#!/usr/bin/python3

import os
import subprocess
import argparse
from pathlib import Path
from utils import exec_cmd

SCRIPT_OUTPUT_NAME = "idle-governor-events.txt"
RES_OUTPUT_NAME = "c-state-idle-residency.json"
PKG_OUTPUT_NAME = "stat-data.json"
SYS_PATH = "/sys/devices/system/cpu/cpuidle/"

def switch_gov(gov: str):
    '''Switches the Idle Governor of a System to gov'''
    cmd = f"echo {gov} | sudo tee /sys/devices/system/cpu/cpuidle/current_governor"
    print(f"{os.path.basename(__file__)} will execute \"{cmd}\" now")
    subprocess.run(cmd, shell=True, check=True)

def avail_pkg_cstates():
    ''' Returns the available pkg-residencies'''
    pkg_path = '/sys/devices/cstate_pkg/events/'
    event = os.listdir(pkg_path)
    pkg_names = [f'cstate_pkg/{e}/'for e in event]
    pkg_names = ','.join(pkg_names)
    return pkg_names

def get_perf_idle_samples(gov: str, workload: str, cpu: int, power: str, pkg : bool):
    '''Uses perf to get recordings of task events while executing workload'''
    cmds = []
    if pkg:
        pkg_cstates = avail_pkg_cstates()
        perf_stat = f'sudo perf stat -j -o {PKG_OUTPUT_NAME} -e {pkg_cstates},power/energy-pkg/,power/energy-cores/ -C{cpu} -- '
    perf_rec = (f'sudo perf record -C {cpu} '
    '-e sched:sched_switch,power:cpu_frequency,power:cpu_idle,irq:irq_handler_entry,'
    'timer:hrtimer_cancel,power:cpu_idle_miss '
    f'-o {gov}/perf.data -- {workload}')
    if pkg:
        cmds.append(perf_stat + perf_rec)
    else:
        cmds.append(perf_rec)
    cmds.append(f"sudo chown {os.getuid()}:{os.getgid()} {gov}/perf.data")
    cmds.append(f"perf script -i {gov}/perf.data -s {power} -- "
        "--mode idle-governor --file-out")
    cmds.append(f"mv {SCRIPT_OUTPUT_NAME} {gov}/{SCRIPT_OUTPUT_NAME}")
    cmds.append(f"mv {RES_OUTPUT_NAME} {gov}/{RES_OUTPUT_NAME}")
    if pkg:
        cmds.append(f"mv -f {PKG_OUTPUT_NAME} {gov}/{PKG_OUTPUT_NAME}")
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
    parser.add_argument('-e', '--extended', help='Include C-State for Package Level and Energy Information',
                        default = False, action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    cpu = args.cpu
    power = args.power
    extended = args.extended
    workload = f'taskset --cpu-list {cpu} ./{args.workload}'
    with open(SYS_PATH + "available_governors", encoding='utf-8') as avail_file:
        avail_gov = avail_file.read().split()
    with open(SYS_PATH + "current_governor", encoding='utf-8') as cur_file:
        used_gov = cur_file.read().strip()
    try:
        for gov in avail_gov:
            Path(gov).mkdir(parents=True, exist_ok=True)
            get_perf_idle_samples(gov, workload, cpu, power, extended)
    finally:
        print(f"Switching back to original Idle Governor: {used_gov}")
        switch_gov(used_gov)

if __name__ == "__main__":
    main()
