#!/usr/bin/python
# Try code translator from python
# Interleave machine instructions (from LLVM) and microcode (from QDIS)
from __future__ import print_function, unicode_literals, division, absolute_import
import sys, os
sys.path.append(os.path.abspath('..'))
from ctypes import c_ubyte, create_string_buffer, cast, POINTER, byref
import qdis
from qdis.format import format_inst
import sys

if __name__ == '__main__':
    STYLE_ADDR = '\033[38;5;226m'
    STYLE_COLON = '\033[38;5;244m'
    STYLE_RESET = '\033[0m'

    d = qdis.Disassembler(qdis.TGT_ARM, None)

    f = open(sys.argv[1], 'rb')
    base = 0x0
    #base = 0x142e8
    f.seek(base)
    instructions = f.read(4096)

    offset = 0
    pc = base
    while offset < len(instructions):
        print ((STYLE_ADDR+'%08x'+STYLE_COLON+':'+STYLE_RESET) % (pc+offset))
        flags = qdis.INST_ARM_VFPEN_MASK
        result = d.disassemble(instructions[offset:offset+qdis.MAX_INST_SIZE], pc + offset, flags)

        for i in result.ops:
            if i.opcode == qdis.OP_END:
                continue
            print('  '+format_inst(d,i,result.syms))

        offset += 4

