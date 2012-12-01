#!/usr/bin/python
'''
Generate target-specific entries in Makefile.modules, and dispatch_create.h.

Run this script after changing which modules (targets) are built.
'''
# Copyright (c) 2012 Wladimir J. van der Laan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from os import path
import sys
import subprocess

# TODO do the 32 bit targets make sense where a 64 bit one exists, or are they all just
#  subsets or special modes?
TARGETS=[
('QDIS_TGT_ARM', 'arm', 'arm', []),
#('QDIS_TGT_X86_32', 'x86_32', 'i386', []),
('QDIS_TGT_X86_64', 'x86_64', 'i386', ['-DTARGET_X86_64']),
#('QDIS_TGT_MIPS_32', 'mips_32', 'mips', []),
('QDIS_TGT_MIPS_64', 'mips_64', 'mips', ['-DTARGET_MIPS64']),
#('QDIS_TGT_PPC_32', 'ppc_32', 'ppc', []),
('QDIS_TGT_PPC_64', 'ppc_64', 'ppc', ['-DTARGET_PPC64']),
('QDIS_TGT_ALPHA', 'alpha', 'alpha', []),
#('QDIS_TGT_CRIS', 'cris', 'cris', []),
#('QDIS_TGT_LM32', 'lm32', 'lm32', []),
('QDIS_TGT_M68K', 'm68k', 'm68k', []),
#('QDIS_TGT_MICROBLAZE', 'microblaze', 'microblaze', []),
#('QDIS_TGT_OPENRISC', 'openrisc', 'openrisc', []),
#('QDIS_TGT_S390X', 's390x', 's390x', []),
#('QDIS_TGT_SH4', 'sh4', 'sh4', []),
#('QDIS_TGT_SPARC_32', 'sparc_32', 'sparc', []),
('QDIS_TGT_SPARC_64', 'sparc_64', 'sparc', ['-DTARGET_SPARC64']),
#('QDIS_TGT_UNICORE32', 'unicore', 'unicore', []),
#('QDIS_TGT_XTENSA', 'xtensa', 'xtensa', []),
]

#
# Partial linking
# ld -r /tmp/a.o  /tmp/b.o /tmp/c.o -o /tmp/d.o
#   we want to restrict the symbols exported by the output object, so that no collisions happen
#
# Must be put into separate directory per target
def join(x):
    return ' '.join(x)

def build_tgt(outfile, objname, basename, cflags):
    outfile.write('# target: '+objname+' (target-'+basename+')\n')
    TARGET='arm'
    TARGETDIR = '$(QEMUROOT)/target-' + basename
    TARGETCFLAGS = ['$(CFLAGS)','-I'+TARGETDIR,'-DNEED_CPU_H','-w','-DTARGET='+objname]
    TARGETCFLAGS += cflags
    targetcflags = 'TARGETCFLAGS_'+objname
    outfile.write(targetcflags+'='+join(TARGETCFLAGS)+'\n')
    RENAME_SYMS = [ # objdump -t XXX-module.o | grep COM
    "dis_size",
    "gen_opc_instr_start",
    "gen_opc_pc",
    "tcg_ctx",
    "dis_offset",
    "gen_opc_icount",
    "dis_memory",
    "dis_fault"
    ]
    args = []
    for sym in RENAME_SYMS:
        args.append('--redefine-sym')
        args.append(sym+'='+objname+'_'+sym)
    rename_symbols = 'RENAME_SYMBOLS_'+objname
    outfile.write(rename_symbols+'='+join(args)+'\n')
    # Mask these symbols, so that they don't overlap between the modules
    # I'd rather use --strip-symbols, but objcopy disallows this due to
    # relocations.
    # --prefix-symbols also can't be used because it escaped the
    # *UND* symbols as well.
    TARGETSOURCES = [
        path.join(TARGETDIR, 'translate.c'),
        path.join('$(QEMUROOT)', 'tcg', 'tcg.c'),
        path.join('$(QEMUROOT)', 'tcg', 'optimize.c'),
        path.join('$(QEMUROOT)', basename + '-dis.c'),
        'qemu-stubs.c',
        'target-' + basename + '.c'
    ]
    TARGETINTERMEDIATES =[]
    for srcname in TARGETSOURCES:
        out = path.splitext(path.basename(srcname))[0] + '-' + objname + '.o'
        TARGETINTERMEDIATES.append(out)
        outfile.write(out+': '+ srcname+ '\n')
        outfile.write('\t'+join(['$(CC)','$('+targetcflags+')', srcname, '-c', '-o', out])+'\n')
    TARGETOUT_UNSTRIPPED = objname + '-unstripped.o'
    TARGETOUT = objname + '-module.o'
    # Partial link
    outfile.write(TARGETOUT_UNSTRIPPED+': '+join(TARGETINTERMEDIATES)+'\n')
    outfile.write('\t'+join(['$(LD)', '-r'] + TARGETINTERMEDIATES + ['-o', TARGETOUT_UNSTRIPPED])+'\n')
    # Make all symbols local except for entry point
    #check_call([OBJCOPY, '--prefix-symbols='+objname+'_', TARGETOUT_UNSTRIPPED, TARGETOUT])
    outfile.write(TARGETOUT+': '+join([TARGETOUT_UNSTRIPPED])+'\n')
    outfile.write('\t'+join(['$(OBJCOPY)', '-G', objname+'_create', '$('+rename_symbols+')', TARGETOUT_UNSTRIPPED, TARGETOUT])+'\n')
    outfile.write('\n')
    return [TARGETOUT]

def build_dispatcher(targets):
    with open('dispatch_create.h', 'w') as f:
        f.write('''// This file is auto-generated, do not edit
#ifndef DISPATCH_CREATE_H
#define DISPATCH_CREATE_H
''')
        for (enumname, objname, _, _) in targets:
            f.write('extern QDisassembler* %s_create(QDisCPUFeature *feat);\n' % (objname))
        f.write('''static CreateFunction create_disassembler(QDisTarget tgt)
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

# build dispatcher.h
build_dispatcher(TARGETS)

# build Makefile.modules
outfile = open('Makefile.modules','w')
outfile.write('### Generated by build.sh ###\n')
modules = []
for (enumname, objname, basename, cflags) in TARGETS:
    modules.extend(build_tgt(outfile, objname, basename, cflags))
outfile.write('MODULES='+join(modules)+'\n')
outfile.close()
