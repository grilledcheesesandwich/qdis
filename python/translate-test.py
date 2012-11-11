# Try code translator from python
from ctypes import c_ubyte, create_string_buffer, cast, POINTER, byref
import disass

STYLE_ADDR = '\033[38;5;226m'
STYLE_COLON = '\033[38;5;244m'
STYLE_RESET = '\033[0m'

dis = disass.dis_Create(disass.DIS_TGT_ARM, None)


# Buffer to store microcode instructions
OutbufferType = c_ubyte * disass.DIS_BUFFER_SIZE

def lookup_name(infotype, x):
    '''
    Wrap dis_LookupName in a Python-friendly interface.
    '''
    rv = disass.dis_LookupName(dis, infotype, x)
    if rv is None:
        return None
    else:
        return str(rv)

def format_arg(arg, res):
    '''
    Format instruction argument as string, similar to tcg_dump syntax.
    '''
    # TODO: formatting input/output arguments different, call flags, etc
    if arg.flags & disass.DIS_ARG_CONSTANT:
        # TODO: DIS_ARG_COND, DIS_ARG_CALL_FLAGS
        mask = ~0
        if arg.size == disass.DIS_SIZE_32:
            mask = 0xffffffff
        return '$0x%x' % (arg.value&mask)
    else:
        if arg.flags & disass.DIS_ARG_GLOBAL:
            return lookup_name(disass.DIS_INFO_GLOBAL, arg.value)
        elif arg.flags & disass.DIS_ARG_TEMP:
            pref = '?'
            if arg.value < res.num_syms:
                type_ = res.syms[arg.value].type
                if type_ == disass.DIS_SYM_LOCAL:
                    pref = 'loc'
                elif type_ == disass.DIS_SYM_TEMP:
                    pref = 'tmp'
            return '%s%i' % (pref, arg.value)

    return str(arg.value)

outbuffer = OutbufferType()

f = open('test.so', 'rb')
base = 0x142e8
f.seek(0x142e8)
instructions = f.read(4096)

inst = create_string_buffer(instructions, len(instructions))
offset = 0
pc = base

while offset < len(inst):
    print ((STYLE_ADDR+'%08x'+STYLE_COLON+':'+STYLE_RESET) % (pc+offset))
    flags = 0
    optimize = disass.DIS_OPTIMIZE_FULL
    if offset >= len(inst):
        raise IndexError('Out of bounds access')
    result = disass.dis_Disassemble(dis, byref(inst,offset), len(inst)-offset, pc + offset, flags, optimize, outbuffer, len(outbuffer))
    offset += 4

    if result != disass.DIS_OK:
        if result == disass.DIS_ERR_OUT_OF_BOUNDS_ACCESS:
            raise IndexError('Out of bounds access')
        raise Exception('Disassembly error %i' % result)

    data = cast(outbuffer, POINTER(disass.DisResult)).contents
    argptr = 0
    for idx in xrange(data.num_ops):
        op = data.ops[idx]
        if op.opcode in [disass.DIS_OP_END,disass.DIS_OP_NOP,disass.DIS_OP_NOP1,
                disass.DIS_OP_NOP2,disass.DIS_OP_NOP3,disass.DIS_OP_NOPN]:
            argptr += op.args
            continue # skip "end" instruction, it is not interesting
        op_str = lookup_name(disass.DIS_INFO_OP, op.opcode)
        args = []
        for y in xrange(op.args):
            arg = data.args[argptr+y]
            #print '  %08x 0x%x %i' % (arg.flags,arg.value,arg.size)
            args.append(format_arg(arg, data))
        print('  %s %s' % (op_str, (','.join(args))))
        argptr += op.args
