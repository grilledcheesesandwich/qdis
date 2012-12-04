#include <stdarg.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <inttypes.h>

#include "cpu.h"

int main()
{
    /* hold a pointer to the function to make sure it is generated */
    void *x = (void*)&cpu_get_tb_cpu_state;
    void *y = (void*)&cpu_pc_from_tb;
    printf("%s %s\n", x, y);
    return 0;
}

