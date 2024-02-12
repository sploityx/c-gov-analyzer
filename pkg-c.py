#!/usr/bin/env python3

from utils import read_msr

MSR_PKG_C2_RESIDENCY = 0x60D
MSR_PKG_C3_RESIDENCY = 0x3F8
MSR_PKG_C6_RESIDENCY = 0x3F9
MSR_PKG_C7_RESIDENCY = 0x3FA


def main():
    pc2 = read_msr(MSR_PKG_C2_RESIDENCY)
    pc3 = read_msr(MSR_PKG_C3_RESIDENCY)
    pc6 = read_msr(MSR_PKG_C6_RESIDENCY)
    pc7 = read_msr(MSR_PKG_C7_RESIDENCY)

if __name__ == '__main__':
    main()
