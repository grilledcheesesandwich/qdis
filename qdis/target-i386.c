/*
 * Target-specific code for i386 architecture.
 *
 * Copyright (c) 2012 Wladimir J. van der Laan
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
#include "common.h"

/* CPU specific initialization */
static CPUArchState *init_target(QDisCPUFeature *features)
{
    optimize_flags_init();
    CPUX86State *env = (CPUX86State*)malloc(sizeof(CPUX86State));
    memset(env, 0, sizeof(CPUX86State));
    // Just blanket enable all features for now
    env->cpuid_features = 0xFFFFFFFF;
    env->cpuid_ext_features = 0xFFFFFFF;
    env->cpuid_ext2_features = 0xFFFFFFF;
    env->cpuid_7_0_ebx_features = 0xFFFFFFFF;
    return env;
}

static size_t target_pc_offset()
{
    return offsetof(CPUX86State, eip);
}

static size_t target_sp_offset()
{
    return offsetof(CPUX86State, regs[R_ESP]);
}

static void target_disassemble_text(disassemble_info *info, uint64_t pc, uint64_t flags)
{
    if ((flags >> HF_CS64_SHIFT) & 1) {
        info->mach = bfd_mach_x86_64;
    } else if ((flags >> HF_CS32_SHIFT) & 1) {
        info->mach = bfd_mach_i386_i386;
    } else {
        info->mach = bfd_mach_i386_i8086;
    }
    print_insn_i386(pc, info);
}

