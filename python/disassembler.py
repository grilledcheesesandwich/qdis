'''
Higher-level Python wrapper for the disass functions.
'''
from ctypes import c_ubyte, create_string_buffer, cast, POINTER, byref
import qdis

# Buffer to store microcode instructions
OutbufferType = c_ubyte * qdis.QDIS_BUFFER_SIZE

# maximum expected size of one instruction
MAX_INST_SIZE = 64

def flags_to_str(d, infotype, flags):
    x = 1
    rv = []
    while flags:
        if flags & x:
            name = d.lookup_name(qdis.QDIS_INFO_CALLFLAG, x)
            if name is None:
                name = '0x%x' % x
            rv.append(name)
            flags &= ~x
        x <<= 1
    if not rv:
        return '0'
    else:
        return '|'.join(rv)

def format_arg(d, arg, syms, is_movi_inst):
    '''
    Format instruction argument as string, similar to tcg_dump syntax.
    '''
    if arg.flags & qdis.QDIS_ARG_CONSTANT:
        name = None
        if arg.flags & qdis.QDIS_ARG_COND:
            name = d.lookup_name(qdis.QDIS_INFO_COND, arg.value)
        elif arg.flags & qdis.QDIS_ARG_CALLFLAGS:
            name = flags_to_str(d, qdis.QDIS_INFO_CALLFLAG, arg.value)
        elif is_movi_inst:
            name = d.lookup_name(qdis.QDIS_INFO_HELPER_BY_ADDR, arg.value)
        if name is not None:
            return name
        mask = ~0
        if arg.size == qdis.QDIS_SIZE_32:
            mask = 0xffffffff
        return '$0x%x' % (arg.value&mask)
    else:
        if arg.flags & qdis.QDIS_ARG_GLOBAL:
            return d.lookup_name(qdis.QDIS_INFO_GLOBAL, arg.value)
        elif arg.flags & qdis.QDIS_ARG_TEMP:
            pref = '?'
            if arg.value < len(syms):
                type_ = syms[arg.value].type
                if type_ == qdis.QDIS_SYM_LOCAL:
                    pref = 'loc'
                elif type_ == qdis.QDIS_SYM_TEMP:
                    pref = 'tmp'
            return '%s%i' % (pref, arg.value)

    return str(arg.value)

def format_inst(d, i, syms):
    op_str = d.lookup_name(qdis.QDIS_INFO_OP, i.opcode)
    args = []
    is_movi_inst = i.opcode in [qdis.QDIS_OP_MOVI_I32, qdis.QDIS_OP_MOVI_I64]
    for arg in i.args:
        args.append(format_arg(d, arg, syms, is_movi_inst))
    return ('%s %s' % (op_str, (','.join(args))))

class Instruction(object):
    def __init__(self, opcode, args):
        self.opcode = opcode
        self.args = args

class Block(object):
    def __init__(self, ops, syms):
        self.ops = ops
        self.syms = syms

class Disassembler(object):
    def __init__(self, tgt, features=None):
        self.dis = qdis.qdis_Create(tgt, features)
        self.outbuffer = OutbufferType()

    def disassemble(self, inst, pc, flags, optimize=qdis.QDIS_OPTIMIZE_FULL):
        '''
        inst: binary instruction
        pc: current pc
        flags: instruction flags
        optimize: microcode optimization flags
        '''
        inst_buf = create_string_buffer(inst, len(inst))

        result = qdis.qdis_Disassemble(self.dis, inst_buf, len(inst_buf), pc, flags, optimize,
                self.outbuffer, len(self.outbuffer))

        if result != qdis.QDIS_OK:
            if result == qdis.QDIS_ERR_OUT_OF_BOUNDS_ACCESS:
                raise IndexError('Out of bounds access')
            raise Exception('Disassembly error %i' % result)

        data = cast(self.outbuffer, POINTER(qdis.QDisResult)).contents
        argptr = 0
        instructions = []
        for idx in xrange(data.num_ops):
            op = data.ops[idx]
            instructions.append(Instruction(op.opcode, data.args[argptr:argptr+op.args]))
            argptr += op.args
        return Block(instructions, data.syms[0:data.num_syms])

    def lookup_name(self, infotype, x):
        '''
        Look up token name.
        '''
        rv = qdis.qdis_LookupName(self.dis, infotype, x)
        if rv.data is None:
            return None
        else:
            return str(rv.data)

    def lookup_value(self, infotype, x):
        '''
        Get value from Disassembler object.
        '''
        return qdis.qdis_LookupValue(self.dis, infotype, x)
