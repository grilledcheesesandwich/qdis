/* Common stuff that applies to all architectures;
 * provides the interface to the outside world:
 *   TARGET_Create
 *   TARGET_Disassemble
 *   TARGET_Dump
 *   TARGET_Destroy
 */
#include <stdio.h>
#include "tcg.h"
#include "qemu-stubs.h"
#include "qdis.h"
#include "internal.h"
#include "disas-util.h"

struct Impl_ {
    TCGContext *ctx;
    CPUArchState *env;
};

/* target specific */
static CPUArchState *init_target(QDisCPUFeature *features);
static size_t target_pc_offset();
static size_t target_sp_offset();
static void target_disassemble_text(disassemble_info *dis_info, uint64_t pc, uint64_t inst_flags);

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

/* Find global with state offset `offset` */
static size_t find_global(TCGContext *ctx, size_t offset)
{
    int i = 0;
    for(i=0; i<ctx->nb_globals; ++i)
    {
        if(!ctx->temps[i].fixed_reg && ctx->temps[i].mem_allocated &&
           // ctx->temps[i].mem_reg == ?? &&
           ctx->temps[i].mem_offset == offset)
            return i;
    }
    return QDIS_INVALID;
}

/* Basetype to dis bitfield width */
static size_t baseTypeToDis(TCGType type)
{
    switch(type)
    {
    case TCG_TYPE_I32: return QDIS_SIZE_32;
    case TCG_TYPE_I64: return QDIS_SIZE_64;
    default: return QDIS_SIZE_UNKNOWN;
    }
}

/* helper functions for disassembly */
static void fillSymbols(TCGContext *ctx, QDisSym *syms)
{
    int i = 0;
    for(i = ctx->nb_globals; i < ctx->nb_temps; ++i)
    {
        int symid = i - ctx->nb_globals;
        syms[symid].type = ctx->temps[i].temp_local ? QDIS_SYM_LOCAL : QDIS_SYM_TEMP;
        syms[symid].size = baseTypeToDis(ctx->temps[i].base_type);
    }
}
static void fillArg(TCGContext *s, QDisArg *argo, uint32_t flags, int idx)
{
    argo->flags = flags;
    if(idx < s->nb_globals)
    {
#if 0
        if(ctx->temps[i].mem_allocated && ctx->temps[i].mem_reg==0)
        {
            argo->flags |= QDIS_ARG_GLOBAL;
            argo->value = s->temp[idx].mem_offset; // offset into env
        } else {
            argo->flags |= QDIS_ARG_ENVPTR;
            argo->value = s->temp[idx].reg;
        }
#endif
        argo->flags |= QDIS_ARG_GLOBAL;
        argo->value = idx; // ordinal for QDIS_INFO_GLOBAL
    } else if(idx < s->nb_temps) {
        argo->flags |= QDIS_ARG_TEMP;
        argo->value = idx - s->nb_globals;
    }
    argo->size = baseTypeToDis(s->temps[idx].base_type);
}
static void fillConst(TCGContext *s, QDisArg *argo, uint32_t flags, size_t value, QDisBitsize size)
{
    argo->flags = flags;
    argo->value = value;
    argo->size = size;
}
static void fillOpcodes(TCGContext *s, QDisOp *opso, QDisArg *argso, size_t *ops_ptr_out, size_t *args_ptr_out)
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

    opc_ptr = s->gen_opc_buf;
    args = s->gen_opparam_buf;
    while (opc_ptr < s->gen_opc_ptr)
    {
        bool nop = false;
        c = *opc_ptr++;
        def = &tcg_op_defs[c];

        args_ptr_start = args_ptr;
        /* determine number of args etc */
        if (c == INDEX_op_nop || c == INDEX_op_nop2 || c == INDEX_op_nop3 || c == INDEX_op_nopn) {
            nb_oargs = def->nb_oargs;
            nb_iargs = def->nb_iargs;
            nb_cargs = def->nb_cargs;
            if (c == INDEX_op_nopn) {
                /* varible number of arguments */
                nb_cargs = args[0];
            }
            nop = true;
        } else if (c == INDEX_op_call) {
            /* variable number of arguments */
            nb_oargs = args[0] >> 16;
            nb_iargs = args[0] & 0xffff;
            nb_cargs = def->nb_cargs + 1;
            /* one carg at the end (flags) */
            /* function name */
            fillArg(s, &argso[args_ptr + 0], QDIS_ARG_INPUT | QDIS_ARG_CALLTARGET, args[1 + nb_oargs + nb_iargs - 1]);
            /* flags */
            fillConst(s, &argso[args_ptr + 1], QDIS_ARG_CONSTANT | QDIS_ARG_CALLFLAGS,
                args[1 + nb_oargs + nb_iargs], QDIS_SIZE_64);
            args_ptr += 2;
            for(i = 0; i < (nb_oargs + nb_iargs - 1); i++) {
                if(args[1 + i] != TCG_CALL_DUMMY_ARG) // Not interested in dummy args
                {
                    fillArg(s, &argso[args_ptr], i<nb_oargs ? QDIS_ARG_OUTPUT : QDIS_ARG_INPUT, args[1 + i]);
                    args_ptr += 1;
                }
            }
            /* Skip last carg, which is "number of arguments". */
        } else if (c == INDEX_op_movi_i32 || c == INDEX_op_movi_i64) {
            nb_oargs = def->nb_oargs;
            nb_iargs = def->nb_iargs;
            nb_cargs = def->nb_cargs;
            for(i = 0; i < nb_oargs; i++) {
                fillArg(s, &argso[args_ptr], QDIS_ARG_OUTPUT, args[i]);
                args_ptr += 1;
            }
            for(i = 0; i < nb_iargs; i++) {
                fillArg(s, &argso[args_ptr], QDIS_ARG_INPUT, args[nb_oargs + i]);
                args_ptr += 1;
            }
            for(i = 0; i < nb_cargs; i++) {
                fillConst(s, &argso[args_ptr], QDIS_ARG_CONSTANT,
                    args[nb_oargs + nb_iargs + i],
                    (c == INDEX_op_movi_i64) ? QDIS_SIZE_64 : QDIS_SIZE_32);
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
                fillArg(s, &argso[args_ptr], QDIS_ARG_OUTPUT, args[i]);
                args_ptr += 1;
            }
            for(i = 0; i < nb_iargs; i++) {
                fillArg(s, &argso[args_ptr], QDIS_ARG_INPUT, args[nb_oargs + i]);
                args_ptr += 1;
            }
            i = 0;
            /* condition */
            switch (c) {
            case INDEX_op_brcond_i32:
            case INDEX_op_setcond_i32:
            case INDEX_op_movcond_i32:
            case INDEX_op_brcond2_i32:
            case INDEX_op_setcond2_i32:
            case INDEX_op_brcond_i64:
            case INDEX_op_setcond_i64:
            case INDEX_op_movcond_i64:
                fillConst(s, &argso[args_ptr], QDIS_ARG_CONSTANT | QDIS_ARG_COND,
                    args[nb_oargs + nb_iargs + i], QDIS_SIZE_64);
                args_ptr += 1;
                i += 1;
                break;
            default:
                break;
            }
            /* label */
            switch (c) {
            case INDEX_op_br:
            case INDEX_op_brcond_i32:
            case INDEX_op_brcond2_i32:
            case INDEX_op_brcond_i64:
            case INDEX_op_set_label:
                fillConst(s, &argso[args_ptr], QDIS_ARG_CONSTANT | QDIS_ARG_LABEL,
                    args[nb_oargs + nb_iargs + i], QDIS_SIZE_64);
                args_ptr += 1;
                i += 1;
                break;
            default:
                break;
            }
            for(; i < nb_cargs; i++) {
                fillConst(s, &argso[args_ptr], QDIS_ARG_CONSTANT,
                    args[nb_oargs + nb_iargs + i], QDIS_SIZE_64);
                args_ptr += 1;
            }
        }
        args += nb_iargs + nb_oargs + nb_cargs;
        if(!nop)
        {
            opso[ops_ptr].opcode = c;
            opso[ops_ptr].args = args_ptr - args_ptr_start;
            ops_ptr += 1;
        }
    }
    *ops_ptr_out = ops_ptr;
    *args_ptr_out = args_ptr;
}

/* vtable method implementations */
static QDisStatus disassemble(QDisassembler *dis, uint8_t *inst, size_t size, uint64_t pc, uint64_t inst_flags, uint32_t optimize,
        void *outbuf, size_t outsize)
{
    TCGContext *ctx = dis->impl->ctx;
    if(outbuf == NULL)
        return QDIS_ERR_NULLPOINTER;
    if(((size_t)outbuf) & 7) // Improperly aligned output buffer
        return QDIS_ERR_ALIGNMENT;
    disassembly_set_window(inst, pc, size);
    TranslationBlock tb = {
        .pc = pc,
        .flags = inst_flags,
        /* set tb type to unknown for translators that don't override it */
        .s2e_tb_type = TB_UNKNOWN
    };

    // there are two singlestep flags, one in the environment, and one global
    // use the global one as we don't want to trigger interrupts
    singlestep = 1;

    cpu_single_env = dis->impl->env;
    tcg_func_start(ctx); // Resets state of context
    gen_intermediate_code(dis->impl->env, &tb);

    if(disassembly_get_error())
    {
        return QDIS_ERR_OUT_OF_BOUNDS_ACCESS;
    }
    if(optimize & QDIS_OPTIMIZE_GENERAL)
    {
        ctx->gen_opparam_ptr =
            tcg_optimize(ctx, ctx->gen_opc_ptr, ctx->gen_opparam_buf, tcg_op_defs);
    }
    if(optimize & QDIS_OPTIMIZE_LIVENESS)
    {
        tcg_liveness_analysis(ctx);
    }

    /* allocation */
    struct OutBuf out = {.ptr = outbuf, .end = outbuf + outsize};
    QDisResult *result = outbuf_alloc(&out, sizeof(QDisResult));
    if(result == NULL)
        return QDIS_ERR_BUFFER_TOO_SMALL;
    memset(result, 0, sizeof(QDisResult));
    /*   opcodes */
    result->num_ops = ctx->gen_opc_ptr - ctx->gen_opc_buf;
    result->ops = outbuf_alloc(&out, result->num_ops * sizeof(QDisOp));
    memset(result->ops, 0, result->num_ops * sizeof(QDisOp));
    /*   arguments */
    result->num_args = ctx->gen_opparam_ptr - ctx->gen_opparam_buf;
    result->args = outbuf_alloc(&out, result->num_args * sizeof(QDisArg));
    memset(result->args, 0, result->num_args * sizeof(QDisArg));
    /*   symbols */
    result->num_syms = ctx->nb_temps - ctx->nb_globals;
    result->syms = outbuf_alloc(&out, result->num_syms * sizeof(QDisSym));
    memset(result->syms, 0, result->num_syms * sizeof(QDisSym));
    /*   labels */
    result->num_labels = ctx->nb_labels;

    if(result->ops == NULL || result->args == NULL || result->syms == NULL)
        return QDIS_ERR_BUFFER_TOO_SMALL;

    fillSymbols(ctx, result->syms);
    fillOpcodes(ctx, result->ops, result->args, &result->num_ops, &result->num_args);

    result->inst_type = (QDisInstType)tb.s2e_tb_type;
    result->inst_size = tb.size;

    if(!(optimize & QDIS_OPTIMIZE_NOTEXT))
    {
        result->inst_text = outbuf_printf_start(&out);
        disassemble_info dis_info;
        disas_init(&dis_info, &out, inst, pc, size);
#ifdef TARGET_WORDS_BIGENDIAN
        dis_info.endian = BFD_ENDIAN_BIG;
#else
        dis_info.endian = BFD_ENDIAN_LITTLE;
#endif
        target_disassemble_text(&dis_info, pc, inst_flags);
    }
    //tcg_dump_ops(ctx);
    result->total_size = (size_t)out.ptr - (size_t)outbuf;

    return QDIS_OK;
}

static void dump(QDisassembler *dis)
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
static const char *lookupName(QDisassembler *dis, QDisInfoType type, size_t id)
{
    TCGContext *ctx = dis->impl->ctx;
    switch(type)
    {
    case QDIS_INFO_OP:
        if(id < tcg_op_defs_max)
            return tcg_op_defs[id].name;
        else
            return NULL;
    case QDIS_INFO_COND:
        if(id <= QDIS_COND_GTU)
            return cond_name[id];
        else
            return NULL;
    case QDIS_INFO_CALLFLAG:
        switch(type)
        {
        case QDIS_CALL_NO_READ_GLOBALS:
            return "NO_READ_GLOBALS";
        case QDIS_CALL_NO_WRITE_GLOBALS:
            return "NO_WRITE_GLOBALS";
        case QDIS_CALL_NO_SIDE_EFFECTS:
            return "NO_SIDE_EFFECTS";
        }
        return NULL;
    case QDIS_INFO_HELPER_BY_ADDR: {
        TCGHelperInfo *info = tcg_find_helper(ctx, id);
        if(info != NULL)
            return info->name;
        else
            return NULL;
        }
    case QDIS_INFO_HELPER:
        if(id < ctx->nb_helpers)
            return ctx->helpers[id].name;
        else
            return NULL;
        break;
    case QDIS_INFO_GLOBAL:
        if(id < ctx->nb_globals)
            return ctx->temps[id].name;
        else
            return NULL;
    }
    return NULL;
}


static size_t lookupValue(QDisassembler *dis, QDisInfoType type, size_t id)
{
    TCGContext *ctx = dis->impl->ctx;
    switch(type)
    {
    case QDIS_INFO_NUM_OPS:
        return tcg_op_defs_max;
    case QDIS_INFO_PC_OFFSET:
        return target_pc_offset();
    case QDIS_INFO_SP_OFFSET:
        return target_sp_offset();
    case QDIS_INFO_PC_GLOBAL:
        return find_global(ctx, target_pc_offset());
    case QDIS_INFO_SP_GLOBAL:
        return find_global(ctx, target_sp_offset());
    case QDIS_INFO_NUM_HELPERS:
        return ctx->nb_helpers;
    case QDIS_INFO_NUM_GLOBALS:
        return ctx->nb_globals;
    case QDIS_INFO_GLOBAL_SIZE:
        if(id < ctx->nb_globals)
            return baseTypeToDis(ctx->temps[id].base_type);
        else
            return 0;
    case QDIS_INFO_GLOBAL_OFFSET:
        if(id < ctx->nb_globals && !ctx->temps[id].fixed_reg && ctx->temps[id].mem_allocated)
            return ctx->temps[id].mem_offset;
        else
            return QDIS_INVALID;
    case QDIS_INFO_STATE_SIZE:
        return sizeof(CPUArchState);
    }
    return 0;
}

static void destroy(QDisassembler *dis)
{
    free(dis->impl);
    free(dis);
}

QDisassembler *glue(TARGET,_create)(QDisCPUFeature *feat)
{
    QDisassembler *rv = malloc(sizeof(QDisassembler));
    memset(rv, 0, sizeof(QDisassembler));
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

