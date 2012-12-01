/*
 * Main dispatcher code for QDIS.
 *
 * Copyright (c) 2012 Wladimir J. van der Laan
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
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
