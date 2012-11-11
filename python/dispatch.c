#include "disass.h"
#include "internal.h"

#include "dispatch_create.h"

Disassembler *dis_Create(DisTarget tgt, DisCPUFeature *feat)
{
    CreateFunction createfunc = create_disassembler(tgt);
    if(createfunc == NULL)
        return NULL;
    return createfunc(feat);
}

DisStatus dis_Disassemble(Disassembler *dis, uint8_t *inst, size_t size, uint64_t pc, uint64_t inst_flags, uint32_t optimize,
        void *outbuf, size_t outsize)
{
    if(dis == NULL) return DIS_ERR_NULLPOINTER;
    return dis->disassemble(dis, inst, size, pc, inst_flags, optimize, outbuf, outsize);
}

void dis_Dump(Disassembler *dis)
{
    if(dis == NULL) return;
    dis->dump(dis);
}

const char *dis_LookupName(Disassembler *dis, DisInfoType type, size_t id)
{
    if(dis == NULL) return NULL;
    return dis->lookupName(dis, type, id);
}

size_t dis_LookupValue(Disassembler *dis, DisInfoType type, size_t id)
{
    if(dis == NULL) return 0;
    return dis->lookupValue(dis, type, id);
}

void dis_Destroy(Disassembler *dis)
{
    if(dis == NULL) return;
    dis->destroy(dis);
}
