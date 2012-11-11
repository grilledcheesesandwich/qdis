#include "common.h"

/* CPU specific initialization */
static CPUArchState *init_target(DisCPUFeature *features)
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
