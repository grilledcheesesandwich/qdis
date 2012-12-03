#!/usr/bin/python
'''
Show tcg code for helper function.
'''
from __future__ import print_function, unicode_literals, division, absolute_import
import sys, os
sys.path.append(os.path.abspath('..'))

import functools # for partial
import argparse
from binascii import b2a_hex
import qdis
from qdis.format import format_inst

def print_func(name, qd, result):
    print('[%s]' % name)
    ptr = 0
    while ptr < len(result.ops):
        i = result.ops[ptr]
        print ('  '+format_inst(qd,i,result.syms))
        ptr += 1
    print()

def main():
    qd = qdis.Disassembler(qdis.TGT_ARM, None)
    print_func('get_tb_cpu_state', qd, qd.get_helper(qdis.HELPER_GET_TB_CPU_STATE))
    print_func('get_cpu_state_tb', qd, qd.get_helper(qdis.HELPER_GET_CPU_STATE_TB))

if __name__ == '__main__':
    main()
