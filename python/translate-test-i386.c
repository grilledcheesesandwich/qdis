#define TARGET i386
#include "common.h"

/* CPU specific initialization */
static CPUArchState *init_target(DisassCPUFeature *features)
{
    optimize_flags_init();
    CPUX86State *env = (CPUX86State*)malloc(sizeof(CPUX86State));
    memset(env, 0, sizeof(CPUX86State));
    cpu_single_env = env;
    // Just blanket enable all features for now
    env->cpuid_features = 0xFFFFFFFF;
    env->cpuid_ext_features = 0xFFFFFFF;
    env->cpuid_ext2_features = 0xFFFFFFF;
    env->cpuid_7_0_ebx_features = 0xFFFFFFFF;
    return env;
}

int main(int argc, char **argv)
{
    Disassembler *dis = i386_Create(NULL);
    // Now let's disassemble an instruction!
    // 48 81 eb 28 ee 67 00    sub    $0x67ee28,%rbx
    unsigned char inst[] = {0x48, 0x81, 0xeb, 0x28, 0xee, 0x67, 0x00};
    //unsigned char inst[] = {0x73, 0x24};
    //
    uint64_t inst_flags = (HF_CS64_MASK | HF_LMA_MASK);
    if(i386_Disassemble(dis, inst, sizeof(inst), 0x1000, inst_flags, true) != DIS_OK)
        printf("Warning: access out of bounds during disassembly\n");

    i386_Dump(dis);
    // dump output
    tcg_dump_ops(dis->ctx);

}
