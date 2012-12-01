#ifndef H_DISAS_UTIL
#define H_DISAS_UTIL
#include "dis-asm.h"

/* output stream funcs */
struct OutBuf
{
    void *ptr;
    void *end;
};
void *outbuf_alloc(struct OutBuf *outbuf, size_t size);
char *outbuf_printf_start(struct OutBuf *outbuf);
int outbuf_printf(struct OutBuf *stream, const char *format, ...);

/* initialize disassemble_info object with defaults */
void disas_init(disassemble_info *info, struct OutBuf *out, void *code, uint64_t pc, size_t size);

#endif

