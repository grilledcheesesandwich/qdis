#include "qdis.h"
#include "internal.h"

#include "dispatch_create.h"

QDisassembler *qdis_Create(QDisTarget tgt, QDisCPUFeature *feat)
{
    CreateFunction createfunc = create_disassembler(tgt);
    if(createfunc == NULL)
        return NULL;
    return createfunc(feat);
}

QDisStatus qdis_Disassemble(QDisassembler *dis, uint8_t *inst, size_t size, uint64_t pc, uint64_t inst_flags, uint32_t optimize,
        void *outbuf, size_t outsize)
{
    if(dis == NULL) return QDIS_ERR_NULLPOINTER;
    return dis->disassemble(dis, inst, size, pc, inst_flags, optimize, outbuf, outsize);
}

void qdis_Dump(QDisassembler *dis)
{
    if(dis == NULL) return;
    dis->dump(dis);
}

const char *qdis_LookupName(QDisassembler *dis, QDisInfoType type, size_t id)
{
    if(dis == NULL) return NULL;
    return dis->lookupName(dis, type, id);
}

size_t qdis_LookupValue(QDisassembler *dis, QDisInfoType type, size_t id)
{
    if(dis == NULL) return 0;
    return dis->lookupValue(dis, type, id);
}

void qdis_Destroy(QDisassembler *dis)
{
    if(dis == NULL) return;
    dis->destroy(dis);
}
