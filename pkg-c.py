#!/usr/bin/env python3

from utils import read_msr
from utils import exec_cmd
from time import sleep
import os

MSR_PKG_C2_RESIDENCY = 0x60D
MSR_PKG_C3_RESIDENCY = 0x3F8
MSR_PKG_C6_RESIDENCY = 0x3F9
MSR_PKG_C7_RESIDENCY = 0x3FA

def output_pkg_c(file_name):
    c2_pkg = read_msr(MSR_PKG_C2_RESIDENCY)
    c3_pkg = read_msr(MSR_PKG_C3_RESIDENCY)
    c6_pkg = read_msr(MSR_PKG_C6_RESIDENCY)
    c7_pkg = read_msr(MSR_PKG_C7_RESIDENCY)
    if os.path.exists(file_name):
        exec_cmd(f'mv {file_name} {file_name}.old')
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(f'PKG C2: {c2_pkg}\n')
        file.write(f'PKG C3: {c3_pkg}\n')
        file.write(f'PKG C6: {c6_pkg}\n')
        file.write(f'PKG C7: {c7_pkg}\n')

def calc_pkg_dif(file_fst, file_scnd):
    with open(file_fst, 'r', encoding='utf-8') as fst:
        with open(file_scnd, 'r', encoding='utf-8') as scnd:
            for (fst_line, scnd_line) in zip(fst, scnd):
                print(fst_line.split()[0] + ' ' + fst_line.split()[1], end=' ')
                print(int(fst_line.split()[-1]) - int(scnd_line.split()[-1]))


def main():
    output_pkg_c('pkg-c.txt')
    sleep(5)
    output_pkg_c('pkg-c.txt')
    calc_pkg_dif('pkg-c.txt', 'pkg-c.txt.old')

if __name__ == '__main__':
    main()
