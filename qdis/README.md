qdis
======

Universal instruction decoding library based on `qemu`.

Building the library
---------------------

Building:

    $ make

This creates a libqdis.so.
    
To edit which modules are generated, modify `gen_modules.py` then run:

    $ python gen_modules.py  (optional)

To re-generate the Python binding (optional, needs ctypesgen):

    $ bash gen_python_binding.sh

What information is returned
=============================
Microcode

Instruction type (only for i386/amd64/arm for now)

CALL/RET/JMP/DEFAULT, information that cannot be (trivially) derived from the returned microcode.
- `DEFAULT` means that execution will continue normally with the next instruction.


Credits
=============================
- `SET_TB_TYPE` borrowed from S2E.  http://dslab.epfl.ch/proj/s2e

