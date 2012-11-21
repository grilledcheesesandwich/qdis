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

