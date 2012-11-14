// This file is auto-generated, do not edit
#ifndef DISPATCH_CREATE_H
#define DISPATCH_CREATE_H
extern QDisassembler* arm_create(QDisCPUFeature *feat);
extern QDisassembler* x86_32_create(QDisCPUFeature *feat);
extern QDisassembler* x86_64_create(QDisCPUFeature *feat);
extern QDisassembler* mips_32_create(QDisCPUFeature *feat);
static CreateFunction create_disassembler(QDisTarget tgt)
{
    switch(tgt)
    {
    case QDIS_TGT_ARM: return arm_create;
    case QDIS_TGT_X86_32: return x86_32_create;
    case QDIS_TGT_X86_64: return x86_64_create;
    case QDIS_TGT_MIPS_32: return mips_32_create;
    default: return NULL;
    }
    return NULL;
}
#endif
