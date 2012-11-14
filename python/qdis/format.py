'''
Format/pretty-print qemu microcode instructions.
'''
from __future__ import print_function, unicode_literals, division, absolute_import
import qdis

def flags_to_str(d, infotype, flags):
    x = 1
    rv = []
    while flags:
        if flags & x:
            name = d.lookup_name(INFO_CALLFLAG, x)
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
    if arg.flags & qdis.ARG_CONSTANT:
        name = None
        if arg.flags & qdis.ARG_COND:
            name = d.lookup_name(qdis.INFO_COND, arg.value)
        elif arg.flags & qdis.ARG_CALLFLAGS:
            name = flags_to_str(d, qdis.INFO_CALLFLAG, arg.value)
        elif is_movi_inst:
            name = d.lookup_name(qdis.INFO_HELPER_BY_ADDR, arg.value)
        if name is not None:
            return name
        mask = ~0
        if arg.size == qdis.SIZE_32:
            mask = 0xffffffff
        return '$0x%x' % (arg.value&mask)
    else:
        if arg.flags & qdis.ARG_GLOBAL:
            return d.lookup_name(qdis.INFO_GLOBAL, arg.value)
        elif arg.flags & qdis.ARG_TEMP:
            pref = '?'
            if arg.value < len(syms):
                type_ = syms[arg.value].type
                if type_ == qdis.SYM_LOCAL:
                    pref = 'loc'
                elif type_ == qdis.SYM_TEMP:
                    pref = 'tmp'
            return '%s%i' % (pref, arg.value)

    return str(arg.value)

def format_inst(d, i, syms):
    op_str = d.lookup_name(qdis.INFO_OP, i.opcode)
    args = []
    is_movi_inst = i.opcode in [qdis.OP_MOVI_I32, qdis.OP_MOVI_I64]
    for arg in i.args:
        args.append(format_arg(d, arg, syms, is_movi_inst))
    return ('%s %s' % (op_str, (','.join(args))))
