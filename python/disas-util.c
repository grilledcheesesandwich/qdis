/*
 * Target-independent utilities for disassembling instructions to text format 
 * using qemu's built-in libbfd. 
 * These are basically wrappers to print to a memory buffer instead of a stream.
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
#include "disas-util.h"

#include <stdio.h>

void *outbuf_alloc(struct OutBuf *outbuf, size_t size)
{
    size_t alignment = 1;
    if(size == 0) return NULL;
    else if(size == 1) alignment = 1;
    else if(size > 1) alignment = 2;
    else if(size > 2) alignment = 4;
    else alignment = 8;

    size_t ptr_aligned = QEMU_ALIGN_UP((size_t)outbuf->ptr, alignment);
    size_t ptr_end = ptr_aligned + size;

    if(ptr_end > (size_t)outbuf->end)
        return NULL;
    outbuf->ptr = (void*)ptr_end;
    return (void*)ptr_aligned;
}

char *outbuf_printf_start(struct OutBuf *outbuf)
{
    char *rv = (char*) outbuf_alloc(outbuf, 1);
    if(rv != NULL)
        rv[0] = 0;
    return rv;
}

/* Append text to output buffer
 * precondition: outbuf_printf_start was called.
 */
int outbuf_printf(struct OutBuf *stream, const char *format, ...)
{
    // Seek one before terminating NULL character
    if(stream->ptr == stream->end)
        return 0;
    char *addr = ((char*)stream->ptr) - 1;
    size_t size = (size_t)stream->end - (size_t)addr;
    va_list ap;
    if(size <= 1 || *addr != 0)
        return 0;
    va_start(ap, format);
    int rv = vsnprintf(addr, size, format, ap);
    va_end(ap);
    // Update end pointer to point beyond terminating 0 character
    // Use strlen and not the return value of vsnprintf because the string may have been truncated.
    stream->ptr = addr + strlen(addr) + 1;
    return rv;
}

int generic_symbol_at_address (bfd_vma addr, struct disassemble_info *info)
{
    /* Just print address */
    return 1;
}

void generic_print_address (bfd_vma addr, struct disassemble_info *info)
{
    (*info->fprintf_func) (info->stream, "0x%" PRIx64, addr);
}

/* Get LENGTH bytes from info's buffer, at target address memaddr.
   Transfer them to myaddr.  */
int
buffer_read_memory(bfd_vma memaddr, bfd_byte *myaddr, int length,
                   struct disassemble_info *info)
{
    if (memaddr < info->buffer_vma
        || memaddr + length > info->buffer_vma + info->buffer_length)
        /* Out of bounds.  Use EIO because GDB uses it.  */
        return EIO;
    memcpy (myaddr, info->buffer + (memaddr - info->buffer_vma), length);
    return 0;
}

void
perror_memory (int status, bfd_vma memaddr, struct disassemble_info *info)
{
    /* no error message */
}

void disas_init(disassemble_info *info, struct OutBuf *out, void *code, uint64_t pc, size_t size)
{
    INIT_DISASSEMBLE_INFO((*info), (FILE*)out, (fprintf_function)outbuf_printf);

    info->buffer = code;
    info->buffer_vma = pc;
    info->buffer_length = size;
}

/* called from QEMU */
bfd_vma bfd_getl64 (const bfd_byte *addr)
{
  unsigned long long v;

  v = (unsigned long long) addr[0];
  v |= (unsigned long long) addr[1] << 8;
  v |= (unsigned long long) addr[2] << 16;
  v |= (unsigned long long) addr[3] << 24;
  v |= (unsigned long long) addr[4] << 32;
  v |= (unsigned long long) addr[5] << 40;
  v |= (unsigned long long) addr[6] << 48;
  v |= (unsigned long long) addr[7] << 56;
  return (bfd_vma) v;
}

bfd_vma bfd_getl32 (const bfd_byte *addr)
{
  unsigned long v;

  v = (unsigned long) addr[0];
  v |= (unsigned long) addr[1] << 8;
  v |= (unsigned long) addr[2] << 16;
  v |= (unsigned long) addr[3] << 24;
  return (bfd_vma) v;
}

bfd_vma bfd_getb32 (const bfd_byte *addr)
{
  unsigned long v;

  v = (unsigned long) addr[0] << 24;
  v |= (unsigned long) addr[1] << 16;
  v |= (unsigned long) addr[2] << 8;
  v |= (unsigned long) addr[3];
  return (bfd_vma) v;
}

bfd_vma bfd_getl16 (const bfd_byte *addr)
{
  unsigned long v;

  v = (unsigned long) addr[0];
  v |= (unsigned long) addr[1] << 8;
  return (bfd_vma) v;
}

bfd_vma bfd_getb16 (const bfd_byte *addr)
{
  unsigned long v;

  v = (unsigned long) addr[0] << 24;
  v |= (unsigned long) addr[1] << 16;
  return (bfd_vma) v;
}
