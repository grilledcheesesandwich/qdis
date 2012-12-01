#include "common.h"

/* CPU specific initialization */
static CPUArchState *init_target(QDisCPUFeature *features)
{
    CPUSPARCState *env = (CPUSPARCState*)malloc(sizeof(CPUSPARCState));
    memset(env, 0, sizeof(CPUSPARCState));
    gen_intermediate_code_init(env);
    // XXX features
    return env;
}

static size_t target_pc_offset()
{
    return offsetof(CPUSPARCState, pc);
}

static size_t target_sp_offset()
{
    // TODO: env->regwptr[22]
    //       Sparc has multiple register windows, so this is not simply an offset
    return 0;
}

static void target_disassemble_text(disassemble_info *info, uint64_t pc, uint64_t flags)
{
    print_insn_sparc(pc, info);
}
