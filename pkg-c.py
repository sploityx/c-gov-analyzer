#!/usr/bin/env python3

from utils import read_msr
from utils import exec_cmd
from time import sleep
import os

MSR_PKG_C2_RESIDENCY = 0x60D
MSR_PKG_C3_RESIDENCY = 0x3F8
# If retention mode is activated, this counter does not increment
MSR_PKG_C6_RESIDENCY = 0x3F9
MSR_PKG_C7_RESIDENCY = 0x3FA

# MSR to test if any meaningful data can be gathered
MSR_PKG_POWER_INFO = 0x614
"""
MSR_PKG_ENERGY_STATUS
MSR_DRAM_ENERGY_STATUS
MSR_PP0_ENERGY_STATUS
MSR_PP1_ENERGY_STATUS
MSR_PLATFORM_ENERGY_STATUS
MSR_PKG_C8_RESIDENCY
MSR_PKG_C9_RESIDENCY
MSR_PKG_C10_RESIDENCY
"""

def output_pkg_c(file_name):
    c2_pkg = read_msr(MSR_PKG_C2_RESIDENCY)
    c3_pkg = read_msr(MSR_PKG_C3_RESIDENCY)
    c6_pkg = read_msr(MSR_PKG_C6_RESIDENCY)
    c7_pkg = read_msr(MSR_PKG_C7_RESIDENCY)
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(f'PKG C2: {c2_pkg}\n')
        file.write(f'PKG C3: {c3_pkg}\n')
        file.write(f'PKG C6: {c6_pkg}\n')
        file.write(f'PKG C7: {c7_pkg}\n')

def calc_pkg_dif(file_out, file_fst, file_scnd):
    if os.path.exists(file_out):
        os.remove(file_out)
    with open(file_fst, 'r', encoding='utf-8') as fst:
        with open(file_scnd, 'r', encoding='utf-8') as scnd:
            for (fst_line, scnd_line) in zip(fst, scnd):
                with open(file_out, 'a', encoding='utf-8') as out:
                    out.write(fst_line.split()[0] + ' ' + fst_line.split()[1] + ' ')
                    out.write(str(int(scnd_line.split()[-1]) - int(fst_line.split()[-1])))
                    out.write('\n')


def main():
    for i in range(0,10):
        output_pkg_c(f'pkg-c-start-{i}.txt')
        sleep(5)
        output_pkg_c(f'pkg-c-end-{i}.txt')
        calc_pkg_dif(f'pkg-c-{i}.txt', f'pkg-c-start-{i}.txt', f'pkg-c-end-{i}.txt')

if __name__ == '__main__':
    main()
