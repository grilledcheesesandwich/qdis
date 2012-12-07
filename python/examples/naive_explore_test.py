#!/usr/bin/python
'''
Explore an executable naively, ie without doing any symbolic evaluation
or jump table interpolation. Just follow jumps and calls from a provided
entry point, and keep track of what was visited.

Usage:
    naive_explore_test.py binary.dat 0x12345 (arm|thumb)

'''
from __future__ import print_function, unicode_literals, division, absolute_import
import sys, os
sys.path.append(os.path.abspath('..'))
import functools # for partial
import argparse
import mmap
from binascii import b2a_hex
import qdis
from qdis.format import format_inst
import naive_explore
from naive_explore import UNDEFINED,TRACE_INSTRUCTION

STYLE_ADDR = '\033[38;5;226m'
STYLE_COLON = '\033[38;5;244m'
STYLE_MICRO = '\033[38;5;248m'
STYLE_INST = '\033[38;5;179m'
STYLE_WARNING_HEAD = '\033[48;5;196;38;5;232m'
STYLE_WARNING_MSG = '\033[38;5;167m'
STYLE_EXPR_TGT = '\033[38;5;93m'
STYLE_EXPR = '\033[38;5;105m'
STYLE_RESET = '\033[0m'

BOTTOM = '\u22A5' # used as undefined character

# Show debug information after processing instruction
show_debug = False

def is_valid_pc(pc, iflag):
    '''
    Check if pc is a valid instruction location, given instruction flags
    iflag.
    XXX ARM specific, move this in to qdis.
    '''
    if iflag & qdis.INST_ARM_THUMB_MASK:
        return not (pc & 1)
    else:
        return not (pc & 3)

def main():
    parser = argparse.ArgumentParser(description='Scan binary for reachable instructions')
    parser.add_argument('image', metavar='IMAGE', help='Binary image to explore')
    parser.add_argument('pc', metavar='PC', help='Initial program counter')
    parser.add_argument('iflags', metavar='ISET', help='Instruction set')
    args = parser.parse_args()

    def format_value(value):
        if value is not None:
            return '%08x' % value
        else:
            return BOTTOM
    def format_pc_iflag(pc, iflag):
        'Format pc and new instruction flags pair'
        rv = format_value(pc)
        if iflag is not None:
            rv += '(%x)' % iflag
        else:
            rv += '('+BOTTOM+')'
        return rv
    def expr_trace(addr, value):
        '''Custom tracing func'''
        if addr==TRACE_INSTRUCTION:
            print ('  '+STYLE_MICRO+format_inst(qd,value,result.syms)+STYLE_RESET)
        else:
            print('  %s%s%s = %s%s%s' % (STYLE_EXPR_TGT, addr, STYLE_RESET, STYLE_EXPR, format_value(value), STYLE_RESET))
    def warning(msg):
        if naive_explore.show_warnings:
            print('  ' + STYLE_WARNING_HEAD + 'Warning' + STYLE_RESET + ' ' + STYLE_WARNING_MSG + msg + STYLE_RESET)

    # Default flags for ARM
    default_flags = {
        'arm': (qdis.TGT_ARM, qdis.IFLAGS_DEFAULT_ARM), 
        'thumb': (qdis.TGT_ARM, qdis.IFLAGS_DEFAULT_THUMB)
    }

    qd = qdis.Disassembler(default_flags[args.iflags][0], None)
    f = open(args.image, 'rb')
    code = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)

    ev = naive_explore.NaiveEval(qd)
    ev.trace_func = expr_trace
    ev.warning_func = warning

    pc = int(args.pc,0)
    flags = default_flags[args.iflags][1]

    visited = set()
    # list of states
    worklist = []
    in_worklist = set() # set of pcs in worklist
    # add first instruction to work list
    worklist.append((pc,flags))
    in_worklist.add(pc)
    while worklist:
        pc,flags = worklist.pop()
        in_worklist.remove(pc)

        if not is_valid_pc(pc, flags):
            print('Warning: PC %08x is invalid with iflags %08x' % (pc,flags))
            continue

        visited.add(pc)

        instdata = code[pc:pc+qdis.MAX_INST_SIZE]
        
        result = qd.disassemble(instdata, pc, flags)
        
        print ("%s%08x%s: %s%s %s" % (STYLE_ADDR,pc,STYLE_COLON,STYLE_RESET,
            STYLE_INST, result.inst_text))
        #print(result.inst_type, result.inst_size, result.inst_text)

        pcs_out = ev.start_block(result, pc, flags)
        is_call = result.inst_type in [qdis.ITYPE_CALL, qdis.ITYPE_CALL_IND]
        is_return = result.inst_type in [qdis.ITYPE_RET]
        if is_call:
            # In case of a call, continue after instruction
            # Assume instruction flags are the same upon return
            pcs_out.add((pc + result.inst_size, flags))

        if show_debug:
            print('New PCs: %s' % (' '.join([format_pc_iflag(x, iflag) for x,iflag in pcs_out])))
            print('is_call %i is_return %i' % (is_call, is_return))
        
        # TODO: warn when exception or other strange helper
        unknown_jump_target = False
        # First defined PC
        for cand_pc,cand_iflag in pcs_out:
            if cand_pc is UNDEFINED:
                unknown_jump_target = True
            if cand_pc is not UNDEFINED and not cand_pc in visited and not cand_pc in in_worklist:
                worklist.append((cand_pc,cand_iflag))
                in_worklist.add(cand_pc)

        if unknown_jump_target and not is_return:
            print('One of jump targets is unknown')
        if show_debug:
            print()

    print()
    print('Visited addresses:')
    for addr in sorted(visited):
        print('  %08x' % addr)
    
    f.close()


if __name__ == '__main__':
    main()

