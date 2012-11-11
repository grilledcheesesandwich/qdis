#ifndef H_QEMU_HOOKS
#define H_QEMU_HOOKS

void disassembly_set_window(void *memory, uint64_t offset, size_t size);
bool disassembly_get_error();

#endif
