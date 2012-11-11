//#define TARGET arm
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

static CPUArchState *init_target(DisCPUFeature *features)
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
    set_features(env);
    printf("Features: %016x\n", env->features);
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
