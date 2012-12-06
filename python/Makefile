QEMUROOT = ..

SOURCES_LIB = $(QEMUROOT)/cutils.c \
	  dispatch.c \
	  disas-util.c
SOURCES_TEST =  translate-test.c

OBJECTS_LIB_BASE := $(basename $(SOURCES_LIB))
OBJECTS_LIB  := $(OBJECTS_LIB_BASE:%=%.o)
OBJECTS_TEST_BASE := $(basename $(SOURCES_TEST))
OBJECTS_TEST := $(OBJECTS_TEST_BASE:%=%.o)

QEMUCFLAGS=-I. -I$(QEMUROOT)  \
	-I$(QEMUROOT)/tcg -I$(QEMUROOT)/fpu -I$(QEMUROOT)/include -I$(QEMUROOT)/linux-user \
	-D__STDC_FORMAT_MACROS -D_GNU_SOURCE  -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE \
	-DTCG_PYTHON \
	-Wredundant-decls -Wundef -Wendif-labels -Wwrite-strings -fno-strict-aliasing \
	-Wno-sign-compare -Wno-missing-field-initializers -fexceptions $(shell pkg-config --cflags glib-2.0)
QEMULDFLAGS = $(shell pkg-config --libs glib-2.0)

CC = gcc
OBJCOPY = objcopy
CXXFLAGS += $(QEMUCFLAGS)
CFLAGS += $(QEMUCFLAGS) -Wall -Wextra -Wformat -Wformat-security -g -O -fPIC
LDFLAGS += $(QEMULDFLAGS) -g -O
LDFLAGS_SHARED += $(LDFLAGS) -shared

all: translate-test libqdis.so

include Makefile.modules

clean:
	rm -f $(OBJECTS_LIB) $(OBJECTS_TEST) *.o

translate-test: $(OBJECTS_LIB) $(OBJECTS_TEST) $(MODULES)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

libqdis.so: $(OBJECTS_LIB) $(MODULES)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS_SHARED)

# Generate cpu_get_tb_cpu_state function and other helpers as LLVM bitcode (proof of concept)
# XXX ARM only, and the files used differ per architecture
CLANG=/opt/clang/bin/clang
LLVM_LINK=/opt/clang/bin/llvm-link

#include Makefile.helpers-i386
#include Makefile.helpers-arm

