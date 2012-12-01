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

