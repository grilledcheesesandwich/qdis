#include "common.h"

/* CPU specific initialization */
static CPUArchState *init_target(DisCPUFeature *features)
{
    ppc_translate_init();
    CPUPPCState *env = (CPUPPCState*)malloc(sizeof(CPUPPCState));
    memset(env, 0, sizeof(CPUPPCState));
    // XXX features
    return env;
}
