#!/usr/bin/python
'''
Concrete execution (emulation) of code fragment.
Sooper slow, but just a proof of concept.
'''
from __future__ import print_function, unicode_literals, division, absolute_import
import functools # for partial
import argparse
from binascii import b2a_hex
import qdis
from qdis.format import format_inst

UNDEFINED = None

TRACE_INSTRUCTION = 'inst'

# Show stores to globals
trace_global_stores = False
# Show stores to temps and locals
trace_temp_stores = False
# Show stored to memory
trace_mem_stores = False
# Show all microcode for disassembled instructions
trace_microcode = False
# Show warnings (non-implemented microcode instructions etc)
show_warnings = False

# Utilities for working with modular arithmetic
def s_to_u(x, mask):
    '''
    Move range for signed comparison.
    range -0x80000000 .. 0x7fffffff to
           0x00000000 .. 0xffffffff
    '''
    return (x + (mask>>1)+1) & mask

def sign_extend(x, mask):
    '''
    Unsigned to signed value
    '''
    halfway = (mask>>1)+1 # smallest signed int
    if x < halfway: # positive or zero, return as-is
        return x
    else: # negative, subtract one full rotation
        return x - (mask + 1)

# General operations
def binop_s(op, width):
    mask = (1<<width)-1
    def apply(self, inst):
        t0 = self.load(inst.args[1])
        t1 = self.load(inst.args[2])
        if t0 is None or t1 is None:
            rv = None
        else:
            rv = op(sign_extend(t0, mask), sign_extend(t1, mask)) & mask
        self.store(inst.args[0], rv)
        self.ptr += 1
    return apply

def binop(op, width):
    mask = (1<<width)-1
    def apply(self, inst):
        t0 = self.load(inst.args[1])
        t1 = self.load(inst.args[2])
        if t0 is None or t1 is None:
            rv = None
        else:
            rv = op(t0, t1) & mask
        self.store(inst.args[0], rv)
        self.ptr += 1
    return apply

def unop(op, width):
    mask = (1<<width)-1
    def apply(self, inst):
        t0 = self.load(inst.args[1])
        if t0 is None:
            rv = None
        else:
            rv = op(t0) & mask
        self.store(inst.args[0], rv)
        self.ptr += 1
    return apply

def extop(srcwidth, dstwidth, signed):
    smask = (1<<srcwidth)-1
    if signed: # sign-extend
        return unop(lambda t0: sign_extend(t0 & smask, smask), dstwidth)
    else: # zero-extend
        return unop(lambda t0: t0 & smask, dstwidth)

def mem_ldop(width, signed):
    def apply(self, inst):
        addr = self.load(inst.args[1])
        rv = self.state.memld(addr, width)
        self.store(inst.args[0], rv)
        self.ptr += 1
    return apply

def mem_stop(width):
    def apply(self, inst):
        addr = self.load(inst.args[1])
        value = self.load(inst.args[0])
        if trace_mem_stores:
            self.trace_func((addr,width), value)
        self.state.memst(addr, width, value)
        self.ptr += 1
    return apply

# General conditions
CONDITIONS = {
    qdis.COND_NEVER: lambda x0,x1,mask: False,
    qdis.COND_ALWAYS: lambda x0,x1,mask: True,
    qdis.COND_EQ: lambda x0,x1,mask: x0==x1, 
    qdis.COND_NE: lambda x0,x1,mask: x0!=x1, 
    qdis.COND_LT: lambda x0,x1,mask: s_to_u(x0,mask)<s_to_u(x1,mask), 
    qdis.COND_GE: lambda x0,x1,mask: s_to_u(x0,mask)>=s_to_u(x1,mask), 
    qdis.COND_LE: lambda x0,x1,mask: s_to_u(x0,mask)<=s_to_u(x1,mask), 
    qdis.COND_GT: lambda x0,x1,mask: s_to_u(x0,mask)>s_to_u(x1,mask), 
    qdis.COND_LTU: lambda x0,x1,mask: x0<x1, 
    qdis.COND_GEU: lambda x0,x1,mask: x0>=x1, 
    qdis.COND_LEU: lambda x0,x1,mask: x0<=x1, 
    qdis.COND_GTU: lambda x0,x1,mask: x0>x1, 
}

# XXX move this inside qdis some way
#     need platform-independent way to compute instruction flag and pc changes from env change instructions
ENV_ARM_THUMB_FLAG = 0xd0

# Memory handling
import struct
LITTLE_ENDIAN={
    8: struct.Struct(b'<B'),
    16: struct.Struct(b'<H'),
    32: struct.Struct(b'<L'),
    64: struct.Struct(b'<Q')
}
BIG_ENDIAN={
    8: struct.Struct(b'>B'),
    16: struct.Struct(b'>H'),
    32: struct.Struct(b'>L'),
    64: struct.Struct(b'>Q')
}

class CPUState(object):
    '''
    Current state of simulated machine.
    '''
    def __init__(self):
        self.globals = [] # list of registers
        self.memory = []  # list of (base, [buffer...])
        self.env = {}
        self.endian = LITTLE_ENDIAN

    def memld(self, addr, width):
        value = None
        width_b = width // 8
        for (base, end, buf) in self.memory:
            if addr >= base and (addr + width_b) <= end:
                value = buf[(addr-base):(addr-base+width_b)]
        if value is not None:
            return self.endian[width].unpack(bytes(value))[0]
        else:
            return None
    
    def memst(self, addr, width, value):
        if value is None:
            return
        value = value & ((1<<width)-1)
        value = self.endian[width].pack(value)
        width_b = width // 8
        for (base, end, buf) in self.memory:
            if addr >= base and (addr + width_b) <= end:
                buf[(addr-base):(addr-base+width_b)] = value

    def add_memory(self, base, size, data=None):
        '''
        Add memory range.
        '''
        mem = bytearray(size)
        if data is not None:
            mem[0:len(data)] = data
        self.memory.append((base, base+size, mem))

    def get_memory(self, addr, size):
        '''
        Read memory data.
        '''
        for (base, end, buf) in self.memory:
            if addr >= base and (addr + size) <= end:
                return buf[(addr-base):(addr-base+size)]
        return None

class ConcreteEval(object):
    '''
    Emulator.
    '''
    def __init__(self, d):
        # Create list of handler bound methods for opcodes
        self.handlers = []
        for opcode in xrange(d.lookup_value(qdis.INFO_NUM_OPS, 0)):
            op_str = d.lookup_name(qdis.INFO_OP, opcode)
            if op_str is not None:
                handler = getattr(self, 'eval_'+op_str, None)
                if handler is None:
                    # print("Warning: unhandled instruction " + op_str)
                    handler = functools.partial(self._unhandled, op_str)
                self.handlers.append(handler)
        num_globals = d.lookup_value(qdis.INFO_NUM_GLOBALS, 0)

        self.state = CPUState()
        self.state.globals = [UNDEFINED] * num_globals 

        self.global_by_id = [None] * num_globals
        self.global_by_name = {}
        for globid in xrange(num_globals):
            name = d.lookup_name(qdis.INFO_GLOBAL, globid)
            self.global_by_id[globid] = name 
            self.global_by_name[name] = globid

        self.warning_func = lambda val: None
        self.trace_func = lambda key,value: None # dummy
        # globals
        self.env_id = self.global_by_name['env']

    def set_globals(self, values):
        '''
        Set a bunch of globals (registers) from a dictionary.
        '''
        for k,v in values.iteritems():
            self.state.globals[self.global_by_name[k]] = v

    def start_block(self, block, args=None):
        # All locals and temps are undefined at the start of every block
        self.temps = [UNDEFINED]*len(block.syms)
        if args is not None:
            self.temps[0:len(args)] = args

        self.ops = block.ops
        self.labels = block.labels
        self.ptr = 0
        while self.ptr is not None:
            i = self.ops[self.ptr]
            if trace_microcode:
                self.trace_func(TRACE_INSTRUCTION, i)
            self.eval_inst(i)
        return self.temps
    
    def eval_inst(self, inst):
        '''Evaluate an instruction'''
        self.handlers[inst.opcode](inst)
    def _unhandled(self, op, inst):
        '''Called when an instruction is unhandled'''
        self.warning_func('unhandled %s (%i)' % (op,inst.opcode))
        # set all output arguments to UNDEFINED
        for arg in inst.args:
            if arg.flags & qdis.ARG_OUTPUT:
                self.store(arg, UNDEFINED)
            elif arg.flags & qdis.ARG_INPUT:
                self.load(arg) # dummy load
        self.ptr += 1
    def store(self, dest, expr):
        '''
        Store symbolic value into global or temporary.
        '''
        if dest.flags & qdis.ARG_GLOBAL:
            if trace_global_stores:
                self.trace_func(self.global_by_id[dest.value], expr)
            self.state.globals[dest.value] = expr
        elif dest.flags & qdis.ARG_TEMP:
            if trace_temp_stores:
                self.trace_func('tmp%i' % dest.value, expr)
            self.temps[dest.value] = expr
        else:
            raise AssertionError('Invalid argument')
    def load(self, dest):
        '''
        Load symbolic value from global or temp.
        '''
        if dest.flags & qdis.ARG_GLOBAL:
            return self.state.globals[dest.value]
        elif dest.flags & qdis.ARG_TEMP:
            return self.temps[dest.value]
        else:
            raise AssertionError('Invalid argument')

    def clear_temps(self):
        '''
        Clear temps (not locals) between basic blocks
        '''
        # TODO
    
    #### Instructions ####
    def eval_discard(self, inst):
        '''discard dest'''
        self.store(inst.args[0], UNDEFINED)
        self.ptr += 1
    
    eval_mov_i32 = unop(lambda x: x, 32)
    eval_mov_i64 = unop(lambda x: x, 64)
    
    def eval_movi_i32(self, inst):
        '''movi_i32 dest,src'''
        self.store(inst.args[0], inst.args[1].value & 0xffffffffL)
        self.ptr += 1
    def eval_movi_i64(self, inst):
        '''movi_642 dest,src'''
        self.store(inst.args[0], inst.args[1].value & 0xffffffffffffffffL)
        self.ptr += 1

    def brcond(self, inst, width):
        '''brcond_iXX t0,t1,cond,label'''
        val0 = self.load(inst.args[0])
        val1 = self.load(inst.args[1])
        cond = inst.args[2].value
        label = inst.args[3].value
        if CONDITIONS[cond](val0, val1, (1<<width)-1):
            self.ptr = self.labels[label]
        else:
            self.ptr += 1
        self.clear_temps()

    def setcond(self, inst, width):
        '''setcond_iXX d0,s0,s1,cond'''
        val0 = self.load(inst.args[1])
        val1 = self.load(inst.args[2])
        cond = inst.args[3].value
        self.store(inst.args[0], CONDITIONS[cond](val0, val1, (1<<width)-1))
        self.ptr += 1

    def movcond(self, inst, width):
        '''movcond_iXX ret,c1,c2,v1,v2,cond''' # ITE
        c1 = self.load(inst.args[1])
        c2 = self.load(inst.args[2])
        v1 = self.load(inst.args[3])
        v2 = self.load(inst.args[4])
        cond = inst.args[5].value
        cond_res = CONDITIONS[cond](c1, c2, (1<<width)-1)
        self.store(inst.args[0], v1 if cond_res else v2)
        self.ptr += 1

    def eval_brcond_i32(self, inst):
        self.brcond(inst, 32)
    def eval_setcond_i32(self, inst):
        self.setcond(inst, 32)
    def eval_movcond_i32(self, inst):
        self.movcond(inst, 32)
    def eval_brcond_i64(self, inst):
        self.brcond(inst, 64)
    def eval_setcond_i64(self, inst):
        self.setcond(inst, 64)
    def eval_movcond_i64(self, inst):
        self.movcond(inst, 64)

    def eval_set_label(self, inst):
        '''set_label $label'''
        self.clear_temps()
        self.ptr += 1

    def eval_st_i32(self, inst):
        '''st_i32 t0,basereg,offset'''
        expr = self.load(inst.args[0])
        self.state.env[inst.args[2].value] = expr
        if trace_global_stores:
            self.trace_func('[env+0x%x]' % inst.args[2].value, expr)
        self.ptr += 1
    
    def eval_ld_i32(self, inst):
        '''ld_i32 t0,basereg,offset'''
        self.store(inst.args[0], self.state.env.get(inst.args[2].value, 0))
        self.ptr += 1

    #def eval_qemu_ld32(self, inst):
    #    self.ptr += 1

    def eval_goto_tb(self, inst):
        '''goto_tb''' # ignored
        self.ptr += 1
    def eval_exit_tb(self, inst):
        '''exit_tb t1''' # interpreted as 'br to end'
        self.clear_temps()
        self.ptr = None

    eval_add_i32 = binop(lambda x,y: x+y, 32)
    eval_sub_i32 = binop(lambda x,y: x-y, 32)
    eval_mul_i32 = binop(lambda x,y: x*y, 32)
    eval_div_i32 = binop_s(lambda x,y: x//y, 32)
    eval_divu_i32 = binop(lambda x,y: x//y, 32)
    eval_rem_i32 = binop_s(lambda x,y: x%y, 32)
    eval_remu_i32 = binop(lambda x,y: x%y, 32)
    eval_and_i32 = binop(lambda x,y: x&y, 32)
    eval_or_i32 = binop(lambda x,y: x|y, 32)
    eval_xor_i32 = binop(lambda x,y: x^y, 32)
    eval_shl_i32 = binop(lambda x,y: x<<y, 32)
    eval_shr_i32 = binop(lambda x,y: x>>y, 32) 
    eval_sar_i32 = binop_s(lambda x,y: x>>y, 32)
    eval_not_i32 = unop(lambda x: ~x, 32)
    eval_neg_i32 = unop(lambda x: -x, 32)
    eval_nand_i32 = binop(lambda x,y: ~(x&y), 32)
    eval_nor_i32 = binop(lambda x,y: ~(x|y), 32)
    eval_eqv_i32 = binop(lambda x,y: ~(x^y), 32)
    eval_rotl_i32 = binop(lambda x,y: (x<<y) | (x>>(32-y)), 32)
    eval_rotr_i32 = binop(lambda x,y: (x>>y) | (x<<(32-y)), 32)
    
    eval_add_i64 = binop(lambda x,y: x+y, 64)
    eval_sub_i64 = binop(lambda x,y: x-y, 64)
    eval_mul_i64 = binop(lambda x,y: x*y, 64)
    eval_div_i64 = binop_s(lambda x,y: x//y, 64)
    eval_divu_i64 = binop(lambda x,y: x//y, 64)
    eval_rem_i64 = binop_s(lambda x,y: x%y, 64)
    eval_remu_i64 = binop(lambda x,y: x%y, 64)
    eval_and_i64 = binop(lambda x,y: x&y, 64)
    eval_or_i64 = binop(lambda x,y: x|y, 64)
    eval_xor_i64 = binop(lambda x,y: x^y, 64)
    eval_shl_i64 = binop(lambda x,y: x<<y, 64)
    eval_shr_i64 = binop(lambda x,y: x>>y, 64) 
    eval_sar_i64 = binop_s(lambda x,y: x>>y, 64)
    eval_not_i64 = unop(lambda x: ~x, 64)
    eval_neg_i64 = unop(lambda x: -x, 64)
    eval_nand_i64 = binop(lambda x,y: ~(x&y), 64)
    eval_nor_i64 = binop(lambda x,y: ~(x|y), 64)
    eval_eqv_i64 = binop(lambda x,y: ~(x^y), 64)
    eval_rotl_i64 = binop(lambda x,y: (x<<y) | (x>>(64-y)), 64)
    eval_rotr_i64 = binop(lambda x,y: (x>>y) | (x<<(64-y)), 64)
    # TODO: bswap16/32/64/deposit
    # sign extension
    eval_ext8s_i32 = extop(8, 32, True)
    eval_ext16s_i32 = extop(16, 32, True)
    eval_ext8u_i32 = extop(8, 32, False)
    eval_ext16u_i32 = extop(16, 32, False)
    eval_ext8s_i64 = extop(8, 64, True)
    eval_ext16s_i64 = extop(16, 64, True)
    eval_ext32s_i64 = extop(32, 64, True)
    eval_ext8u_i64 = extop(8, 64, False)
    eval_ext16u_i64 = extop(16, 64, False)
    eval_ext32u_i64 = extop(32, 64, False)
    # memory
    eval_qemu_ld8u = mem_ldop(8, False)
    eval_qemu_ld8s = mem_ldop(8, True)
    eval_qemu_ld16u = mem_ldop(16, False)
    eval_qemu_ld16s = mem_ldop(16, True)
    eval_qemu_ld32 = mem_ldop(32, False)
    eval_qemu_ld32u = mem_ldop(32, False)
    eval_qemu_ld32s = mem_ldop(32, True)
    eval_qemu_ld64 = mem_ldop(64, True)
    eval_qemu_st8 = mem_stop(8)
    eval_qemu_st16 = mem_stop(16)
    eval_qemu_st32 = mem_stop(32)
    eval_qemu_st64 = mem_stop(64)


