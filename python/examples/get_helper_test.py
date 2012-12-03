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

def main():
    qd = qdis.Disassembler(qdis.TGT_ARM, None)
    result = qd.get_helper(qdis.HELPER_GET_TB_CPU_STATE)
    ptr = 0
    while ptr < len(result.ops):
        i = result.ops[ptr]
        print ('  '+format_inst(qd,i,result.syms))
        ptr += 1

if __name__ == '__main__':
    main()
