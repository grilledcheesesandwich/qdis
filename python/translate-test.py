#!/usr/bin/python
# Try code translator from python
from __future__ import print_function, unicode_literals, division, absolute_import
from ctypes import c_ubyte, create_string_buffer, cast, POINTER, byref
import qdis
from disassembler import Disassembler,MAX_INST_SIZE,format_inst

if __name__ == '__main__':
    STYLE_ADDR = '\033[38;5;226m'
    STYLE_COLON = '\033[38;5;244m'
    STYLE_RESET = '\033[0m'

    d = Disassembler(qdis.QDIS_TGT_ARM, None)

    f = open('test.so', 'rb')
    base = 0x12f80
    #base = 0x142e8
    f.seek(base)
    instructions = f.read(4096)

    offset = 0
    pc = base
    while offset < len(instructions):
        print ((STYLE_ADDR+'%08x'+STYLE_COLON+':'+STYLE_RESET) % (pc+offset))
        flags = qdis.QDIS_INST_ARM_VFPEN_MASK
        result = d.disassemble(instructions[offset:offset+MAX_INST_SIZE], pc + offset, flags)

        for i in result.ops:
            if i.opcode == qdis.QDIS_OP_END:
                continue
            print('  '+format_inst(d,i,result.syms))

        offset += 4

