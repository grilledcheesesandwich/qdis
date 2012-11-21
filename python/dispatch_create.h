// This file is auto-generated, do not edit
#ifndef DISPATCH_CREATE_H
#define DISPATCH_CREATE_H
extern QDisassembler* arm_create(QDisCPUFeature *feat);
extern QDisassembler* x86_64_create(QDisCPUFeature *feat);
extern QDisassembler* mips_64_create(QDisCPUFeature *feat);
extern QDisassembler* ppc_64_create(QDisCPUFeature *feat);
extern QDisassembler* alpha_create(QDisCPUFeature *feat);
extern QDisassembler* sparc_64_create(QDisCPUFeature *feat);
static CreateFunction create_disassembler(QDisTarget tgt)
{
    switch(tgt)
    {
    case QDIS_TGT_ARM: return arm_create;
    case QDIS_TGT_X86_64: return x86_64_create;
    case QDIS_TGT_MIPS_64: return mips_64_create;
    case QDIS_TGT_PPC_64: return ppc_64_create;
    case QDIS_TGT_ALPHA: return alpha_create;
    case QDIS_TGT_SPARC_64: return sparc_64_create;
    default: return NULL;
    }
    return NULL;
}
#endif
