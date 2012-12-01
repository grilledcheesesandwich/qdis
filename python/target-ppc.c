/*
 * Target-specific code for PPC architecture.
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
    ppc_translate_init();
    CPUPPCState *env = (CPUPPCState*)malloc(sizeof(CPUPPCState));
    memset(env, 0, sizeof(CPUPPCState));
    // XXX features
    return env;
}

static size_t target_pc_offset()
{
    return offsetof(CPUPPCState, nip);
}

static size_t target_sp_offset()
{
    // Convention is that GPR1 is SP
    return offsetof(CPUPPCState, gpr[1]);
}

static void target_disassemble_text(disassemble_info *info, uint64_t pc, uint64_t flags)
{
#if 0
    if (flags >> 16) {
        info->endian = BFD_ENDIAN_LITTLE;
    }
    if (flags & 0xFFFF) {
        /* If we have a precise definitions of the instructions set, use it */
        info->mach = flags & 0xFFFF;
    } else 
#endif
    // XXX fix ppc flags, they use ctx->hflags and ctx->bfd_mach not the tb->flags
    {
#ifdef TARGET_PPC64
        info->mach = bfd_mach_ppc64;
#else
        info->mach = bfd_mach_ppc;
#endif
    }
    print_insn_ppc(pc, info);
}

