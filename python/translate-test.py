# Try code translator from python
from ctypes import c_ubyte, create_string_buffer, cast, POINTER
import disass

dis = disass.dis_Create(disass.DIS_TGT_ARM, None)

inst = create_string_buffer('\x3c\xc0\x81\xe5')
pc = 0x1000
flags = 0
optimize = disass.DIS_OPTIMIZE_FULL

OutbufferType = c_ubyte * disass.DIS_BUFFER_SIZE

outbuffer = OutbufferType()

def lookup_name(infotype, x):
    return disass.dis_LookupName(dis, infotype, x)

result = disass.dis_Disassemble(dis, inst, len(inst), pc, flags, optimize, outbuffer, len(outbuffer))
if result != disass.DIS_OK:
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
