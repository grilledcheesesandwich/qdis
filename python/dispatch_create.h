// This file is auto-generated, do not edit
#ifndef DISPATCH_CREATE_H
#define DISPATCH_CREATE_H
extern QDisassembler* arm_create(QDisCPUFeature *feat);
extern QDisassembler* x86_32_create(QDisCPUFeature *feat);
extern QDisassembler* x86_64_create(QDisCPUFeature *feat);
extern QDisassembler* mips_64_create(QDisCPUFeature *feat);
extern QDisassembler* ppc_32_create(QDisCPUFeature *feat);
extern QDisassembler* ppc_64_create(QDisCPUFeature *feat);
extern QDisassembler* alpha_create(QDisCPUFeature *feat);
extern QDisassembler* m68k_create(QDisCPUFeature *feat);
extern QDisassembler* sparc_32_create(QDisCPUFeature *feat);
extern QDisassembler* sparc_64_create(QDisCPUFeature *feat);
static CreateFunction create_disassembler(QDisTarget tgt)
{
    switch(tgt)
    {
    case QDIS_TGT_ARM: return arm_create;
    case QDIS_TGT_I386: return x86_32_create;
    case QDIS_TGT_X86_64: return x86_64_create;
    case QDIS_TGT_MIPS: return mips_64_create;
    case QDIS_TGT_PPC: return ppc_32_create;
    case QDIS_TGT_PPC64: return ppc_64_create;
    case QDIS_TGT_ALPHA: return alpha_create;
    case QDIS_TGT_M68K: return m68k_create;
    case QDIS_TGT_SPARC: return sparc_32_create;
    case QDIS_TGT_SPARCV9: return sparc_64_create;
    default: return NULL;
    }
    return NULL;
}
#endif
