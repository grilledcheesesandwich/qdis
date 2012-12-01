#include "common.h"

/* CPU specific initialization */
static CPUArchState *init_target(QDisCPUFeature *features)
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

static void target_disassemble_text(disassemble_info *info, uint64_t pc, uint64_t flags)
{
    if ((flags >> HF_CS64_SHIFT) & 1) {
        info->mach = bfd_mach_x86_64;
    } else if ((flags >> HF_CS32_SHIFT) & 1) {
        info->mach = bfd_mach_i386_i386;
    } else {
        info->mach = bfd_mach_i386_i8086;
    }
    print_insn_i386(pc, info);
}

