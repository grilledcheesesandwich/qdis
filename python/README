qdis
Instruction decoding library based on qemu
Python wrapper

Building:

$ python gen_modules.py  (optional)
$ make

Creates a libqdis.so

To re-generate the Python binding:

$ bash gen_python_binding.sh (optional, needs ctypesgen)

What information is returned
=============================
Microcode

Instruction type (only for i386/amd64/arm for now)

CALL/RET/JMP/DEFAULT, information that cannot be (trivially) derived from the returned microcode.
- `DEFAULT` means that execution will continue normally with the next instruction.


Credits
=============================
SET_TB_TYPE borrowed from S2E
http://dslab.epfl.ch/proj/s2e

