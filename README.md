The qdis library
==================

Introduction
----------------

The qdis library offers a generic interface for disassembling binary program code to IR.

It is built upon the well-known emulator `qemu`, originally written by Fabrice Bellard.

Rationale
-----------

Disassembling to a generic IR facilitates automatic analysis of cross-platform code. 

This makes it possible to write tools that do, for example, abstract or symbolic execution once and apply 
it to programs of every architecture.

Supported architectures
------------------------

Fully supported
- ARM
- i386 / x86_64

Partially supported
- mips (32 and 64)
- ppc (32 and 64)
- alpha
- m68k
- sparc (32 and 64)

With a little extra work, the following architectures could also be supported, as
qemu has translators for them:

- cris
- lm32
- microblaze
- openrisc
- s390x
- sh4
- unicore
- xtensa

Building
==========

    cd qdis
    python gen_modules.py (optional, only needed when modified)
    bash gen_python_binding.sh (optional, only needed when qdis.h modified)
    make

Intermediate Representation (IR)
=================================

The intermediate representation is based on TCG (Tiny Code Generator).
This offers a commonality between the various instruction sets, a general microcode.
All internal effects of instructions, such as updating of flags is made explicit.

Refer for opcodes to README.tcg

Why not LLVM?
--------------
A well-known IR for compilation is LLVM (ref), as used by the C compiler Clang. Many tools exist to process
and process LLVM code, and it would be great to make use of these.

However, although the instruction set is similar [1] to that of TCG and thus basic translation is straightforward, 
LLVM IR sits at a significantly higher level than that of CPU instructions. To enable optimization, the LLVM IR
reasons in term of basic types, functions, parameters, memory allocation/deallocation. Much of this information
is lost while compiling to CPU code, and would have to be reconstructed to form correct and complete LLVM code from disassembly.

Converting to LLVM could thus be seen as a layer on top of a microcode IR such as produced by QDIS. The 
Revgen tool [2] in the S2E project [3] does exactly this (but only for X86). I borrowed some ideas from them such
as returning an instruction category from QEMU, but explicitly don't include the LLVM 
conversion in this base library as I want to keep the flexibility open for tools that build upon QDIS to 
use either naive or recognition of higher-level structures (For example: in the case of heavily obfuscated 
or hand-written assembly code, simple platform heuristics for recognizing functions would be useless).

There is also libcpu [3] which aims to be a generic CPU emulation library, using LLVM as backend. It shares
some of the goals with QDIS and implements many of the instruction set architectures also present in 
QEMU, but some of them are quite incomplete (ARM, for example).  I chose to use QEMU as base as it as an active 
emulator project has seen a lot of real-life code.

[1] http://llvm.org/docs/LangRef.html
[2] http://infoscience.epfl.ch/record/166081/files/revgen.pdf
[3] http://dslab.epfl.ch/proj/s2e
[4] http://www.libcpu.org/wiki/Main_Page

Architecture of qdis
======================
The design `qemu` is aimed at raw speed. This means that some tradeoffs have been made.
One of these is that much of the code is specialized according to both the host and client CPU. This effectively prevents
the code from being build for multiple clients at once, in one executable.

Aside: `qemu` internally uses the word 'target' in a two conflicting ways: in some parts of the code (tcg) it is 
used to describe the backend (ie, target for code generation, the host), in other parts it is used to 
describe the frontend (ie, the emulated guest CPU). `qdis` API uses the word target for the frontend only.

By using a special build process with symbol renaming and scope changing, `qdis` produces a module for every target
instruction set. These modules are linked together to form the library. In this way, a single API can be offered
to convert many instruction sets, in principle all of those supported by qemu (though not all are implemented yet,
see later on), to IR.

I have chosen to use a custom build process instead of rewriting parts of QEMU because I do not want to diverge
too much, as to make it easier to merge in changes and improvements from QEMU which is a very actively maintained project.

Helpers
--------------
For complex instructions qemu emits calls to helper functions.
These complicate the interpretation process as they are target-dependent, unlike the TCG opcodes.
(ie ARM has XXX i386 has `cc_compute_c` to compute condition flags)
In a future version, it would be useful if qdis provides abstract version of the helper functions in 
(for example, in LLVM or TCG IR format)
so that these can be included in analysis without building special cases.

Build internals
----------------
`gen_modules.py` generates `Makefile.modules` and `dispatch_create.h`.
The generated makefile is included in the main makefile and contains build instructions to build the 
modules from a precious mingling of qemu source code and qdis code.
The dispatch header file calls the entry point of the module based on one of the `QDIS_TGT_*` constants.

Python binding
----------------
The Python binding uses ctypes and is generated using ctypesgen [1] so it is a direct
mapping of the C API. Use the script `gen_python_binding.sh` to 
re-generate the Python binding when `qdis.h` was modified. The rationale for using ctypes (apart from not having
to bother with the fun process of writing a Python API binding) is that it works as-is with the PyPy Python JIT.

[1] http://code.google.com/p/ctypesgen/

Data structures / API
======================

Instruction flags
------------------
Selecting the instruction set is not enough to completely determine instruction decoding.

Sometimes the interpretation of instructions depends on certain state of the CPU. This is mainly the case when the
CPU supports multiple instruction sets, for example ARM processors support the 32-bit ARM instruction set as well as the 16-bit
Thumb instruction set and can switch between them at any time. AMD64 processors can switch between 16-bit, 32-bit and
64-bit mode, which affects the size and number of registers.

For this reason QDIS accepts instruction flags for each decoded instructions. These instruction flags provide additional
information on how to decode the instruction.

As instructions influence the CPU state, and this CPU state can in turn change the instruction interpretation (for example,
the ARM BLX instruction). To capture this, QDIS provides a special helper function that takes the current CPU
state and returns the new Program Counter and instruction flags, and a symmetric function that takes a
Program Counter and instruction flags and puts these into the CPU state.

