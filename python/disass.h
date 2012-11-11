#ifndef H_DISASS
#define H_DISASS
#include <stdbool.h>
#include <stdlib.h>
#include <stdint.h>
/* qemu instruction decoder -- external interface */
// Return status values
typedef enum
{
    DIS_OK = 0,
    DIS_ERR_OUT_OF_BOUNDS_ACCESS = 1, /* instruction ran outside buffer */
    DIS_ERR_BUFFER_TOO_SMALL = 2,  /* output buffer too small */
    DIS_ERR_NULLPOINTER = 3, /* unexpected NULL argument */
    DIS_ERR_ALIGNMENT = 4, /* output buffer not aligned to 8 bytes */
} DisStatus;

typedef enum
{
    // (Address) register bitsize
    DIS_TGT_8BIT  = 0x0000, // not supported
    DIS_TGT_16BIT = 0x1000, // not supported
    DIS_TGT_32BIT = 0x2000,
    DIS_TGT_64BIT = 0x3000,
    // Supported architectures
    DIS_TGT_ARM = 0 | DIS_TGT_32BIT,
    DIS_TGT_X86_32 = 1 | DIS_TGT_32BIT,
    DIS_TGT_X86_64 = 1 | DIS_TGT_64BIT,
    DIS_TGT_ALPHA = 2 | DIS_TGT_64BIT,
    DIS_TGT_CRIS = 3 | DIS_TGT_32BIT,
    DIS_TGT_LM32 = 4 | DIS_TGT_32BIT,
    DIS_TGT_M68K = 5 | DIS_TGT_32BIT,
    DIS_TGT_MICROBLAZE = 6 | DIS_TGT_32BIT,
    DIS_TGT_MIPS_32 = 7 | DIS_TGT_32BIT,
    DIS_TGT_MIPS_64 = 7 | DIS_TGT_64BIT,
    DIS_TGT_OPENRISC = 8 | DIS_TGT_32BIT,
    DIS_TGT_PPC_32 = 9 | DIS_TGT_32BIT,
    DIS_TGT_PPC_64 = 9 | DIS_TGT_64BIT,
    DIS_TGT_S390X = 10 | DIS_TGT_64BIT,
    DIS_TGT_SH4 = 11 | DIS_TGT_32BIT,
    DIS_TGT_SPARC_32 = 12 | DIS_TGT_32BIT,
    DIS_TGT_SPARC_64 = 12 | DIS_TGT_64BIT,
    DIS_TGT_UNICORE32 = 13 | DIS_TGT_32BIT,
    DIS_TGT_XTENSA = 14 | DIS_TGT_32BIT
} DisTarget;

// Tokens for CPU features
// XX use ELF hwcap flags here?
typedef enum
{
    DIS_FEATURE_END = 0,
    DIS_ARM_FEATURE_VFP,
    DIS_ARM_FEATURE_AUXCR,  /* ARM1026 Auxiliary control register.  */
    DIS_ARM_FEATURE_XSCALE, /* Intel XScale extensions.  */
    DIS_ARM_FEATURE_IWMMXT, /* Intel iwMMXt extension.  */
    DIS_ARM_FEATURE_V6,
    DIS_ARM_FEATURE_V6K,
    DIS_ARM_FEATURE_V7,
    DIS_ARM_FEATURE_THUMB2,
    DIS_ARM_FEATURE_MPU,    /* Only has Memory Protection Unit, not full MMU.  */
    DIS_ARM_FEATURE_VFP3,
    DIS_ARM_FEATURE_VFP_FP16,
    DIS_ARM_FEATURE_NEON,
    DIS_ARM_FEATURE_THUMB_DIV, /* divide supported in Thumb encoding */
    DIS_ARM_FEATURE_M, /* Microcontroller profile.  */
    DIS_ARM_FEATURE_OMAPCP, /* OMAP specific CP15 ops handling.  */
    DIS_ARM_FEATURE_THUMB2EE,
    DIS_ARM_FEATURE_V7MP,    /* v7 Multiprocessing Extensions */
    DIS_ARM_FEATURE_V4T,
    DIS_ARM_FEATURE_V5,
    DIS_ARM_FEATURE_STRONGARM,
    DIS_ARM_FEATURE_VAPA, /* cp15 VA to PA lookups */
    DIS_ARM_FEATURE_ARM_DIV, /* divide supported in ARM encoding */
    DIS_ARM_FEATURE_VFP4, /* VFPv4 (implies that NEON is v2) */
    DIS_ARM_FEATURE_GENERIC_TIMER,
    DIS_ARM_FEATURE_MVFR, /* Media and VFP Feature Registers 0 and 1 */
    DIS_ARM_FEATURE_DUMMY_C15_REGS, /* RAZ/WI all of cp15 crn=15 */
    DIS_ARM_FEATURE_CACHE_TEST_CLEAN, /* 926/1026 style test-and-clean ops */
    DIS_ARM_FEATURE_CACHE_DIRTY_REG, /* 1136/1176 cache dirty status register */
    DIS_ARM_FEATURE_CACHE_BLOCK_OPS, /* v6 optional cache block operations */
    DIS_ARM_FEATURE_MPIDR, /* has cp15 MPIDR */
    DIS_ARM_FEATURE_PXN, /* has Privileged Execute Never bit */
    DIS_ARM_FEATURE_LPAE, /* has Large Physical Address Extension */
    // TODO i386 etc
} DisCPUFeature;

/* XXX need a more standarized way that doesn't rely on qemu internals as much? */
/* arm */
#define DIS_INST_ARM_THUMB_SHIFT      0
#define DIS_INST_ARM_THUMB_MASK       (1 << DIS_INST_ARM_THUMB_SHIFT)
#define DIS_INST_ARM_VECLEN_SHIFT     1
#define DIS_INST_ARM_VECLEN_MASK      (0x7 << DIS_INST_ARM_VECLEN_SHIFT)
#define DIS_INST_ARM_VECSTRIDE_SHIFT  4
#define DIS_INST_ARM_VECSTRIDE_MASK   (0x3 << DIS_INST_ARM_VECSTRIDE_SHIFT)
#define DIS_INST_ARM_PRIV_SHIFT       6
#define DIS_INST_ARM_PRIV_MASK        (1 << DIS_INST_ARM_PRIV_SHIFT)
#define DIS_INST_ARM_VFPEN_SHIFT      7
#define DIS_INST_ARM_VFPEN_MASK       (1 << DIS_INST_ARM_VFPEN_SHIFT)
#define DIS_INST_ARM_CONDEXEC_SHIFT   8
#define DIS_INST_ARM_CONDEXEC_MASK    (0xff << DIS_INST_ARM_CONDEXEC_SHIFT)
#define DIS_INST_ARM_BSWAP_CODE_SHIFT 16
#define DIS_INST_ARM_BSWAP_CODE_MASK  (1 << DIS_INST_ARM_BSWAP_CODE_SHIFT)

/* x86 */
#define DIS_INST_X86_CPL_SHIFT         0
#define DIS_INST_X86_SOFTMMU_SHIFT     2 /* true if soft mmu is being used */
#define DIS_INST_X86_INHIBIT_IRQ_SHIFT 3 /* true if hardware interrupts must be disabled for next instruction */
#define DIS_INST_X86_CS32_SHIFT        4 /* 16 or 32 segments */
#define DIS_INST_X86_SS32_SHIFT        5
#define DIS_INST_X86_ADDSEG_SHIFT      6 /* zero base for DS, ES and SS : can be '0' only in 32 bit CS segment */
#define DIS_INST_X86_PE_SHIFT          7 /* copy of CR0.PE (protected mode) */
#define DIS_INST_X86_TF_SHIFT          8 /* must be same as eflags */
#define DIS_INST_X86_MP_SHIFT          9 /* the order must be MP, EM, TS */
#define DIS_INST_X86_EM_SHIFT         10
#define DIS_INST_X86_TS_SHIFT         11
#define DIS_INST_X86_IOPL_SHIFT       12 /* must be same as eflags */
#define DIS_INST_X86_LMA_SHIFT        14 /* only used on x86_64: long mode active */
#define DIS_INST_X86_CS64_SHIFT       15 /* only used on x86_64: 64 bit code segment  */
#define DIS_INST_X86_RF_SHIFT         16 /* must be same as eflags */
#define DIS_INST_X86_VM_SHIFT         17 /* must be same as eflags */
#define DIS_INST_X86_AC_SHIFT         18 /* must be same as eflags */
#define DIS_INST_X86_SMM_SHIFT        19 /* CPU in SMM mode */
#define DIS_INST_X86_SVME_SHIFT       20 /* SVME enabled (copy of EFER.SVME) */
#define DIS_INST_X86_SVMI_SHIFT       21 /* SVM intercepts are active */
#define DIS_INST_X86_OSFXSR_SHIFT     22 /* CR4.OSFXSR */
#define DIS_INST_X86_SMAP_SHIFT       23 /* CR4.SMAP */

#define DIS_INST_X86_CPL_MASK          (3 << DIS_INST_X86_CPL_SHIFT)
#define DIS_INST_X86_SOFTMMU_MASK      (1 << DIS_INST_X86_SOFTMMU_SHIFT)
#define DIS_INST_X86_INHIBIT_IRQ_MASK  (1 << DIS_INST_X86_INHIBIT_IRQ_SHIFT)
#define DIS_INST_X86_CS32_MASK         (1 << DIS_INST_X86_CS32_SHIFT)
#define DIS_INST_X86_SS32_MASK         (1 << DIS_INST_X86_SS32_SHIFT)
#define DIS_INST_X86_ADDSEG_MASK       (1 << DIS_INST_X86_ADDSEG_SHIFT)
#define DIS_INST_X86_PE_MASK           (1 << DIS_INST_X86_PE_SHIFT)
#define DIS_INST_X86_TF_MASK           (1 << DIS_INST_X86_TF_SHIFT)
#define DIS_INST_X86_MP_MASK           (1 << DIS_INST_X86_MP_SHIFT)
#define DIS_INST_X86_EM_MASK           (1 << DIS_INST_X86_EM_SHIFT)
#define DIS_INST_X86_TS_MASK           (1 << DIS_INST_X86_TS_SHIFT)
#define DIS_INST_X86_IOPL_MASK         (3 << DIS_INST_X86_IOPL_SHIFT)
#define DIS_INST_X86_LMA_MASK          (1 << DIS_INST_X86_LMA_SHIFT)
#define DIS_INST_X86_CS64_MASK         (1 << DIS_INST_X86_CS64_SHIFT)
#define DIS_INST_X86_RF_MASK           (1 << DIS_INST_X86_RF_SHIFT)
#define DIS_INST_X86_VM_MASK           (1 << DIS_INST_X86_VM_SHIFT)
#define DIS_INST_X86_AC_MASK           (1 << DIS_INST_X86_AC_SHIFT)
#define DIS_INST_X86_SMM_MASK          (1 << DIS_INST_X86_SMM_SHIFT)
#define DIS_INST_X86_SVME_MASK         (1 << DIS_INST_X86_SVME_SHIFT)
#define DIS_INST_X86_SVMI_MASK         (1 << DIS_INST_X86_SVMI_SHIFT)
#define DIS_INST_X86_OSFXSR_MASK       (1 << DIS_INST_X86_OSFXSR_SHIFT)
#define DIS_INST_X86_SMAP_MASK         (1 << DIS_INST_X86_SMAP_SHIFT)

typedef struct Disassembler_ Disassembler;

typedef enum {
    DIS_OPTIMIZE_NONE = 0x0,
    DIS_OPTIMIZE_LIVENESS = 0x1,
    DIS_OPTIMIZE_GENERAL = 0x2,
    DIS_OPTIMIZE_FULL = DIS_OPTIMIZE_LIVENESS | DIS_OPTIMIZE_GENERAL
} DisOptimizeFlags;

/* Symbol type */
typedef enum
{
    DIS_SYM_LOCAL = 1, // Local temp
    DIS_SYM_TEMP = 2   // Normal temp
} DisSymType;

/* Symbol or argument size */
typedef enum
{
    DIS_SIZE_UNKNOWN = 0,
    DIS_SIZE_8  = 8,
    DIS_SIZE_16 = 16,
    DIS_SIZE_32 = 32,
    DIS_SIZE_64 = 64
} DisBitsize;

/* Temp symbol description */
typedef struct
{
    DisSymType type;
    DisBitsize size;
} DisSym;

/* Condition code */
typedef enum
{
    /* non-signed */
    DIS_COND_NEVER  = 0 | 0 | 0 | 0,
    DIS_COND_ALWAYS = 0 | 0 | 0 | 1,
    DIS_COND_EQ     = 8 | 0 | 0 | 0,
    DIS_COND_NE     = 8 | 0 | 0 | 1,
    /* signed */
    DIS_COND_LT     = 0 | 0 | 2 | 0,
    DIS_COND_GE     = 0 | 0 | 2 | 1,
    DIS_COND_LE     = 8 | 0 | 2 | 0,
    DIS_COND_GT     = 8 | 0 | 2 | 1,
    /* unsigned */
    DIS_COND_LTU    = 0 | 4 | 0 | 0,
    DIS_COND_GEU    = 0 | 4 | 0 | 1,
    DIS_COND_LEU    = 8 | 4 | 0 | 0,
    DIS_COND_GTU    = 8 | 4 | 0 | 1,
} DisConditionCode;

typedef struct
{
    uint16_t opcode;
    uint8_t args; // Number of arguments
} DisOp;

/* Argument flags */
typedef enum
{
    DIS_ARG_GLOBAL = 0x1, // global offset
    DIS_ARG_TEMP = 0x2,  // temp symbol id
    //DIS_ARG_ENVPTR = 0x4,  // "env" pointer
    DIS_ARG_COND = 0x8,   // condition code (DisConditionCode)
    DIS_ARG_DUMMY = 0x10,  // dummy argument (for alignment)
    DIS_ARG_CALLFLAGS = 0x40, // DisCallFlags
    DIS_ARG_CALLTARGET = 0x80, // Target of call instruction
    DIS_ARG_INPUT = 0x100,  // Input argument
    DIS_ARG_OUTPUT = 0x200, // Output argument
    DIS_ARG_CONSTANT = 0x400 // Constant (immediate) argument
} DisArgFlags;

/* Argument description */
typedef struct
{
    size_t value;
    DisBitsize size; // only set for DIS_ARG_CONSTANT
    uint16_t flags; // DisArgFlags
} DisArg;

/* Opcodes (from: tcg_opc.h) */
typedef enum
{
    DIS_OP_END = 0,
    DIS_OP_NOP = 1,
    DIS_OP_NOP1 = 2,
    DIS_OP_NOP2 = 3,
    DIS_OP_NOP3 = 4,
    DIS_OP_NOPN = 5,
    DIS_OP_DISCARD = 6,
    DIS_OP_SET_LABEL = 7,
    DIS_OP_CALL = 8,
    DIS_OP_BR = 9,
    DIS_OP_MOV_I32 = 10,
    DIS_OP_MOVI_I32 = 11,
    DIS_OP_SETCOND_I32 = 12,
    DIS_OP_MOVCOND_I32 = 13,
    DIS_OP_LD8U_I32 = 14,
    DIS_OP_LD8S_I32 = 15,
    DIS_OP_LD16U_I32 = 16,
    DIS_OP_LD16S_I32 = 17,
    DIS_OP_LD_I32 = 18,
    DIS_OP_ST8_I32 = 19,
    DIS_OP_ST16_I32 = 20,
    DIS_OP_ST_I32 = 21,
    DIS_OP_ADD_I32 = 22,
    DIS_OP_SUB_I32 = 23,
    DIS_OP_MUL_I32 = 24,
    DIS_OP_DIV_I32 = 25,
    DIS_OP_DIVU_I32 = 26,
    DIS_OP_REM_I32 = 27,
    DIS_OP_REMU_I32 = 28,
    DIS_OP_DIV2_I32 = 29,
    DIS_OP_DIVU2_I32 = 30,
    DIS_OP_AND_I32 = 31,
    DIS_OP_OR_I32 = 32,
    DIS_OP_XOR_I32 = 33,
    DIS_OP_SHL_I32 = 34,
    DIS_OP_SHR_I32 = 35,
    DIS_OP_SAR_I32 = 36,
    DIS_OP_ROTL_I32 = 37,
    DIS_OP_ROTR_I32 = 38,
    DIS_OP_DEPOSIT_I32 = 39,
    DIS_OP_BRCOND_I32 = 40,
    DIS_OP_ADD2_I32 = 41,
    DIS_OP_SUB2_I32 = 42,
    DIS_OP_BRCOND2_I32 = 43,
    DIS_OP_MULU2_I32 = 44,
    DIS_OP_SETCOND2_I32 = 45,
    DIS_OP_EXT8S_I32 = 46,
    DIS_OP_EXT16S_I32 = 47,
    DIS_OP_EXT8U_I32 = 48,
    DIS_OP_EXT16U_I32 = 49,
    DIS_OP_BSWAP16_I32 = 50,
    DIS_OP_BSWAP32_I32 = 51,
    DIS_OP_NOT_I32 = 52,
    DIS_OP_NEG_I32 = 53,
    DIS_OP_ANDC_I32 = 54,
    DIS_OP_ORC_I32 = 55,
    DIS_OP_EQV_I32 = 56,
    DIS_OP_NAND_I32 = 57,
    DIS_OP_NOR_I32 = 58,
    DIS_OP_MOV_I64 = 59,
    DIS_OP_MOVI_I64 = 60,
    DIS_OP_SETCOND_I64 = 61,
    DIS_OP_MOVCOND_I64 = 62,
    DIS_OP_LD8U_I64 = 63,
    DIS_OP_LD8S_I64 = 64,
    DIS_OP_LD16U_I64 = 65,
    DIS_OP_LD16S_I64 = 66,
    DIS_OP_LD32U_I64 = 67,
    DIS_OP_LD32S_I64 = 68,
    DIS_OP_LD_I64 = 69,
    DIS_OP_ST8_I64 = 70,
    DIS_OP_ST16_I64 = 71,
    DIS_OP_ST32_I64 = 72,
    DIS_OP_ST_I64 = 73,
    DIS_OP_ADD_I64 = 74,
    DIS_OP_SUB_I64 = 75,
    DIS_OP_MUL_I64 = 76,
    DIS_OP_DIV_I64 = 77,
    DIS_OP_DIVU_I64 = 78,
    DIS_OP_REM_I64 = 79,
    DIS_OP_REMU_I64 = 80,
    DIS_OP_DIV2_I64 = 81,
    DIS_OP_DIVU2_I64 = 82,
    DIS_OP_AND_I64 = 83,
    DIS_OP_OR_I64 = 84,
    DIS_OP_XOR_I64 = 85,
    DIS_OP_SHL_I64 = 86,
    DIS_OP_SHR_I64 = 87,
    DIS_OP_SAR_I64 = 88,
    DIS_OP_ROTL_I64 = 89,
    DIS_OP_ROTR_I64 = 90,
    DIS_OP_DEPOSIT_I64 = 91,
    DIS_OP_BRCOND_I64 = 92,
    DIS_OP_EXT8S_I64 = 93,
    DIS_OP_EXT16S_I64 = 94,
    DIS_OP_EXT32S_I64 = 95,
    DIS_OP_EXT8U_I64 = 96,
    DIS_OP_EXT16U_I64 = 97,
    DIS_OP_EXT32U_I64 = 98,
    DIS_OP_BSWAP16_I64 = 99,
    DIS_OP_BSWAP32_I64 = 100,
    DIS_OP_BSWAP64_I64 = 101,
    DIS_OP_NOT_I64 = 102,
    DIS_OP_NEG_I64 = 103,
    DIS_OP_ANDC_I64 = 104,
    DIS_OP_ORC_I64 = 105,
    DIS_OP_EQV_I64 = 106,
    DIS_OP_NAND_I64 = 107,
    DIS_OP_NOR_I64 = 108,
    DIS_OP_DEBUG_INSN_START = 109,
    DIS_OP_EXIT_TB = 110,
    DIS_OP_GOTO_TB = 111,
    DIS_OP_QEMU_LD8U = 112,
    DIS_OP_QEMU_LD8S = 113,
    DIS_OP_QEMU_LD16U = 114,
    DIS_OP_QEMU_LD16S = 115,
    DIS_OP_QEMU_LD32 = 116,
    DIS_OP_QEMU_LD32U = 117,
    DIS_OP_QEMU_LD32S = 118,
    DIS_OP_QEMU_LD64 = 119,
    DIS_OP_QEMU_ST8 = 120,
    DIS_OP_QEMU_ST16 = 121,
    DIS_OP_QEMU_ST32 = 122,
    DIS_OP_QEMU_ST64 = 123,
} DisOpcode;

/* Hint for output buffer size.
 * Microcode output is generally guaranteed to stay within this size.
 */
#define DIS_BUFFER_SIZE 16384

/* Invalid symbol id */
#define DIS_INVALID ((size_t)-1)

/* Disassembly result structure, as written to output buffer */
typedef struct
{
    size_t num_ops;  // Number of opcodes
    DisOp *ops;     // Pointer to opcodes
    size_t num_args; // Total number of arguments
    DisArg *args;   // Pointer to arguments
    size_t num_syms; // Total number of temp symbols
    DisSym *syms; // Pointer to temp symbols
    size_t _padding[10];
} DisResult;

typedef enum {
    /* Strings: General */
    DIS_INFO_OP = 1,      // opcode name
    DIS_INFO_COND = 2,    // condition code name
    /* Values: General */
    DIS_INFO_NUM_OPS = 256,
    /* Strings: CPU arch specific */
    DIS_INFO_HELPER = 513,   // helper name by ordinal
    DIS_INFO_HELPER_BY_ADDR = 514, // helper name by address
    DIS_INFO_GLOBAL = 515,   // global (register) name
    /* Values: CPU arch specific */
    DIS_INFO_PC_OFFSET = 768,   // Program counter register (env offset)
    DIS_INFO_SP_OFFSET = 769,   // Stack pointer register (env offset)
    DIS_INFO_NUM_HELPERS = 770, // Number of helper functions defined
    DIS_INFO_NUM_GLOBALS = 771, // Number of globals defined
    DIS_INFO_GLOBAL_SIZE = 772, // global (register) bit size (DisBitsize)
    DIS_INFO_GLOBAL_OFFSET = 773, // global (register) address into environment
    DIS_INFO_STATE_SIZE = 774,  // environment size
} DisInfoType;

/* Call flags */
typedef enum
{
    /* Helper does not read globals (either directly or through an exception). It
       implies TCG_CALL_NO_WRITE_GLOBALS. */
    DIS_CALL_NO_READ_GLOBALS  = 0x0010,
    /* Helper does not write globals */
    DIS_CALL_NO_WRITE_GLOBALS = 0x0020,
    /* Helper can be safely suppressed if the return value is not used. */
    DIS_CALL_NO_SIDE_EFFECTS  = 0x0040
} DisCallFlags;

/* features is a list of features, terminated with DIS_FEATURE_END.
 * If NULL, enable as many features as possible (without conflicts).
 *
 * Returns NULL on failure.
 * */
Disassembler *dis_Create(DisTarget tgt, DisCPUFeature *feat);

/* Disassemble an instruction.
 * flags: CPU specific instruction decoding flags
 */
DisStatus dis_Disassemble(Disassembler *dis, uint8_t *inst, size_t size, uint64_t pc, uint64_t inst_flags, uint32_t optimize,
        void *outbuffer, size_t outsize);

/* Look up name for opcode or helper.
 * Returns the requested name or NULL if no such info.
 */
const char *dis_LookupName(Disassembler *dis, DisInfoType type, size_t id);

/* Look up integer-valued value.
 * */
size_t dis_LookupValue(Disassembler *dis, DisInfoType type, size_t id);

/* Dump status for debugging.
 */
void dis_Dump(Disassembler *dis);

/* Destroy a disassembler.
 */
void dis_Destroy(Disassembler *dis);

#endif
