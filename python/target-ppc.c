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

static void target_disassemble_text(disassemble_info *info, uint64_t pc, uint64_t flags)
{
#if 0
    if (flags >> 16) {
        info->endian = BFD_ENDIAN_LITTLE;
    }
    if (flags & 0xFFFF) {
        /* If we have a precise definitions of the instructions set, use it */
        info->mach = flags & 0xFFFF;
    } else 
#endif
    // XXX fix ppc flags, they use ctx->hflags and ctx->bfd_mach not the tb->flags
    {
#ifdef TARGET_PPC64
        info->mach = bfd_mach_ppc64;
#else
        info->mach = bfd_mach_ppc;
#endif
    }
    print_insn_ppc(pc, info);
}

