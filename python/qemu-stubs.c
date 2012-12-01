/* QEmu stubs */

struct TranslationBlock;
typedef struct TranslationBlock TranslationBlock;
#include "cpu.h"
#include "tcg.h"

uint8_t gen_opc_instr_start[OPC_BUF_SIZE]; /* search_pc */
target_ulong gen_opc_pc[OPC_BUF_SIZE]; /* search_pc */
uint16_t gen_opc_icount[OPC_BUF_SIZE]; /* search_pc */
TCGContext tcg_ctx;

/* Current CPU */
DEFINE_TLS(CPUArchState *,cpu_single_env);

/** Debugging **/
int qemu_loglevel = 0;
/* loglevel_mask: CPU_LOG_TB_OP_OPT, to make sure that PCs are logged?
 not important if only disassembling one instruction at a time with
 single stepping */

int use_icount = 0;
int singlestep = 0;

/* dummy logging */
void qemu_log(const char *fmt, ...)
{
    va_list ap;

    va_start(ap, fmt);
#if 0 /* TODO: log to some python obj */
    if (qemu_logfile) {
        vfprintf(qemu_logfile, fmt, ap);
    }
#endif
    vprintf(fmt, ap); // DEBUG
    va_end(ap);
}

void qemu_log_mask(int mask, const char *fmt, ...)
{
    va_list ap;

    va_start(ap, fmt);
#if 0 /* TODO: log to some python obj */
    if ((qemu_loglevel & mask) && qemu_logfile) {
        vfprintf(qemu_logfile, fmt, ap);
    }
#endif
    vprintf(fmt, ap); // DEBUG
    va_end(ap);
}

// Memory accesses with bounds checking
// TODO: make this more specific and less global?
// QEMU architecture makes this very difficult
uint8_t *dis_memory;
target_ulong dis_offset;
target_ulong dis_size;
bool dis_fault;

void disassembly_set_window(void *memory, uint64_t offset, size_t size)
{
    dis_memory = memory;
    dis_offset = offset;
    dis_size = size;
    dis_fault = false; // out-of-bounds access
}

bool disassembly_get_error()
{
    return dis_fault;
}

// TODO: handle non-aligned!
uint8_t cpu_ldub_code(CPUArchState *arch, target_ulong addr)
{
    if((addr - dis_offset + 1) > dis_size)
    {
        dis_fault = true;
        return 0;
    }
    return *((uint8_t*)(dis_memory + addr - dis_offset));
}

int8_t cpu_ldsb_code(CPUArchState *arch, target_ulong addr)
{
    if((addr - dis_offset + 1) > dis_size)
    {
        dis_fault = true;
        return 0;
    }
    return *((int8_t*)(dis_memory + addr - dis_offset));
}

uint16_t cpu_lduw_code(CPUArchState *arch, target_ulong addr)
{
    if((addr - dis_offset + 2) > dis_size)
    {
        dis_fault = true;
        return 0;
    }
    return *((uint16_t*)(dis_memory + addr - dis_offset));
}

int16_t cpu_ldsw_code(CPUArchState *arch, target_ulong addr)
{
    if((addr - dis_offset + 2) > dis_size)
    {
        dis_fault = true;
        return 0;
    }
    return *((int16_t*)(dis_memory + addr - dis_offset));
}

uint32_t cpu_ldl_code(CPUArchState *arch, target_ulong addr)
{
    if((addr - dis_offset + 4) > dis_size)
    {
        dis_fault = true;
        return 0;
    }
    return *((uint32_t*)(dis_memory + addr - dis_offset));
}

uint64_t cpu_ldq_code(CPUArchState *arch, target_ulong addr)
{
    if((addr - dis_offset + 8) > dis_size)
    {
        dis_fault = true;
        return 0;
    }
    return *((uint64_t*)(dis_memory + addr - dis_offset));
}

