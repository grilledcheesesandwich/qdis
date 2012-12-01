'''
Higher-level Python wrapper for the disass functions.
'''
from __future__ import print_function, unicode_literals, division, absolute_import
from ctypes import c_ubyte, create_string_buffer, cast, POINTER, byref
from qdis import _qdis

def import_qdis_symbols():
    '''Take constants from _qdis, strip prefix'''
    import sys
    g = sys.modules[__name__]
    prefixes = ['QDIS_']
    for name in dir(_qdis):
        for prefix in prefixes:
            if name.startswith(prefix):
                setattr(g, name[len(prefix):], getattr(_qdis, name))

import_qdis_symbols()

# Buffer to store microcode instructions
OutbufferType = c_ubyte * BUFFER_SIZE

# maximum expected size of one instruction
MAX_INST_SIZE = 64

class Instruction(object):
    def __init__(self, opcode, args):
        self.opcode = opcode
        self.args = args

class Block(object):
    def __init__(self, ops, syms, labels, text):
        # list of all instructions in this block
        self.ops = ops
        # list of symbols (temps/locals)
        self.syms = syms
        # list of indices into ops array for labels
        self.labels = labels
        # original machine instruction formatted as text
        # if OPTIMIZE_NOTEXT was not provided
        self.text = text

class Disassembler(object):
    def __init__(self, tgt, features=None):
        self.dis = _qdis.qdis_Create(tgt, features)
        self.outbuffer = OutbufferType()

    def disassemble(self, inst, pc, flags, optimize=OPTIMIZE_FULL):
        '''
        inst: binary instruction
        pc: current pc
        flags: instruction flags
        optimize: microcode optimization flags
        '''
        inst_buf = create_string_buffer(inst, len(inst))

        result = _qdis.qdis_Disassemble(self.dis, inst_buf, len(inst_buf), pc, flags, optimize,
                self.outbuffer, len(self.outbuffer))

        if result != OK:
            if result == ERR_OUT_OF_BOUNDS_ACCESS:
                raise IndexError('Out of bounds access')
            raise Exception('Disassembly error %i' % result)

        data = cast(self.outbuffer, POINTER(_qdis.QDisResult)).contents
        argptr = 0
        instructions = []
        labels = [None] * data.num_labels
        for idx in xrange(data.num_ops):
            op = data.ops[idx]
            if op.opcode == OP_SET_LABEL:
                labels[data.args[argptr].value] = len(instructions)
            instructions.append(Instruction(op.opcode, data.args[argptr:argptr+op.args]))
            argptr += op.args
        return Block(instructions, data.syms[0:data.num_syms], labels, data.text)

    def lookup_name(self, infotype, x):
        '''
        Look up token name.
        '''
        rv = _qdis.qdis_LookupName(self.dis, infotype, x)
        if rv.data is None:
            return None
        else:
            return str(rv.data)

    def lookup_value(self, infotype, x):
        '''
        Get value from Disassembler object.
        '''
        return _qdis.qdis_LookupValue(self.dis, infotype, x)
