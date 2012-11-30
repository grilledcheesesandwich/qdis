#ifndef H_QDIS
#define H_QDIS
#include <stdbool.h>
#include <stdlib.h>
#include <stdint.h>
/* qemu instruction decoder -- external interface */
// Return status values
typedef enum
{
    QDIS_OK = 0,
    QDIS_ERR_OUT_OF_BOUNDS_ACCESS = 1, /* instruction ran outside buffer */
    QDIS_ERR_BUFFER_TOO_SMALL = 2,  /* output buffer too small */
    QDIS_ERR_NULLPOINTER = 3, /* unexpected NULL argument */
    QDIS_ERR_ALIGNMENT = 4, /* output buffer not aligned to 8 bytes */
} QDisStatus;

typedef enum
{
    // (Address) register bitsize
    QDIS_TGT_8BIT  = 0x0000, // not supported
    QDIS_TGT_16BIT = 0x1000, // not supported
    QDIS_TGT_32BIT = 0x2000,
    QDIS_TGT_64BIT = 0x3000,
    // Supported architectures
    QDIS_TGT_ARM = 0 | QDIS_TGT_32BIT,
    //* QDIS_TGT_X86_32 = 1 | QDIS_TGT_32BIT,
    QDIS_TGT_X86_64 = 1 | QDIS_TGT_64BIT,
    QDIS_TGT_ALPHA = 2 | QDIS_TGT_64BIT,
    QDIS_TGT_CRIS = 3 | QDIS_TGT_32BIT,
    QDIS_TGT_LM32 = 4 | QDIS_TGT_32BIT,
    QDIS_TGT_M68K = 5 | QDIS_TGT_32BIT,
    QDIS_TGT_MICROBLAZE = 6 | QDIS_TGT_32BIT,
    //* QDIS_TGT_MIPS_32 = 7 | QDIS_TGT_32BIT,
    QDIS_TGT_MIPS_64 = 7 | QDIS_TGT_64BIT,
    QDIS_TGT_OPENRISC = 8 | QDIS_TGT_32BIT,
    //* QDIS_TGT_PPC_32 = 9 | QDIS_TGT_32BIT,
    QDIS_TGT_PPC_64 = 9 | QDIS_TGT_64BIT,
    QDIS_TGT_S390X = 10 | QDIS_TGT_64BIT,
    QDIS_TGT_SH4 = 11 | QDIS_TGT_32BIT,
    //* QDIS_TGT_SPARC_32 = 12 | QDIS_TGT_32BIT,
    QDIS_TGT_SPARC_64 = 12 | QDIS_TGT_64BIT,
    QDIS_TGT_UNICORE32 = 13 | QDIS_TGT_32BIT,
    QDIS_TGT_XTENSA = 14 | QDIS_TGT_32BIT
} QDisTarget;
//* use the 64 bit target

// Tokens for CPU features
// XXX this list quickly gets out of hand
// use ELF hwcap flags here?
typedef enum
{
    QDIS_FEATURE_END = 0,
    QDIS_ARM_FEATURE_VFP,
    QDIS_ARM_FEATURE_AUXCR,  /* ARM1026 Auxiliary control register.  */
    QDIS_ARM_FEATURE_XSCALE, /* Intel XScale extensions.  */
    QDIS_ARM_FEATURE_IWMMXT, /* Intel iwMMXt extension.  */
    QDIS_ARM_FEATURE_V6,
    QDIS_ARM_FEATURE_V6K,
    QDIS_ARM_FEATURE_V7,
    QDIS_ARM_FEATURE_THUMB2,
    QDIS_ARM_FEATURE_MPU,    /* Only has Memory Protection Unit, not full MMU.  */
    QDIS_ARM_FEATURE_VFP3,
    QDIS_ARM_FEATURE_VFP_FP16,
    QDIS_ARM_FEATURE_NEON,
    QDIS_ARM_FEATURE_THUMB_DIV, /* divide supported in Thumb encoding */
    QDIS_ARM_FEATURE_M, /* Microcontroller profile.  */
    QDIS_ARM_FEATURE_OMAPCP, /* OMAP specific CP15 ops handling.  */
    QDIS_ARM_FEATURE_THUMB2EE,
    QDIS_ARM_FEATURE_V7MP,    /* v7 Multiprocessing Extensions */
    QDIS_ARM_FEATURE_V4T,
    QDIS_ARM_FEATURE_V5,
    QDIS_ARM_FEATURE_STRONGARM,
    QDIS_ARM_FEATURE_VAPA, /* cp15 VA to PA lookups */
    QDIS_ARM_FEATURE_ARM_DIV, /* divide supported in ARM encoding */
    QDIS_ARM_FEATURE_VFP4, /* VFPv4 (implies that NEON is v2) */
    QDIS_ARM_FEATURE_GENERIC_TIMER,
    QDIS_ARM_FEATURE_MVFR, /* Media and VFP Feature Registers 0 and 1 */
    QDIS_ARM_FEATURE_DUMMY_C15_REGS, /* RAZ/WI all of cp15 crn=15 */
    QDIS_ARM_FEATURE_CACHE_TEST_CLEAN, /* 926/1026 style test-and-clean ops */
    QDIS_ARM_FEATURE_CACHE_DIRTY_REG, /* 1136/1176 cache dirty status register */
    QDIS_ARM_FEATURE_CACHE_BLOCK_OPS, /* v6 optional cache block operations */
    QDIS_ARM_FEATURE_MPIDR, /* has cp15 MPIDR */
    QDIS_ARM_FEATURE_PXN, /* has Privileged Execute Never bit */
    QDIS_ARM_FEATURE_LPAE, /* has Large Physical Address Extension */
    // TODO i386 etc
} QDisCPUFeature;

/* Instruction interpretation flags */
/* XXX would like a more standarized way that doesn't rely on qemu internals as much? 
 * also make a selection of flags that usefully affect instruction decoding 
 */
/* ARM */
#define QDIS_INST_ARM_THUMB_SHIFT      0   /* true if thumb instruction set mode */
#define QDIS_INST_ARM_THUMB_MASK       (1 << QDIS_INST_ARM_THUMB_SHIFT)
#define QDIS_INST_ARM_VECLEN_SHIFT     1
#define QDIS_INST_ARM_VECLEN_MASK      (0x7 << QDIS_INST_ARM_VECLEN_SHIFT)
#define QDIS_INST_ARM_VECSTRIDE_SHIFT  4
#define QDIS_INST_ARM_VECSTRIDE_MASK   (0x3 << QDIS_INST_ARM_VECSTRIDE_SHIFT)
#define QDIS_INST_ARM_PRIV_SHIFT       6   /* true if in privileged mode */
#define QDIS_INST_ARM_PRIV_MASK        (1 << QDIS_INST_ARM_PRIV_SHIFT)
#define QDIS_INST_ARM_VFPEN_SHIFT      7   /* true if vfp enabled */
#define QDIS_INST_ARM_VFPEN_MASK       (1 << QDIS_INST_ARM_VFPEN_SHIFT)
#define QDIS_INST_ARM_CONDEXEC_SHIFT   8
#define QDIS_INST_ARM_CONDEXEC_MASK    (0xff << QDIS_INST_ARM_CONDEXEC_SHIFT)
#define QDIS_INST_ARM_BSWAP_CODE_SHIFT 16  /* true if big endian */
#define QDIS_INST_ARM_BSWAP_CODE_MASK  (1 << QDIS_INST_ARM_BSWAP_CODE_SHIFT)

/* x86 */
#define QDIS_INST_X86_CPL_SHIFT         0
#define QDIS_INST_X86_SOFTMMU_SHIFT     2 /* true if soft mmu is being used */
#define QDIS_INST_X86_INHIBIT_IRQ_SHIFT 3 /* true if hardware interrupts must be disabled for next instruction */
#define QDIS_INST_X86_CS32_SHIFT        4 /* 16 or 32 segments */
#define QDIS_INST_X86_SS32_SHIFT        5
#define QDIS_INST_X86_ADDSEG_SHIFT      6 /* zero base for DS, ES and SS : can be '0' only in 32 bit CS segment */
#define QDIS_INST_X86_PE_SHIFT          7 /* copy of CR0.PE (protected mode) */
#define QDIS_INST_X86_TF_SHIFT          8 /* must be same as eflags */
#define QDIS_INST_X86_MP_SHIFT          9 /* the order must be MP, EM, TS */
#define QDIS_INST_X86_EM_SHIFT         10
#define QDIS_INST_X86_TS_SHIFT         11
#define QDIS_INST_X86_IOPL_SHIFT       12 /* must be same as eflags */
#define QDIS_INST_X86_LMA_SHIFT        14 /* only used on x86_64: long mode active */
#define QDIS_INST_X86_CS64_SHIFT       15 /* only used on x86_64: 64 bit code segment  */
#define QDIS_INST_X86_RF_SHIFT         16 /* must be same as eflags */
#define QDIS_INST_X86_VM_SHIFT         17 /* must be same as eflags */
#define QDIS_INST_X86_AC_SHIFT         18 /* must be same as eflags */
#define QDIS_INST_X86_SMM_SHIFT        19 /* CPU in SMM mode */
#define QDIS_INST_X86_SVME_SHIFT       20 /* SVME enabled (copy of EFER.SVME) */
#define QDIS_INST_X86_SVMI_SHIFT       21 /* SVM intercepts are active */
#define QDIS_INST_X86_OSFXSR_SHIFT     22 /* CR4.OSFXSR */
#define QDIS_INST_X86_SMAP_SHIFT       23 /* CR4.SMAP */

#define QDIS_INST_X86_CPL_MASK          (3 << QDIS_INST_X86_CPL_SHIFT)
#define QDIS_INST_X86_SOFTMMU_MASK      (1 << QDIS_INST_X86_SOFTMMU_SHIFT)
#define QDIS_INST_X86_INHIBIT_IRQ_MASK  (1 << QDIS_INST_X86_INHIBIT_IRQ_SHIFT)
#define QDIS_INST_X86_CS32_MASK         (1 << QDIS_INST_X86_CS32_SHIFT)
#define QDIS_INST_X86_SS32_MASK         (1 << QDIS_INST_X86_SS32_SHIFT)
#define QDIS_INST_X86_ADDSEG_MASK       (1 << QDIS_INST_X86_ADDSEG_SHIFT)
#define QDIS_INST_X86_PE_MASK           (1 << QDIS_INST_X86_PE_SHIFT)
#define QDIS_INST_X86_TF_MASK           (1 << QDIS_INST_X86_TF_SHIFT)
#define QDIS_INST_X86_MP_MASK           (1 << QDIS_INST_X86_MP_SHIFT)
#define QDIS_INST_X86_EM_MASK           (1 << QDIS_INST_X86_EM_SHIFT)
#define QDIS_INST_X86_TS_MASK           (1 << QDIS_INST_X86_TS_SHIFT)
#define QDIS_INST_X86_IOPL_MASK         (3 << QDIS_INST_X86_IOPL_SHIFT)
#define QDIS_INST_X86_LMA_MASK          (1 << QDIS_INST_X86_LMA_SHIFT)
#define QDIS_INST_X86_CS64_MASK         (1 << QDIS_INST_X86_CS64_SHIFT)
#define QDIS_INST_X86_RF_MASK           (1 << QDIS_INST_X86_RF_SHIFT)
#define QDIS_INST_X86_VM_MASK           (1 << QDIS_INST_X86_VM_SHIFT)
#define QDIS_INST_X86_AC_MASK           (1 << QDIS_INST_X86_AC_SHIFT)
#define QDIS_INST_X86_SMM_MASK          (1 << QDIS_INST_X86_SMM_SHIFT)
#define QDIS_INST_X86_SVME_MASK         (1 << QDIS_INST_X86_SVME_SHIFT)
#define QDIS_INST_X86_SVMI_MASK         (1 << QDIS_INST_X86_SVMI_SHIFT)
#define QDIS_INST_X86_OSFXSR_MASK       (1 << QDIS_INST_X86_OSFXSR_SHIFT)
#define QDIS_INST_X86_SMAP_MASK         (1 << QDIS_INST_X86_SMAP_SHIFT)

/* A few useful selections */
#define QDIS_IFLAGS_DEFAULT_ARM         (QDIS_INST_ARM_VFPEN_MASK)
#define QDIS_IFLAGS_DEFAULT_THUMB       (QDIS_INST_ARM_VFPEN_MASK | QDIS_INST_ARM_THUMB_MASK)
#define QDIS_IFLAGS_DEFAULT_I386        (QDIS_INST_X86_PE_MASK | QDIS_INST_X86_CS32_MASK | QDIS_INST_X86_SS32_MASK)
#define QDIS_IFLAGS_DEFAULT_AMD64       (QDIS_INST_X86_PE_MASK | QDIS_INST_X86_CS32_MASK | \
                                       QDIS_INST_X86_SS32_MASK | QDIS_INST_X86_CS64_MASK | QDIS_INST_X86_LMA_MASK)

typedef struct QDisassembler_ QDisassembler;

typedef enum {
    QDIS_OPTIMIZE_NONE = 0x0,
    QDIS_OPTIMIZE_LIVENESS = 0x1,
    QDIS_OPTIMIZE_GENERAL = 0x2,
    QDIS_OPTIMIZE_FULL = QDIS_OPTIMIZE_LIVENESS | QDIS_OPTIMIZE_GENERAL
} QDisOptimizeFlags;

/* Symbol type */
typedef enum
{
    QDIS_SYM_LOCAL = 1, // Local temp
    QDIS_SYM_TEMP = 2   // Normal temp
} QDisSymType;

/* Symbol or argument size */
typedef enum
{
    QDIS_SIZE_UNKNOWN = 0,
    QDIS_SIZE_8  = 8,
    QDIS_SIZE_16 = 16,
    QDIS_SIZE_32 = 32,
    QDIS_SIZE_64 = 64
} QDisBitsize;

/* Temp symbol description */
typedef struct
{
    QDisSymType type;
    QDisBitsize size;
} QDisSym;

/* Condition code */
typedef enum
{
    /* non-signed */
    QDIS_COND_NEVER  = 0 | 0 | 0 | 0,
    QDIS_COND_ALWAYS = 0 | 0 | 0 | 1,
    QDIS_COND_EQ     = 8 | 0 | 0 | 0,
    QDIS_COND_NE     = 8 | 0 | 0 | 1,
    /* signed */
    QDIS_COND_LT     = 0 | 0 | 2 | 0,
    QDIS_COND_GE     = 0 | 0 | 2 | 1,
    QDIS_COND_LE     = 8 | 0 | 2 | 0,
    QDIS_COND_GT     = 8 | 0 | 2 | 1,
    /* unsigned */
    QDIS_COND_LTU    = 0 | 4 | 0 | 0,
    QDIS_COND_GEU    = 0 | 4 | 0 | 1,
    QDIS_COND_LEU    = 8 | 4 | 0 | 0,
    QDIS_COND_GTU    = 8 | 4 | 0 | 1,
} QDisConditionCode;

typedef struct
{
    uint16_t opcode;
    uint8_t args; // Number of arguments
} QDisOp;

/* Argument flags */
typedef enum
{
    QDIS_ARG_GLOBAL = 0x1, // global offset
    QDIS_ARG_TEMP = 0x2,  // temp symbol id
    QDIS_ARG_COND = 0x8,   // condition code (DisConditionCode)
    QDIS_ARG_LABEL = 0x10,  // label id
    QDIS_ARG_CALLFLAGS = 0x40, // DisCallFlags
    QDIS_ARG_CALLTARGET = 0x80, // Target of call instruction
    QDIS_ARG_INPUT = 0x100,  // Input argument
    QDIS_ARG_OUTPUT = 0x200, // Output argument
    QDIS_ARG_CONSTANT = 0x400 // Constant (immediate) argument
} QDisArgFlags;

typedef uint64_t QDisVal; // 64 bit on every platform

/* Argument description */
typedef struct
{
    QDisVal value;
    QDisBitsize size; // only set for QDIS_ARG_CONSTANT
    uint16_t flags; // DisArgFlags
} QDisArg;

/* Opcodes (from: tcg_opc.h) */
typedef enum
{
    QDIS_OP_END = 0,
    QDIS_OP_NOP = 1,
    QDIS_OP_NOP1 = 2,
    QDIS_OP_NOP2 = 3,
    QDIS_OP_NOP3 = 4,
    QDIS_OP_NOPN = 5,
    QDIS_OP_DISCARD = 6,
    QDIS_OP_SET_LABEL = 7,
    QDIS_OP_CALL = 8,
    QDIS_OP_BR = 9,
    QDIS_OP_MOV_I32 = 10,
    QDIS_OP_MOVI_I32 = 11,
    QDIS_OP_SETCOND_I32 = 12,
    QDIS_OP_MOVCOND_I32 = 13,
    QDIS_OP_LD8U_I32 = 14,
    QDIS_OP_LD8S_I32 = 15,
    QDIS_OP_LD16U_I32 = 16,
    QDIS_OP_LD16S_I32 = 17,
    QDIS_OP_LD_I32 = 18,
    QDIS_OP_ST8_I32 = 19,
    QDIS_OP_ST16_I32 = 20,
    QDIS_OP_ST_I32 = 21,
    QDIS_OP_ADD_I32 = 22,
    QDIS_OP_SUB_I32 = 23,
    QDIS_OP_MUL_I32 = 24,
    QDIS_OP_DIV_I32 = 25,
    QDIS_OP_DIVU_I32 = 26,
    QDIS_OP_REM_I32 = 27,
    QDIS_OP_REMU_I32 = 28,
    QDIS_OP_DIV2_I32 = 29,
    QDIS_OP_DIVU2_I32 = 30,
    QDIS_OP_AND_I32 = 31,
    QDIS_OP_OR_I32 = 32,
    QDIS_OP_XOR_I32 = 33,
    QDIS_OP_SHL_I32 = 34,
    QDIS_OP_SHR_I32 = 35,
    QDIS_OP_SAR_I32 = 36,
    QDIS_OP_ROTL_I32 = 37,
    QDIS_OP_ROTR_I32 = 38,
    QDIS_OP_DEPOSIT_I32 = 39,
    QDIS_OP_BRCOND_I32 = 40,
    QDIS_OP_ADD2_I32 = 41,
    QDIS_OP_SUB2_I32 = 42,
    QDIS_OP_BRCOND2_I32 = 43,
    QDIS_OP_MULU2_I32 = 44,
    QDIS_OP_SETCOND2_I32 = 45,
    QDIS_OP_EXT8S_I32 = 46,
    QDIS_OP_EXT16S_I32 = 47,
    QDIS_OP_EXT8U_I32 = 48,
    QDIS_OP_EXT16U_I32 = 49,
    QDIS_OP_BSWAP16_I32 = 50,
    QDIS_OP_BSWAP32_I32 = 51,
    QDIS_OP_NOT_I32 = 52,
    QDIS_OP_NEG_I32 = 53,
    QDIS_OP_ANDC_I32 = 54,
    QDIS_OP_ORC_I32 = 55,
    QDIS_OP_EQV_I32 = 56,
    QDIS_OP_NAND_I32 = 57,
    QDIS_OP_NOR_I32 = 58,
    QDIS_OP_MOV_I64 = 59,
    QDIS_OP_MOVI_I64 = 60,
    QDIS_OP_SETCOND_I64 = 61,
    QDIS_OP_MOVCOND_I64 = 62,
    QDIS_OP_LD8U_I64 = 63,
    QDIS_OP_LD8S_I64 = 64,
    QDIS_OP_LD16U_I64 = 65,
    QDIS_OP_LD16S_I64 = 66,
    QDIS_OP_LD32U_I64 = 67,
    QDIS_OP_LD32S_I64 = 68,
    QDIS_OP_LD_I64 = 69,
    QDIS_OP_ST8_I64 = 70,
    QDIS_OP_ST16_I64 = 71,
    QDIS_OP_ST32_I64 = 72,
    QDIS_OP_ST_I64 = 73,
    QDIS_OP_ADD_I64 = 74,
    QDIS_OP_SUB_I64 = 75,
    QDIS_OP_MUL_I64 = 76,
    QDIS_OP_DIV_I64 = 77,
    QDIS_OP_DIVU_I64 = 78,
    QDIS_OP_REM_I64 = 79,
    QDIS_OP_REMU_I64 = 80,
    QDIS_OP_DIV2_I64 = 81,
    QDIS_OP_DIVU2_I64 = 82,
    QDIS_OP_AND_I64 = 83,
    QDIS_OP_OR_I64 = 84,
    QDIS_OP_XOR_I64 = 85,
    QDIS_OP_SHL_I64 = 86,
    QDIS_OP_SHR_I64 = 87,
    QDIS_OP_SAR_I64 = 88,
    QDIS_OP_ROTL_I64 = 89,
    QDIS_OP_ROTR_I64 = 90,
    QDIS_OP_DEPOSIT_I64 = 91,
    QDIS_OP_BRCOND_I64 = 92,
    QDIS_OP_EXT8S_I64 = 93,
    QDIS_OP_EXT16S_I64 = 94,
    QDIS_OP_EXT32S_I64 = 95,
    QDIS_OP_EXT8U_I64 = 96,
    QDIS_OP_EXT16U_I64 = 97,
    QDIS_OP_EXT32U_I64 = 98,
    QDIS_OP_BSWAP16_I64 = 99,
    QDIS_OP_BSWAP32_I64 = 100,
    QDIS_OP_BSWAP64_I64 = 101,
    QDIS_OP_NOT_I64 = 102,
    QDIS_OP_NEG_I64 = 103,
    QDIS_OP_ANDC_I64 = 104,
    QDIS_OP_ORC_I64 = 105,
    QDIS_OP_EQV_I64 = 106,
    QDIS_OP_NAND_I64 = 107,
    QDIS_OP_NOR_I64 = 108,
    QDIS_OP_DEBUG_INSN_START = 109,
    QDIS_OP_EXIT_TB = 110,
    QDIS_OP_GOTO_TB = 111,
    QDIS_OP_QEMU_LD8U = 112,
    QDIS_OP_QEMU_LD8S = 113,
    QDIS_OP_QEMU_LD16U = 114,
    QDIS_OP_QEMU_LD16S = 115,
    QDIS_OP_QEMU_LD32 = 116,
    QDIS_OP_QEMU_LD32U = 117,
    QDIS_OP_QEMU_LD32S = 118,
    QDIS_OP_QEMU_LD64 = 119,
    QDIS_OP_QEMU_ST8 = 120,
    QDIS_OP_QEMU_ST16 = 121,
    QDIS_OP_QEMU_ST32 = 122,
    QDIS_OP_QEMU_ST64 = 123,
} QDisOpcode;

/* Instruction types */
typedef enum
{
    QDIS_ITYPE_UNKNOWN=-1,  /* unlabeled instruction */
    QDIS_ITYPE_DEFAULT=0,   /* go to next instruction */
    QDIS_ITYPE_JMP,         /* jump */
    QDIS_ITYPE_JMP_IND,     /* indirect jump */
    QDIS_ITYPE_COND_JMP,    /* conditional jump */
    QDIS_ITYPE_COND_JMP_IND,/* conditional indirect jump */
    QDIS_ITYPE_CALL,        /* call */
    QDIS_ITYPE_CALL_IND,    /* indirect call */
    QDIS_ITYPE_REP,         /* x86 rep */
    QDIS_ITYPE_RET          /* return from function */
} QDisInstType;

/* Hint for output buffer size.
 * Microcode output is generally guaranteed to stay within this size.
 */
#define QDIS_BUFFER_SIZE 16384

/* Invalid symbol id */
#define QDIS_INVALID ((size_t)-1)

/* Disassembly result structure, as written to output buffer */
typedef struct
{
    size_t num_ops;  // Number of opcodes
    QDisOp *ops;     // Pointer to opcodes
    size_t num_args; // Total number of arguments
    QDisArg *args;   // Pointer to arguments
    size_t num_syms; // Total number of temp symbols
    QDisSym *syms; // Pointer to temp symbols
    size_t num_labels; // Total number of labels
    QDisInstType inst_type; // Instruction type
    size_t _padding[8];
} QDisResult;

typedef enum {
    /* Strings: General */
    QDIS_INFO_OP = 1,      // opcode name
    QDIS_INFO_COND = 2,    // condition code name
    QDIS_INFO_CALLFLAG = 3,// call flag name (DisCallFlags)
    /* Values: General */
    QDIS_INFO_NUM_OPS = 256,
    /* Strings: CPU arch specific */
    QDIS_INFO_HELPER = 513,   // helper name by ordinal
    QDIS_INFO_HELPER_BY_ADDR = 514, // helper name by address
    QDIS_INFO_GLOBAL = 515,   // global (register) name
    /* Values: CPU arch specific */
    QDIS_INFO_PC_OFFSET = 768,   // Program counter register (env offset)
    QDIS_INFO_SP_OFFSET = 769,   // Stack pointer register (env offset)
    QDIS_INFO_NUM_HELPERS = 770, // Number of helper functions defined
    QDIS_INFO_NUM_GLOBALS = 771, // Number of globals defined
    QDIS_INFO_GLOBAL_SIZE = 772, // global (register) bit size (DisBitsize)
    QDIS_INFO_GLOBAL_OFFSET = 773, // global (register) address into environment
    QDIS_INFO_STATE_SIZE = 774,  // environment size
} QDisInfoType;

/* Call flags */
typedef enum
{
    /* Helper does not read globals (either directly or through an exception). It
       implies TCG_CALL_NO_WRITE_GLOBALS. */
    QDIS_CALL_NO_READ_GLOBALS  = 0x0010,
    /* Helper does not write globals */
    QDIS_CALL_NO_WRITE_GLOBALS = 0x0020,
    /* Helper can be safely suppressed if the return value is not used. */
    QDIS_CALL_NO_SIDE_EFFECTS  = 0x0040
} QDisCallFlags;

/* features is a list of features, terminated with QDIS_FEATURE_END.
 * If NULL, enable as many features as possible (without conflicts).
 *
 * Returns NULL on failure.
 * */
QDisassembler *qdis_Create(QDisTarget tgt, QDisCPUFeature *feat);

/* Disassemble an instruction.
 * flags: CPU specific instruction decoding flags
 */
QDisStatus qdis_Disassemble(QDisassembler *dis, uint8_t *inst, size_t size, uint64_t pc, uint64_t inst_flags, uint32_t optimize,
        void *outbuffer, size_t outsize);

/* Look up name for opcode or helper.
 * Returns the requested name or NULL if no such info.
 */
const char *qdis_LookupName(QDisassembler *dis, QDisInfoType type, size_t id);

/* Look up integer-valued value.
 * */
size_t qdis_LookupValue(QDisassembler *dis, QDisInfoType type, size_t id);

/* Dump status for debugging.
 */
void qdis_Dump(QDisassembler *dis);

/* Destroy a disassembler.
 */
void qdis_Destroy(QDisassembler *dis);

#endif
