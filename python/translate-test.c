#include "disass.h"
#include <stdio.h>

void print_info(Disassembler *dis)
{
    size_t pc_idx = dis_LookupValue(dis, DIS_INFO_PC_OFFSET, 0);
    size_t sp_idx = dis_LookupValue(dis, DIS_INFO_SP_OFFSET, 0);
    size_t num_helpers = dis_LookupValue(dis, DIS_INFO_NUM_HELPERS, 0);
    size_t num_globals = dis_LookupValue(dis, DIS_INFO_NUM_GLOBALS, 0);
    size_t num_ops = dis_LookupValue(dis, DIS_INFO_NUM_OPS, 0);
    size_t i = 0;
    printf("State size: 0x%x\n", (int)dis_LookupValue(dis, DIS_INFO_STATE_SIZE, 0));
    printf("PC register: 0x%x\n", (int)pc_idx);
    printf("SP register: 0x%x\n", (int)sp_idx);
    /*
    printf("Ops:\n");
    for(i=0; i<num_ops; ++i)
    {
        printf("  %i %s\n", i, dis_LookupName(dis, DIS_INFO_OP, i));
    }
    */
    printf("Helpers:\n");
    for(i=0; i<num_helpers; ++i)
    {
        printf("  %i %s\n", i, dis_LookupName(dis, DIS_INFO_HELPER, i));
    }
    printf("Globals:\n");
    for(i=0; i<num_globals; ++i)
    {
        printf("  %i %s (0x%x:%i)\n", i, dis_LookupName(dis, DIS_INFO_GLOBAL, i),
                (int)dis_LookupValue(dis, DIS_INFO_GLOBAL_OFFSET, i),
                (int)dis_LookupValue(dis, DIS_INFO_GLOBAL_SIZE, i));
    }
}

void print_dis_result(Disassembler *dis, DisResult *rv)
{
    int i = 0, j = 0, arg = 0;
    printf("Result: %p\n", rv);
    printf("Number of args: %i\n", (int)rv->num_args);
    printf("Number of syms: %i\n", (int)rv->num_syms);
    for(i=0; i<rv->num_syms; ++i)
    {
        printf("  %i type=%i size=%i\n", (int)i, (int)rv->syms[i].type, (int)rv->syms[i].size);
    }
    printf("Number of ops: %i\n", (int)rv->num_ops);
    for(i=0; i<rv->num_ops; ++i)
    {
        printf("  %i opcode=%s\n", (int)i,
                dis_LookupName(dis, DIS_INFO_OP, rv->ops[i].opcode));
        for(j=0; j<rv->ops[i].args; ++j)
        {
            printf("    %i flags=0x%x value=0x%x size=%i\n", (int)arg,
                    (int)rv->args[arg].flags, (int)rv->args[arg].value, (int)rv->args[arg].size
                  );
            ++arg;
        }
    }
    printf("\n");
}

int main(int argc, char **argv)
{
    Disassembler *dis_arm = dis_Create(DIS_TGT_ARM, NULL);
    void *outbuffer = malloc(DIS_BUFFER_SIZE);

    printf("* ARM\n");
    // Now let's disassemble an instruction!
    //unsigned char inst[] = {0x10,0x40,0x2d,0xe9}; // Push {r4,lr}
    //unsigned char inst[] = {0x0a,0x00,0x00,0x0a}; // Push {r4,lr}
    unsigned char inst[] = {0x02, 0x0a, 0x21, 0xf4}; // Push {r4,lr}
    //
    uint64_t inst_flags = 0; // THUMB etc
    if(dis_Disassemble(dis_arm, inst, sizeof(inst), 0x1000, inst_flags, DIS_OPTIMIZE_FULL, outbuffer, DIS_BUFFER_SIZE) != DIS_OK)
        printf("Warning: access out of bounds during disassembly\n");
    else
        print_dis_result(dis_arm, outbuffer);

    Disassembler *dis_x86 = dis_Create(DIS_TGT_X86_64, NULL);

    printf("* X86\n");
    // Now let's disassemble an instruction!
    // 48 81 eb 28 ee 67 00    sub    $0x67ee28,%rbx
    unsigned char inst2[] = {0x48, 0x81, 0xeb, 0x28, 0xee, 0x67, 0x00};
    //unsigned char inst[] = {0x73, 0x24};
    //
    uint64_t inst_flags2 = (DIS_INST_X86_CS64_MASK | DIS_INST_X86_LMA_MASK);
    if(dis_Disassemble(dis_x86, inst2, sizeof(inst2), 0x1000, inst_flags2, DIS_OPTIMIZE_FULL, outbuffer, DIS_BUFFER_SIZE) != DIS_OK)
        printf("Warning: access out of bounds during disassembly\n");
    else
        print_dis_result(dis_x86, outbuffer);

    Disassembler *dis_mips = dis_Create(DIS_TGT_MIPS_32, NULL);

    printf("* MIPS\n");
    // Now let's disassemble an instruction!
    // 48 81 eb 28 ee 67 00    sub    $0x67ee28,%rbx
    unsigned char inst3[] = {0x48, 0x81, 0xeb, 0x28, 0xee, 0x67, 0x00};
    //unsigned char inst[] = {0x73, 0x24};
    //
    uint64_t inst_flags3 = 0;
    if(dis_Disassemble(dis_mips, inst3, sizeof(inst3), 0x1000, inst_flags3, DIS_OPTIMIZE_FULL, outbuffer, DIS_BUFFER_SIZE) != DIS_OK)
        printf("Warning: access out of bounds during disassembly\n");
    else
        print_dis_result(dis_mips, outbuffer);

    /*dis_Dump(dis_arm);
    dis_Dump(dis_x86);
    dis_Dump(dis_mips);*/
    printf("* Info about arm\n");
    print_info(dis_arm);
    printf("\n");
    printf("* Info about x86\n");
    print_info(dis_x86);
    printf("\n");
    printf("* Info about mips\n");
    print_info(dis_mips);
    printf("\n");
}
