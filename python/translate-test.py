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
    if rv.data is None:
        return None
    else:
        return str(rv.data)

CALLFLAGS = {
disass.DIS_CALL_NO_READ_GLOBALS: 'NO_READ_GLOBALS',
disass.DIS_CALL_NO_WRITE_GLOBALS: 'NO_WRITE_GLOBALS',
disass.DIS_CALL_NO_SIDE_EFFECTS: 'NO_SIDE_EFFECTS'
}
def flags_to_str(strings, flags):
    x = 1
    rv = []
    while flags:
        if flags & x:
            rv.append(strings.get(x, '0x%x' % x))
            flags &= ~x
        x <<= 1
    if not rv:
        return '0'
    else:
        return '|'.join(rv)

def format_arg(arg, res, is_movi_inst):
    '''
    Format instruction argument as string, similar to tcg_dump syntax.
    '''
    if arg.flags & disass.DIS_ARG_CONSTANT:
        name = None
        if arg.flags & disass.DIS_ARG_COND:
            name = lookup_name(disass.DIS_INFO_COND, arg.value)
        elif arg.flags & disass.DIS_ARG_CALLFLAGS:
            name = flags_to_str(CALLFLAGS, arg.value)
        elif is_movi_inst:
            name = lookup_name(disass.DIS_INFO_HELPER_BY_ADDR, arg.value)
        if name is not None:
            return name
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
base = 0x12f80
#base = 0x142e8
f.seek(base)
instructions = f.read(4096)

inst = create_string_buffer(instructions, len(instructions))
offset = 0
pc = base

while offset < len(inst):
    print ((STYLE_ADDR+'%08x'+STYLE_COLON+':'+STYLE_RESET) % (pc+offset))
    flags = disass.DIS_INST_ARM_VFPEN_MASK
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
        if op.opcode == disass.DIS_OP_END:
            continue
        op_str = lookup_name(disass.DIS_INFO_OP, op.opcode)
        args = []
        is_movi_inst = op.opcode in [disass.DIS_OP_MOVI_I32, disass.DIS_OP_MOVI_I64]
        for y in xrange(op.args):
            arg = data.args[argptr+y]
            #print '  %08x 0x%x %i' % (arg.flags,arg.value,arg.size)
            args.append(format_arg(arg, data, is_movi_inst))
        print('  %s %s' % (op_str, (','.join(args))))
        argptr += op.args

