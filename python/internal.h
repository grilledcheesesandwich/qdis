#ifndef H_INTERNAL
#define H_INTERNAL

typedef Disassembler* (*CreateFunction)(DisCPUFeature *feat);
typedef DisStatus (*DisassembleFunction)(Disassembler *dis, uint8_t *inst, size_t size, uint64_t pc, uint64_t inst_flags, uint32_t optimize,
        void *outbuffer, size_t outsize);
typedef void (*DumpFunction)(Disassembler *dis);
typedef void (*DestroyFunction)(Disassembler *dis);
typedef const char* (*LookupNameFunction)(Disassembler *dis, DisInfoType type, size_t id);
typedef size_t (*LookupValueFunction)(Disassembler *dis, DisInfoType type, size_t id);

typedef struct Disassembler_
{
    struct Impl_ *impl;
    // vtable
    DisassembleFunction disassemble;
    DumpFunction dump;
    DestroyFunction destroy;
    LookupNameFunction lookupName;
    LookupValueFunction lookupValue;
} Disassembler;

#endif
