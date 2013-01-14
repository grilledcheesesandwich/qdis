/*
 * Target-specific code for ARM architecture.
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

/* ARM specific */
static inline void set_feature(CPUARMState *env, int feature)
{
    env->features |= 1ULL << feature;
}

void set_features(CPUARMState *env)
{
    /* This function is called by cpu_arm_init() because it
     * needs to do common actions based on feature bits, etc
     * that have been set by the subclass init functions.
     * When we have QOM realize support it should become
     * a true realize function instead.
     */
    /* Some features automatically imply others: */
    if (arm_feature(env, ARM_FEATURE_V7)) {
        set_feature(env, ARM_FEATURE_VAPA);
        set_feature(env, ARM_FEATURE_THUMB2);
        set_feature(env, ARM_FEATURE_MPIDR);
        if (!arm_feature(env, ARM_FEATURE_M)) {
            set_feature(env, ARM_FEATURE_V6K);
        } else {
            set_feature(env, ARM_FEATURE_V6);
        }
    }
    if (arm_feature(env, ARM_FEATURE_V6K)) {
        set_feature(env, ARM_FEATURE_V6);
        set_feature(env, ARM_FEATURE_MVFR);
    }
    if (arm_feature(env, ARM_FEATURE_V6)) {
        set_feature(env, ARM_FEATURE_V5);
        if (!arm_feature(env, ARM_FEATURE_M)) {
            set_feature(env, ARM_FEATURE_AUXCR);
        }
    }
    if (arm_feature(env, ARM_FEATURE_V5)) {
        set_feature(env, ARM_FEATURE_V4T);
    }
    if (arm_feature(env, ARM_FEATURE_M)) {
        set_feature(env, ARM_FEATURE_THUMB_DIV);
    }
    if (arm_feature(env, ARM_FEATURE_ARM_DIV)) {
        set_feature(env, ARM_FEATURE_THUMB_DIV);
    }
    if (arm_feature(env, ARM_FEATURE_VFP4)) {
        set_feature(env, ARM_FEATURE_VFP3);
    }
    if (arm_feature(env, ARM_FEATURE_VFP3)) {
        set_feature(env, ARM_FEATURE_VFP);
    }
    if (arm_feature(env, ARM_FEATURE_LPAE)) {
        set_feature(env, ARM_FEATURE_PXN);
    }
}

static CPUArchState *init_target(QDisCPUFeature *features)
{
    // CPU specific initialization
    arm_translate_init();
    CPUARMState *env = (CPUARMState*)malloc(sizeof(CPUARMState));
    memset(env, 0, sizeof(CPUARMState));
    // Enable features of Cortex-A9 (for now, make this configurable or based on elf flags, see elfload.c:get_elf_hwcap)
    // TODO: use cpu.c
    set_feature(env, ARM_FEATURE_V7);
    set_feature(env, ARM_FEATURE_VFP3);
    set_feature(env, ARM_FEATURE_VFP_FP16);
    set_feature(env, ARM_FEATURE_NEON);
    set_feature(env, ARM_FEATURE_THUMB2EE);
    set_feature(env, ARM_FEATURE_DUMMY_C15_REGS);
    set_features(env);
    return env;
}

static size_t target_pc_offset()
{
    return offsetof(CPUARMState, regs[15]);
}

static size_t target_sp_offset()
{
    return offsetof(CPUARMState, regs[13]);
}

static void target_disassemble_text(disassemble_info *info, uint64_t pc, uint64_t flags)
{
    if (ARM_TBFLAG_THUMB(flags)) {
        /* disassembler (like processor) treats odd addresses as Thumb */
        pc |= 1;
    }
    if (ARM_TBFLAG_BSWAP_CODE(flags)) {
#ifdef TARGET_WORDS_BIGENDIAN
        info->endian = BFD_ENDIAN_LITTLE;
#else
        info->endian = BFD_ENDIAN_BIG;
#endif
    } else {
#ifdef TARGET_WORDS_BIGENDIAN
        info->endian = BFD_ENDIAN_BIG;
#else
        info->endian = BFD_ENDIAN_LITTLE;
#endif
    }
    print_insn_arm(pc, info);
}

