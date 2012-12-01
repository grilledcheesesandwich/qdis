The qdis library
==================

Introduction
----------------

A sizable part of the human product of the last decades consists of software, most of it in binary form.

A growing jungle of legacy programs, retro games, closed-source driver blobs, computer viruses and exploits, 

And as software and hardware is finding its way into more areas of our lives, 
there are opaque closed-source binary blobs everywhere; as an example, the firmware of a pacemaker. 
Wouldn't you like to know what is happening inside? Or are you going by the vendor's word that everything is safe and sound?

Much information is lost in old documents of which we don't know how to interpret them.

Closed-source drivers have their problems as well, blocking interoparability, commonality in software and interfaces,
and forces the hardware to quick obsolence when the vendor decides to no longer support it. 

Is it possible to make any sense of this motley jumble of bits and bytes?

It would be nice to open all of this up to data mining, analysis, visualization and eventually understanding.

x... Restricted to programs and not other binary formats such as documents, some libraries already exist for that purpose
(hachoir, ...).

Rationale
-----------
There is just too much binary code to go for the naive approach of reading disassembly.
Although effective, it is very time consuming and thus inefficient.
Code is already interpreted by the CPU so a lot of the work traditionally done by a reverse engineer should be possible to automate
Or at least made easier.

Here the goal is not decompilation from a jumble of assembly code to a jumble of C-ish
code, but understanding and exploration, i.e. documenting the underlying hardware in case of a driver, 
finding out an obscure document format, or finding interesting pecularities in game code.

Also it should be possible to analyze a large amount of binaries and find common patterns, perform data mining.

For this reason I want to experiment with symbolic evaluation (ref), abstract evaluation (ref), partial dynamic evaluation (ref) etc.

Reuse
-------------
Over the years there has been shockingly little reuse, not only of code but also of ideas in software. 
Every generation of hardware, the fast pace in the sector gives the idea that every little thing has to be invented again.
Much of the history is simply lost. How can we ever advance if we don't learn from the mistakes in the past, and 
to make software engineering evolve to a stable discipline instead of franctic buzzword bingo?

Even though the problems back then are, mostly, the same ones as we're trying to solve now. Even with all the churn in
devices and software versions, and graphical shells, the big problems in computer science haven't changed.

Once in a while some old code turns up and solves an immediate problem that there is now (see for example `eqntott` and `espresso`,
http://code.google.com/p/eqntott/ for minimizing boolean expressions, still very relevant). That code was written in my birth year!

Software archeology
-----------------------

Software sports many levels of abstraction, the lowest one is the part that interfaces directly to the hardware, in the
middle is the overall architecture and design of the system (how everything fits together), and at the top is the API 
or user interface it exposes to the outside.

The first barrier to understanding binary code is the understanding of the opcodes of the processor.
Learning the ins and outs of a specific CPU is a large projects in itself. Many different CPUs have been introduced
over the years, and on those also many variations exist, new ones are designed every year.

To add to that, any specific knowledge has a short expiration date of usefulness. There is limited
utility to learn, for example, 68000 instruction set just to understand some old code for which
all documentation and source code were lost. 

For code generation, it is well-understood that a compiler is necessary to abstract away some of the underlying
details and make writing software manageable.

Many tools exist to disassemble programs, even to attempt to decompile them to their original form (or a C-ish 
dialect). Many of these are limited to one instruction set, mainly x86. Times are changing, and x86 is no longer
the only game in town (was it ever?). But extending tools that have been built specifically for one instruction
set to another is generally a lot of work, even though much of the underlying idea is the same: all processors
perform operations on registers, write and read from memory and I/O.

Intermediate Representation (IR)
---------------------------------
Find the commonality between the various instruction sets and write this into an IR.
Internal effects of instructions, such as updating of flags is made explicit.
Updating of flags and such is explicit.

TCG (Tiny Code Generator)
Refer to opcodes in README.tcg

Microcode.

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

Introducing qdis
=====================

Universal disassembler of code.
Not only to the vendor-supplied instruction strings
But to a general IR that can be processed computationally.

It is built upon the great emulator `qemu` originally written by Fabrice Bellard.

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

[make image]

I have chosen to use a custom build process instead of rewriting parts of QEMU because I do not want to diverge
too much, as to make it easier to merge in changes and improvements from QEMU which is a very actively maintained project.

Helpers
--------------
For complex instructions qemu emits calls to helper functions.
These complicate the interpretation process as they are target-dependent, unlike the TCG opcodes.
(ie ARM has XXX i386 has XXX)
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
The Python binding uses ctypes and is generated using ctypesgen [1]. Use the script `gen_python_binding.sh` to 
re-generate the Python binding when `qdis.h` was modified. The rationale for using ctypes (apart from not having
to bother with the fun process of writing a Python API binding) is that it works as-is with the PyPy Python JIT.

[1] http://code.google.com/p/ctypesgen/

Data structures / API
----------------------

