/*
 * Interal definitions and implementation details for QDIS.
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
#ifndef H_INTERNAL
#define H_INTERNAL

typedef QDisassembler* (*CreateFunction)(QDisCPUFeature *feat);
typedef QDisStatus (*DisassembleFunction)(QDisassembler *dis, uint8_t *inst, size_t size, uint64_t pc, uint64_t inst_flags, uint32_t optimize,
        void *outbuffer, size_t outsize);
typedef void (*DumpFunction)(QDisassembler *dis);
typedef void (*DestroyFunction)(QDisassembler *dis);
typedef const char* (*LookupNameFunction)(QDisassembler *dis, QDisInfoType type, size_t id);
typedef size_t (*LookupValueFunction)(QDisassembler *dis, QDisInfoType type, size_t id);

typedef struct QDisassembler_
{
    struct Impl_ *impl;
    // vtable
    DisassembleFunction disassemble;
    DumpFunction dump;
    DestroyFunction destroy;
    LookupNameFunction lookupName;
    LookupValueFunction lookupValue;
} QDisassembler;

#endif
