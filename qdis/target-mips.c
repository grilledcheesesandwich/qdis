/*
 * Target-specific code for MIPS architecture.
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
    mips_tcg_init();
    CPUMIPSState *env = (CPUMIPSState*)malloc(sizeof(CPUMIPSState));
    memset(env, 0, sizeof(CPUMIPSState));
    // XXX features
    return env;
}

static size_t target_pc_offset()
{
    return offsetof(CPUMIPSState, active_tc.PC);
}

static size_t target_sp_offset()
{
    return offsetof(CPUMIPSState, active_tc.gpr[29]);
}

static void target_disassemble_text(disassemble_info *info, uint64_t pc, uint64_t flags)
{
    // XXX make this switch dynamic?
#ifdef TARGET_WORDS_BIGENDIAN
    print_insn_big_mips(pc, info);
#else
    print_insn_little_mips(pc, info);
#endif
}

