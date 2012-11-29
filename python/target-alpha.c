#include "common.h"

/* CPU specific initialization */
static CPUArchState *init_target(QDisCPUFeature *features)
{
    CPUAlphaState *env = (CPUAlphaState*)malloc(sizeof(CPUAlphaState));
    memset(env, 0, sizeof(CPUAlphaState));
    alpha_translate_init();
    // XXX features
    return env;
}

static size_t target_pc_offset()
{
    return offsetof(CPUAlphaState, pc);
}

static size_t target_sp_offset()
{
    // register $30 is used as SP 
    return offsetof(CPUAlphaState, ir[30]);
}
