#!/usr/bin/python
'''
Test concrete execution (emulation) of code fragment to 
decode a message.
Sooper slow, but just a proof of concept and baseline for 
more advanced evaluators.

Usage:
    concrete_eval_test.py

'''
from __future__ import print_function, unicode_literals, division, absolute_import
import sys, os
sys.path.append(os.path.abspath('..'))

import qdis
from qdis.format import format_inst
import mmap
from binascii import a2b_hex, b2a_hex

import concrete_eval

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

def hex_or_bottom(x):
    if x is None:
        return BOTTOM
    else:
        return '%x' % x

def main():
    # Show stores to globals (registers)
    concrete_eval.trace_global_stores = False
    # Show stores to temps and locals
    concrete_eval.trace_temp_stores = False
    # Show stored to memory
    concrete_eval.trace_mem_stores = True#False
    # Show all microcode for disassembled instructions
    concrete_eval.trace_microcode = True#False
    # Show warnings (non-implemented microcode instructions etc)
    concrete_eval.show_warnings = True#False

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
        '''Custom tracing function'''
        if addr==concrete_eval.TRACE_INSTRUCTION:
            print ('  '+STYLE_MICRO+format_inst(qd,value,result.syms)+STYLE_RESET)
        else:
            if isinstance(addr, tuple): # memory
                if addr[0] is None:
                    addr = '[%s:%i]' % (BOTTOM,addr[1])
                else:
                    addr = '[%x:%i]' % addr
            print('  %s%s%s = %s%s%s' % (STYLE_EXPR_TGT, addr, STYLE_RESET, STYLE_EXPR, format_value(value), STYLE_RESET))
    def warning(msg):
        if concrete_eval.show_warnings:
            print('  ' + STYLE_WARNING_HEAD + 'Warning' + STYLE_RESET + ' ' + STYLE_WARNING_MSG + msg + STYLE_RESET)

    qd = qdis.Disassembler(qdis.TGT_ARM, None)
    
    args_image = 'dat/test.bin'

    f = open(args_image, 'rb')
    code = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)

    ev = concrete_eval.ConcreteEval(qd)
    ev.trace_func = expr_trace
    ev.warning_func = warning

    data_in = a2b_hex('53c80c448c5317ab4a49')  
    ev.state.add_memory(0x00000000, 0x00100000, code)
    ev.state.add_memory(0x60000000, 0x00100000, data_in)

    # use a unique return address so that we know when to exit
    # from the emulator
    RETURN_ADDRESS = 0xfffffff0

    ev.set_globals({
        'r0': 0x60000000, # input address
        'r1': 0x60001000, # output address
        'r2': len(data_in),  # data length
        'r13': 0x600ffffc, # set up stack
        'r14': RETURN_ADDRESS # return address token
        })

    pc = 0x714 # starting PC
    flags = qdis.IFLAGS_DEFAULT_ARM # qdis.IFLAGS_DEFAULT_THUMB

    visited = set()
    while pc is not None and pc != RETURN_ADDRESS:
        if not is_valid_pc(pc, flags):
            print('Warning: PC %08x is invalid with iflags %08x' % (pc,flags))
            break

        visited.add(pc)

        instdata = code[pc:pc+qdis.MAX_INST_SIZE]
        
        result = qd.disassemble(instdata, pc, flags)
        
        print ("%s%08x%s: %s%s %s%s" % (STYLE_ADDR,pc,STYLE_COLON,STYLE_RESET,
            STYLE_INST, result.inst_text, STYLE_RESET))

        (pc, flags) = ev.start_block(result, pc, flags)

    print()
    print('Visited addresses:')
    for addr in sorted(visited):
        print('  %08x' % addr)

    data_out = ev.state.get_memory(0x60001000, len(data_in))
    print()
    print(' Output:', data_out, '['+b2a_hex(data_out)+']')
    assert(str(data_out) == "We're here")
    f.close()

if __name__ == '__main__':
    main()

