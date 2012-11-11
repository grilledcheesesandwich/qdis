#!/usr/bin/python
from os import path
import subprocess

def pkg_config(type_, lib):
    return subprocess.check_output([PKGCONFIG, '--'+type_, lib]).strip().split(' ')

PKGCONFIG='pkg-config'
CC='gcc'
LD='ld'
OBJCOPY='objcopy'
CFLAGS=['-Wall','-Wextra','-Wformat','-Wformat-security','-g','-O','-fPIC']
LDFLAGS=['-g','-O']

QEMUROOT='..'
QEMUFLAGS=['-I.', '-I'+QEMUROOT,
	'-I'+path.join(QEMUROOT,'tcg'),
	'-I'+path.join(QEMUROOT,'fpu'),
	'-I'+path.join(QEMUROOT,'include'),
	'-I'+path.join(QEMUROOT,'linux-user'),
	'-D__STDC_FORMAT_MACROS', '-D_GNU_SOURCE', '-D_FILE_OFFSET_BITS=64', '-D_LARGEFILE_SOURCE',
	'-DTCG_PYTHON',
	'-Wredundant-decls', '-w', '-Wundef', '-Wendif-labels', '-Wwrite-strings', '-fno-strict-aliasing',
	'-Wno-sign-compare', '-Wno-missing-field-initializers', '-fexceptions'] + pkg_config('cflags', 'glib-2.0')
QEMULDFLAGS=pkg_config('libs', 'glib-2.0')

TARGETS=[
('DIS_TGT_ARM', 'arm', 'target-arm', []),
('DIS_TGT_X86_32', 'x86_32', 'target-i386', []),
('DIS_TGT_X86_64', 'x86_64', 'target-i386', ['-DTARGET_X86_64']),
('DIS_TGT_MIPS_32', 'mips_32', 'target-mips', []),
#('DIS_TGT_MIPS_64', 'mips_64', 'target-mips', ['-DTARGET_MIPS64']),
#('DIS_TGT_PPC_32', 'ppc_32', 'target-ppc', []),
#('DIS_TGT_PPC_64', 'ppc_64', 'target-ppc', ['-DTARGET_PPC64']),
]
def log(x):
    print(x)

def check_call(args):
    print(' '.join(args))
    return subprocess.check_call(args)
#
# Partial linking
# ld -r /tmp/a.o  /tmp/b.o /tmp/c.o -o /tmp/d.o
#   we want to restrict the symbols exported by the output object, so that no collisions happen
#
# Must be put into separate directory per target

def build_tgt(objname, basename, cflags):
    TARGET='arm'
    TARGETDIR = path.join(QEMUROOT, basename)
    TARGETCFLAGS = ['-I'+TARGETDIR,'-DNEED_CPU_H','-DTARGET='+objname]
    TARGETCFLAGS += CFLAGS + QEMUFLAGS + cflags
    # Mask these symbols, so that they don't overlap between the modules
    # I'd rather use --strip-symbols, but objcopy disallows this due to
    # relocations.
    # --prefix-symbols also can't be used because it escaped the
    # *UND* symbols as well.
    RENAME_SYMS = [ # objdump -t XXX-module.o | grep COM
    "gen_opparam_buf",
    "dis_size",
    "gen_opc_ptr",
    "gen_opc_instr_start",
    "gen_opc_pc",
    "gen_opc_buf",
    "tcg_ctx",
    "dis_offset",
    "gen_opc_icount",
    "gen_opparam_ptr",
    "dis_memory",
    "dis_fault"
    ]
    TARGETSOURCES = [
        path.join(TARGETDIR, 'translate.c'),
        path.join(QEMUROOT, 'tcg', 'tcg.c'),
        path.join(QEMUROOT, 'tcg', 'optimize.c'),
        'qemu-hooks.c',
        basename + '.c'
    ]
    TARGETINTERMEDIATES =[]
    for srcname in TARGETSOURCES:
        out = path.splitext(path.basename(srcname))[0] + '-' + objname + '.o'
        TARGETINTERMEDIATES.append(out)
        check_call([CC] + TARGETCFLAGS + [srcname, '-c', '-o', out])
    TARGETOUT_UNSTRIPPED = objname + '-unstripped.o'
    TARGETOUT = objname + '-module.o'
    # Partial link
    check_call([LD, '-r'] + TARGETINTERMEDIATES + ['-o', TARGETOUT_UNSTRIPPED])
    # Make all symbols local except for entry point
    #check_call([OBJCOPY, '--prefix-symbols='+objname+'_', TARGETOUT_UNSTRIPPED, TARGETOUT])
    args = []
    for sym in RENAME_SYMS:
        args.append('--redefine-sym')
        args.append(sym+'='+objname+'_'+sym)
    check_call([OBJCOPY, '-G', objname+'_create']+args+[TARGETOUT_UNSTRIPPED, TARGETOUT])

def build_dispatcher(targets):
    with open('dispatch_create.h', 'w') as f:
        f.write('''// This file is auto-generated, do not edit
#ifndef DISPATCH_CREATE_H
#define DISPATCH_CREATE_H
''')
        for (enumname, objname, _, _) in targets:
            f.write('extern Disassembler* %s_create(DisCPUFeature *feat);\n' % (objname))
        f.write('''static CreateFunction create_disassembler(DisTarget tgt)
{
    switch(tgt)
    {
''')
        for (enumname, objname, _, _) in targets:
            f.write('    case %s: return %s_create;\n' % (enumname, objname))
        f.write('''    default: return NULL;
    }
    return NULL;
}
#endif
''')

build_dispatcher(TARGETS)
for (enumname, objname, basename, cflags) in TARGETS:
    build_tgt(objname, basename, cflags)
