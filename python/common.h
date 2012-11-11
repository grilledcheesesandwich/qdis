/* Common stuff that applies to all architectures;
 * provides the interface to the outside world:
 *   TARGET_Create
 *   TARGET_Disassemble
 *   TARGET_Dump
 *   TARGET_Destroy
 */
#include <stdio.h>
#include "tcg.h"
#include "qemu-hooks.h"
#include "disass.h"
#include "internal.h"

struct Impl_ {
    TCGContext *ctx;
    CPUArchState *env;
};

static CPUArchState *init_target(DisCPUFeature *features);
static size_t target_pc_offset();
static size_t target_sp_offset();

/* from tcg.c */
extern TCGOpDef tcg_op_defs[];
extern const size_t tcg_op_defs_max;
extern const char * const cond_name[];
extern TCGHelperInfo *tcg_find_helper(TCGContext *s, tcg_target_ulong val);

/* target independent */
static TCGContext *init_global()
{
    TCGContext *ctx = &tcg_ctx;
    // Global initialization
    tcg_context_init(ctx);
    return ctx;
}
#if 0
/* Find global with state offset `offset` */
static size_t findGlobal(TCGContext *ctx, size_t offset)
{
    int i = 0;
    for(i=0; i<ctx->nb_globals; ++i)
    {
        if(!ctx->temps[i].fixed_reg && ctx->temps[i].mem_allocated &&
           // ctx->temps[i].mem_reg == ?? &&
           ctx->temps[i].mem_offset == offset)
            return i;
    }
    return DIS_INVALID;
}
#endif
/* Basetype to dis bitfield width */
static size_t baseTypeToDis(TCGType type)
{
    switch(type)
    {
    case TCG_TYPE_I32: return DIS_SIZE_32;
    case TCG_TYPE_I64: return DIS_SIZE_64;
    default: return DIS_SIZE_UNKNOWN;
    }
}
/* output stream funcs */
struct OutBuf
{
    void *ptr;
    void *end;
};
void *outbufAlloc(struct OutBuf *outbuf, size_t size)
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

/* helper functions for disassembly */
static void fillSymbols(TCGContext *ctx, DisSym *syms)
{
    int i = 0;
    for(i = ctx->nb_globals; i < ctx->nb_temps; ++i)
    {
        int symid = i - ctx->nb_globals;
        syms[symid].type = ctx->temps[i].temp_local ? DIS_SYM_LOCAL : DIS_SYM_TEMP;
        syms[symid].size = baseTypeToDis(ctx->temps[i].base_type);
    }
}
static void fillArg(TCGContext *s, DisArg *argo, uint32_t flags, int idx)
{
    argo->flags = flags;
    if(idx < s->nb_globals)
    {
#if 0
        if(ctx->temps[i].mem_allocated && ctx->temps[i].mem_reg==0)
        {
            argo->flags |= DIS_ARG_GLOBAL;
            argo->value = s->temp[idx].mem_offset; // offset into env
        } else {
            argo->flags |= DIS_ARG_ENVPTR;
            argo->value = s->temp[idx].reg;
        }
#endif
        argo->flags |= DIS_ARG_GLOBAL;
        argo->value = idx; // ordinal for DIS_INFO_GLOBAL
    } else if(idx < s->nb_temps) {
        argo->flags |= DIS_ARG_TEMP;
        argo->value = idx - s->nb_globals;
    }
    argo->size = DIS_SIZE_UNKNOWN;
}
static void fillConst(TCGContext *s, DisArg *argo, uint32_t flags, size_t value, DisBitsize size)
{
    argo->flags = flags;
    argo->value = value;
    argo->size = size;
}
static int fillOpcodes(TCGContext *s, DisOp *opso, DisArg *argso)
{
    const uint16_t *opc_ptr;
    const TCGArg *args;
    TCGArg arg;
    TCGOpcode c;
    int i, k, nb_oargs, nb_iargs, nb_cargs;
    int ops_ptr = 0;
    int args_ptr = 0, args_ptr_start = 0;
    const TCGOpDef *def;
    char buf[128];

    opc_ptr = gen_opc_buf;
    args = gen_opparam_buf;
    while (opc_ptr < gen_opc_ptr) {
        c = *opc_ptr++;
        def = &tcg_op_defs[c];

        opso[ops_ptr].opcode = c;
        args_ptr_start = args_ptr;
        /* determine number of args etc */
        if (c == INDEX_op_call) {
            /* variable number of arguments */
            TCGArg arg = *args++; /* this argument is dropped */
            nb_oargs = arg >> 16;
            nb_iargs = arg & 0xffff;
            nb_cargs = def->nb_cargs;
            /* one carg at the end (flags) */
            /* function name */
            fillArg(s, &argso[args_ptr + 0], DIS_ARG_INPUT | DIS_ARG_CALLTARGET, args[nb_oargs + nb_iargs - 1]);
            /* flags */
            fillConst(s, &argso[args_ptr + 1], DIS_ARG_CONSTANT | DIS_ARG_CALLFLAGS,
                args[nb_oargs + nb_iargs], DIS_SIZE_64);
            args_ptr += 2;
            for(i = 0; i < nb_oargs; i++) {
                fillArg(s, &argso[args_ptr], DIS_ARG_OUTPUT, args[i]);
                args_ptr += 1;
            }
            for(i = 0; i < (nb_iargs - 1); i++) {
                fillArg(s, &argso[args_ptr], DIS_ARG_INPUT, args[nb_oargs + i]);
                args_ptr += 1;
            }
            /* Skip last carg, which is "number of arguments".  * Insert a dummy to make the number of arguments match. */
            fillConst(s, &argso[args_ptr], DIS_ARG_CONSTANT | DIS_ARG_DUMMY, 0, DIS_SIZE_64);
            args_ptr += 1;
        } else if (c == INDEX_op_movi_i32 || c == INDEX_op_movi_i64) {
            nb_oargs = def->nb_oargs;
            nb_iargs = def->nb_iargs;
            nb_cargs = def->nb_cargs;
            for(i = 0; i < nb_oargs; i++) {
                fillArg(s, &argso[args_ptr], DIS_ARG_OUTPUT, args[i]);
                args_ptr += 1;
            }
            for(i = 0; i < nb_iargs; i++) {
                fillArg(s, &argso[args_ptr], DIS_ARG_INPUT, args[nb_oargs + i]);
                args_ptr += 1;
            }
            for(i = 0; i < nb_cargs; i++) {
                fillConst(s, &argso[args_ptr], DIS_ARG_CONSTANT,
                    args[nb_oargs + nb_iargs + i],
                    (c == INDEX_op_movi_i64) ? DIS_SIZE_64 : DIS_SIZE_32);
                args_ptr += 1;
            }
        } else {
            if (c == INDEX_op_nopn) {
                /* variable number of arguments */
                nb_cargs = *args;
                nb_oargs = 0;
                nb_iargs = 0;
            } else {
                nb_oargs = def->nb_oargs;
                nb_iargs = def->nb_iargs;
                nb_cargs = def->nb_cargs;
            }

            for(i = 0; i < nb_oargs; i++) {
                fillArg(s, &argso[args_ptr], DIS_ARG_OUTPUT, args[i]);
                args_ptr += 1;
            }
            for(i = 0; i < nb_iargs; i++) {
                fillArg(s, &argso[args_ptr], DIS_ARG_INPUT, args[nb_oargs + i]);
                args_ptr += 1;
            }
            switch (c) {
            case INDEX_op_brcond_i32:
            case INDEX_op_setcond_i32:
            case INDEX_op_movcond_i32:
            case INDEX_op_brcond2_i32:
            case INDEX_op_setcond2_i32:
            case INDEX_op_brcond_i64:
            case INDEX_op_setcond_i64:
            case INDEX_op_movcond_i64:
                fillConst(s, &argso[args_ptr], DIS_ARG_CONSTANT | DIS_ARG_COND,
                    args[nb_oargs + nb_iargs + i], DIS_SIZE_64);
                args_ptr += 1;
                i = 1;
                break;
            default:
                i = 0;
                break;
            }
            for(; i < nb_cargs; i++) {
                fillConst(s, &argso[args_ptr], DIS_ARG_CONSTANT,
                    args[nb_oargs + nb_iargs + i], DIS_SIZE_64);
                args_ptr += 1;
            }
        }
        args += nb_iargs + nb_oargs + nb_cargs;

        opso[ops_ptr].args = args_ptr - args_ptr_start;
        ops_ptr += 1;
    }
    return args_ptr;
}

/* vtable method implementations */
static DisStatus disassemble(Disassembler *dis, uint8_t *inst, size_t size, uint64_t pc, uint64_t inst_flags, uint32_t optimize,
        void *outbuf, size_t outsize)
{
    TCGContext *ctx = dis->impl->ctx;
    if(outbuf == NULL)
        return DIS_ERR_NULLPOINTER;
    if(((size_t)outbuf) & 7) // Improperly aligned output buffer
        return DIS_ERR_ALIGNMENT;
    disassembly_set_window(inst, pc, size);
    TranslationBlock tb = {
        .pc = pc,
        .flags = inst_flags
    };

    // there are two singlestep flags, one in the environment, and one global
    // use the global one as we don't want to trigger interrupts
    singlestep = 1;

    cpu_single_env = dis->impl->env;
    tcg_func_start(ctx); // Resets state of context
    gen_intermediate_code_pc(dis->impl->env, &tb);

    if(disassembly_get_error())
    {
        return DIS_ERR_OUT_OF_BOUNDS_ACCESS;
    }
    if(optimize & DIS_OPTIMIZE_GENERAL)
    {
        gen_opparam_ptr =
            tcg_optimize(ctx, gen_opc_ptr, gen_opparam_buf, tcg_op_defs);
    }
    if(optimize & DIS_OPTIMIZE_LIVENESS)
    {
        tcg_liveness_analysis(ctx);
    }

    /* allocation */
    struct OutBuf out = {.ptr = outbuf, .end = outbuf + outsize};
    DisResult *result = outbufAlloc(&out, sizeof(DisResult));
    printf("result %p outbuf=%p\n", result, outbuf);
    if(result == NULL)
        return DIS_ERR_BUFFER_TOO_SMALL;
    /*   opcodes */
    result->num_ops = gen_opc_ptr - gen_opc_buf;
    result->ops = outbufAlloc(&out, result->num_ops * sizeof(DisOp));
    memset(result->ops, 0, result->num_ops * sizeof(DisOp));
    /*   arguments */
    result->num_args = gen_opparam_ptr - gen_opparam_buf;
    result->args = outbufAlloc(&out, result->num_args * sizeof(DisArg));
    memset(result->args, 0, result->num_args * sizeof(DisArg));
    /*   symbols */
    result->num_syms = ctx->nb_temps - ctx->nb_globals;
    result->syms = outbufAlloc(&out, result->num_syms * sizeof(DisSym));
    memset(result->syms, 0, result->num_syms * sizeof(DisSym));

    if(result->ops == NULL || result->args == NULL || result->syms == NULL)
        return DIS_ERR_BUFFER_TOO_SMALL;

    fillSymbols(ctx, result->syms);
    int argc = fillOpcodes(ctx, result->ops, result->args);
    assert(argc == result->num_args);
    tcg_dump_ops(ctx);

    return DIS_OK;
}

static void dump(Disassembler *dis)
{
    //
    // target setup complete: print tcg globals
    // tcg_ctx->globals
    // want to know: registers, helpers
    // globals (registers):
    TCGContext *ctx = dis->impl->ctx;
    int i=0;
    printf("Ops:\n");
    for(i=0; i<tcg_op_defs_max; ++i)
    {
        printf("  %i %s\n", i, tcg_op_defs[i].name);
    }
    printf("Globals:\n");
    for(i=0; i<ctx->nb_globals; ++i)
    {
        printf("  %i %s %i %i %i %i\n", i, ctx->temps[i].name, ctx->temps[i].fixed_reg, ctx->temps[i].mem_allocated,
                ctx->temps[i].mem_reg, ctx->temps[i].mem_offset);
    }
    printf("Helpers:\n");
    for(i=0; i<ctx->nb_helpers; ++i)
    {
        printf("  %i %p %s\n", i, ctx->helpers[i].func, ctx->helpers[i].name);
    }
    printf("\n");
    tcg_dump_ops(ctx);
}
static const char *lookupName(Disassembler *dis, DisInfoType type, size_t id)
{
    TCGContext *ctx = dis->impl->ctx;
    switch(type)
    {
    case DIS_INFO_OP:
        if(id < tcg_op_defs_max)
            return tcg_op_defs[id].name;
    case DIS_INFO_COND:
        if(id <= DIS_COND_GTU)
            return cond_name[id];
    case DIS_INFO_HELPER_BY_ADDR: {
        TCGHelperInfo *info = tcg_find_helper(ctx, id);
        if(info != NULL)
            return info->name;
        }
    case DIS_INFO_HELPER:
        if(id < ctx->nb_helpers)
            return ctx->helpers[id].name;
    case DIS_INFO_GLOBAL:
        if(id < ctx->nb_globals)
            return ctx->temps[id].name;
    }
    return NULL;
}


static size_t lookupValue(Disassembler *dis, DisInfoType type, size_t id)
{
    TCGContext *ctx = dis->impl->ctx;
    switch(type)
    {
    case DIS_INFO_NUM_OPS:
        return tcg_op_defs_max;
    case DIS_INFO_PC_OFFSET:
        return target_pc_offset();
    case DIS_INFO_SP_OFFSET:
        return target_sp_offset();
    case DIS_INFO_NUM_HELPERS:
        return ctx->nb_helpers;
    case DIS_INFO_NUM_GLOBALS:
        return ctx->nb_globals;
    case DIS_INFO_GLOBAL_SIZE:
        if(id < ctx->nb_globals)
            return baseTypeToDis(ctx->temps[id].base_type);
    case DIS_INFO_GLOBAL_OFFSET:
        if(id < ctx->nb_globals && !ctx->temps[id].fixed_reg && ctx->temps[id].mem_allocated)
            return ctx->temps[id].mem_offset;
        else
            return DIS_INVALID;
    case DIS_INFO_STATE_SIZE:
        return sizeof(CPUArchState);
    }
    return 0;
}

static void destroy(Disassembler *dis)
{
    free(dis->impl);
    free(dis);
}

Disassembler *glue(TARGET,_create)(DisCPUFeature *feat)
{
    Disassembler *rv = malloc(sizeof(Disassembler));
    memset(rv, 0, sizeof(Disassembler));
    rv->impl = malloc(sizeof(struct Impl_));
    memset(rv->impl, 0, sizeof(struct Impl_));

    rv->impl->ctx = init_global();
    rv->impl->env = init_target(NULL);
    // Build vtable
    rv->disassemble = disassemble;
    rv->dump = dump;
    rv->destroy = destroy;
    rv->lookupName = lookupName;
    rv->lookupValue = lookupValue;
    // TODO: Build list of globals / offsets into env
    // "state map" would make it possible to request the name and size of globals by offset, iso by ordinal
    // also add in eip for x86
    return rv;
}
