#include "qdis.h"
#include <stdio.h>

void print_info(QDisassembler *dis)
{
    size_t pc_idx = qdis_LookupValue(dis, QDIS_INFO_PC_OFFSET, 0);
    size_t sp_idx = qdis_LookupValue(dis, QDIS_INFO_SP_OFFSET, 0);
    size_t num_helpers = qdis_LookupValue(dis, QDIS_INFO_NUM_HELPERS, 0);
    size_t num_globals = qdis_LookupValue(dis, QDIS_INFO_NUM_GLOBALS, 0);
    size_t num_ops = qdis_LookupValue(dis, QDIS_INFO_NUM_OPS, 0);
    size_t i = 0;
    printf("State size: 0x%x\n", (int)qdis_LookupValue(dis, QDIS_INFO_STATE_SIZE, 0));
    printf("PC register: 0x%x\n", (int)pc_idx);
    printf("SP register: 0x%x\n", (int)sp_idx);
    /*
    printf("Ops:\n");
    for(i=0; i<num_ops; ++i)
    {
        printf("  %i %s\n", i, qdis_LookupName(dis, QDIS_INFO_OP, i));
    }
    */
    printf("Helpers:\n");
    for(i=0; i<num_helpers; ++i)
    {
        printf("  %i %s\n", i, qdis_LookupName(dis, QDIS_INFO_HELPER, i));
    }
    printf("Globals:\n");
    for(i=0; i<num_globals; ++i)
    {
        printf("  %i %s (0x%x:%i)\n", i, qdis_LookupName(dis, QDIS_INFO_GLOBAL, i),
                (int)qdis_LookupValue(dis, QDIS_INFO_GLOBAL_OFFSET, i),
                (int)qdis_LookupValue(dis, QDIS_INFO_GLOBAL_SIZE, i));
    }
}

void print_dis_result(QDisassembler *dis, QDisResult *rv)
{
    int i = 0, j = 0, arg = 0;
    printf("Result: %p\n", rv);
    printf("Text: %s\n", rv->inst_text);
    printf("Instruction length: %i\n", (int)rv->inst_size);
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
                qdis_LookupName(dis, QDIS_INFO_OP, rv->ops[i].opcode));
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
    QDisassembler *dis_arm = qdis_Create(QDIS_TGT_ARM, NULL);
    void *outbuffer = malloc(QDIS_BUFFER_SIZE);

    printf("* ARM\n");
    // Now let's disassemble an instruction!
    //unsigned char inst[] = {0x10,0x40,0x2d,0xe9}; // Push {r4,lr}
    //unsigned char inst[] = {0x0a,0x00,0x00,0x0a}; // Push {r4,lr}
    unsigned char inst[] = {0x02, 0x0a, 0x21, 0xf4}; // Push {r4,lr}
    //
    uint64_t inst_flags = 0; // THUMB etc
    if(qdis_Disassemble(dis_arm, inst, sizeof(inst), 0x1000, inst_flags, QDIS_OPTIMIZE_FULL, outbuffer, QDIS_BUFFER_SIZE) != QDIS_OK)
        printf("Warning: access out of bounds during disassembly\n");
    else
        print_dis_result(dis_arm, outbuffer);

    QDisassembler *dis_x86 = qdis_Create(QDIS_TGT_X86_64, NULL);

    printf("* X86\n");
    // Now let's disassemble an instruction!
    // 48 81 eb 28 ee 67 00    sub    $0x67ee28,%rbx
    unsigned char inst2[] = {0x48, 0x81, 0xeb, 0x28, 0xee, 0x67, 0x00};
    //unsigned char inst[] = {0x73, 0x24};
    //
    uint64_t inst_flags2 = (QDIS_INST_X86_CS64_MASK | QDIS_INST_X86_LMA_MASK);
    if(qdis_Disassemble(dis_x86, inst2, sizeof(inst2), 0x1000, inst_flags2, QDIS_OPTIMIZE_FULL, outbuffer, QDIS_BUFFER_SIZE) != QDIS_OK)
        printf("Warning: access out of bounds during disassembly\n");
    else
        print_dis_result(dis_x86, outbuffer);

    QDisassembler *dis_mips = qdis_Create(QDIS_TGT_MIPS, NULL);

    printf("* MIPS\n");
    // Now let's disassemble an instruction!
    // 48 81 eb 28 ee 67 00    sub    $0x67ee28,%rbx
    unsigned char inst3[] = {0x48, 0x81, 0xeb, 0x28, 0xee, 0x67, 0x00};
    //unsigned char inst[] = {0x73, 0x24};
    //
    uint64_t inst_flags3 = 0;
    if(qdis_Disassemble(dis_mips, inst3, sizeof(inst3), 0x1000, inst_flags3, QDIS_OPTIMIZE_FULL, outbuffer, QDIS_BUFFER_SIZE) != QDIS_OK)
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
