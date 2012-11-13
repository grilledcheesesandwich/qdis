// This file is auto-generated, do not edit
#ifndef DISPATCH_CREATE_H
#define DISPATCH_CREATE_H
extern Disassembler* arm_create(DisCPUFeature *feat);
extern Disassembler* x86_32_create(DisCPUFeature *feat);
extern Disassembler* x86_64_create(DisCPUFeature *feat);
extern Disassembler* mips_32_create(DisCPUFeature *feat);
static CreateFunction create_disassembler(DisTarget tgt)
{
    switch(tgt)
    {
    case DIS_TGT_ARM: return arm_create;
    case DIS_TGT_X86_32: return x86_32_create;
    case DIS_TGT_X86_64: return x86_64_create;
    case DIS_TGT_MIPS_32: return mips_32_create;
    default: return NULL;
    }
    return NULL;
}
#endif
