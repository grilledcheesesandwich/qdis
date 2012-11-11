//#define TARGET i386
#include "common.h"

/* CPU specific initialization */
static CPUArchState *init_target(DisCPUFeature *features)
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
