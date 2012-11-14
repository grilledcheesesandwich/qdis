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
