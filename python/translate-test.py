# Try code translator from python
from ctypes import c_ubyte, create_string_buffer, cast, POINTER, byref
import disass

STYLE_ADDR = '\033[1;33m'
STYLE_RESET = '\033[0m'

dis = disass.dis_Create(disass.DIS_TGT_ARM, None)


# Buffer to store microcode instructions
OutbufferType = c_ubyte * disass.DIS_BUFFER_SIZE

def lookup_name(infotype, x):
    return disass.dis_LookupName(dis, infotype, x)

outbuffer = OutbufferType()

f = open('test.so', 'rb')
base = 0x142e8
f.seek(0x142e8)
instructions = f.read(4096)

inst = create_string_buffer(instructions, len(instructions))
offset = 0
pc = base

while offset < len(inst):
    print ((STYLE_ADDR+'%08x'+STYLE_RESET+':') % (pc+offset))
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
    print lookup_name(disass.DIS_INFO_OP, op.opcode)
    for y in xrange(op.args):
        arg = data.args[argptr+y]
        print '  %08x 0x%x %i' % (arg.flags,arg.value,arg.size)
    argptr += op.args
