QEMUROOT = ..

SOURCES = $(QEMUROOT)/cutils.c \
	  dispatch.c \
	  translate-test.c

BaseNameSources := $(sort $(basename $(SOURCES)))
ObjectsO  := $(BaseNameSources:%=%.o)

QEMUFLAGS=-I. -I$(QEMUROOT)  \
	-I$(QEMUROOT)/tcg -I$(QEMUROOT)/fpu -I$(QEMUROOT)/include -I$(QEMUROOT)/linux-user \
	-D__STDC_FORMAT_MACROS -D_GNU_SOURCE  -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE \
	-DTCG_PYTHON -DTARGET_X86_64\
	-Wredundant-decls -Wundef -Wendif-labels -Wwrite-strings -fno-strict-aliasing \
	-Wno-sign-compare -Wno-missing-field-initializers -fexceptions $(shell pkg-config --cflags glib-2.0)
QEMULDFLAGS = $(shell pkg-config --libs glib-2.0)

CC = gcc
CXXFLAGS += $(QEMUFLAGS)
CFLAGS += $(QEMUFLAGS) -Wall -Wextra -Wformat -Wformat-security -g -O
LDFLAGS += $(QEMULDFLAGS) -g -O
MODULES = arm-module.o x86_32-module.o x86_64-module.o mips_32-module.o

all: translate-test

clean:
	rm -f $(ObjectsO)

translate-test: $(ObjectsO) $(MODULES)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)
