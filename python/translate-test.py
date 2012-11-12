# Try code translator from python
from ctypes import c_ubyte, create_string_buffer, cast, POINTER, byref
import disass

# Buffer to store microcode instructions
OutbufferType = c_ubyte * disass.DIS_BUFFER_SIZE

# maximum expected size of one instruction
MAX_INST_SIZE = 64

def flags_to_str(d, infotype, flags):
    x = 1
    rv = []
    while flags:
        if flags & x:
            name = d.lookup_name(disass.DIS_INFO_CALLFLAG, x)
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
    if arg.flags & disass.DIS_ARG_CONSTANT:
        name = None
        if arg.flags & disass.DIS_ARG_COND:
            name = d.lookup_name(disass.DIS_INFO_COND, arg.value)
        elif arg.flags & disass.DIS_ARG_CALLFLAGS:
            name = flags_to_str(d, disass.DIS_INFO_CALLFLAG, arg.value)
        elif is_movi_inst:
            name = d.lookup_name(disass.DIS_INFO_HELPER_BY_ADDR, arg.value)
        if name is not None:
            return name
        mask = ~0
        if arg.size == disass.DIS_SIZE_32:
            mask = 0xffffffff
        return '$0x%x' % (arg.value&mask)
    else:
        if arg.flags & disass.DIS_ARG_GLOBAL:
            return d.lookup_name(disass.DIS_INFO_GLOBAL, arg.value)
        elif arg.flags & disass.DIS_ARG_TEMP:
            pref = '?'
            if arg.value < len(syms):
                type_ = syms[arg.value].type
                if type_ == disass.DIS_SYM_LOCAL:
                    pref = 'loc'
                elif type_ == disass.DIS_SYM_TEMP:
                    pref = 'tmp'
            return '%s%i' % (pref, arg.value)

    return str(arg.value)

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
        self.dis = disass.dis_Create(tgt, features)
        self.outbuffer = OutbufferType()

    def disassemble(self, inst, pc, flags, optimize=disass.DIS_OPTIMIZE_FULL):
        '''
        inst: binary instruction
        pc: current pc
        flags: instruction flags
        optimize: microcode optimization flags
        '''
        inst_buf = create_string_buffer(inst, len(inst))

        result = disass.dis_Disassemble(self.dis, inst_buf, len(inst_buf), pc, flags, optimize,
                self.outbuffer, len(self.outbuffer))

        if result != disass.DIS_OK:
            if result == disass.DIS_ERR_OUT_OF_BOUNDS_ACCESS:
                raise IndexError('Out of bounds access')
            raise Exception('Disassembly error %i' % result)

        data = cast(self.outbuffer, POINTER(disass.DisResult)).contents
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
        rv = disass.dis_LookupName(self.dis, infotype, x)
        if rv.data is None:
            return None
        else:
            return str(rv.data)

    def lookup_value(self, infotype, x):
        '''
        Get value from Disassembler object.
        '''
        return disass.dis_LookupValue(self.dis, infotype, x)

if __name__ == '__main__':
    STYLE_ADDR = '\033[38;5;226m'
    STYLE_COLON = '\033[38;5;244m'
    STYLE_RESET = '\033[0m'

    d = Disassembler(disass.DIS_TGT_ARM, None)

    f = open('test.so', 'rb')
    base = 0x12f80
    #base = 0x142e8
    f.seek(base)
    instructions = f.read(4096)

    offset = 0
    pc = base
    while offset < len(instructions):
        print ((STYLE_ADDR+'%08x'+STYLE_COLON+':'+STYLE_RESET) % (pc+offset))
        flags = disass.DIS_INST_ARM_VFPEN_MASK
        result = d.disassemble(instructions[offset:offset+MAX_INST_SIZE], pc + offset, flags)

        for i in result.ops:
            if i.opcode == disass.DIS_OP_END:
                continue
            op_str = d.lookup_name(disass.DIS_INFO_OP, i.opcode)
            args = []
            is_movi_inst = i.opcode in [disass.DIS_OP_MOVI_I32, disass.DIS_OP_MOVI_I64]
            for arg in i.args:
                #print '  %08x 0x%x %i' % (arg.flags,arg.value,arg.size)
                args.append(format_arg(d, arg, result.syms, is_movi_inst))
            print('  %s %s' % (op_str, (','.join(args))))

        offset += 4

