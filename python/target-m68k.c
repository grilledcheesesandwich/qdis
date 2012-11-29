#include "common.h"

static CPUArchState *init_target(QDisCPUFeature *features)
{
    // CPU specific initialization
    m68k_tcg_init();
    CPUM68KState *env = (CPUM68KState*)malloc(sizeof(CPUM68KState));
    memset(env, 0, sizeof(CPUM68KState));
    // TODO: features
    return env;
}

static size_t target_pc_offset()
{
    return offsetof(CPUM68KState, pc);
}

static size_t target_sp_offset()
{
    return offsetof(CPUM68KState, aregs[7]);
}
