#!/usr/bin/python
'''
Explore an executable naively, ie without doing any symbolic evaluation
or jump table interpolation. Just follow jumps and calls from a provided
entry point, and keep track of what was visited.
'''
from __future__ import print_function, unicode_literals, division, absolute_import
import functools # for partial
import argparse
import mmap
from binascii import b2a_hex
import qdis
from qdis.format import format_inst

UNDEFINED = None
TRACE_INSTRUCTION = 'inst'

# Show stores to globals
trace_global_stores = False#True
# Show stores to temps and locals
trace_temp_stores = False#True
# Show all microcode for disassembled instructions
trace_microcode = False#True
# Show warnings (non-implemented microcode instructions etc)
show_warnings = False
# Show debug information after processing instruction
show_debug = False

class SavedState(object):
    '''
    Saved state object for evaluator.
    '''
    def __init__(self, globals_, temps_, jump_iflag):
        self.globals = globals_[:]
        self.temps = temps_[:]
        self.jump_iflag = jump_iflag

# XXX move this inside qdis some way
#     need platform-independent way to compute instruction flag and pc changes from env change instructions
ENV_ARM_THUMB_FLAG = 0xd0

class NaiveEval(object):
    '''
    Naive evaluator, to determine what PCs to search next from an instruction.
    Only understands implicit moves and moves between registers right now.
    '''
    def __init__(self, d):
        # Create list of handler bound methods for opcodes
        self.handlers = []
        for opcode in xrange(d.lookup_value(qdis.INFO_NUM_OPS, 0)):
            op_str = d.lookup_name(qdis.INFO_OP, opcode)
            if op_str is not None:
                handler = getattr(self, 'eval_'+op_str, None)
                if handler is None:
                    # print("Warning: unhandled instruction " + op_str)
                    handler = functools.partial(self._unhandled, op_str)
                self.handlers.append(handler)
        num_globals = d.lookup_value(qdis.INFO_NUM_GLOBALS, 0)

        self.globals = [UNDEFINED] * num_globals 
        self.global_by_id = [None] * num_globals
        self.global_by_name = {}
        for globid in xrange(num_globals):
            name = d.lookup_name(qdis.INFO_GLOBAL, globid)
            self.global_by_id[globid] = name 
            self.global_by_name[name] = globid

        self.warning_func = lambda val: None
        self.trace_func = lambda key,value: None # dummy
        self.env_id = self.global_by_name['env']
        # globals
        self.pc_id = d.lookup_value(qdis.INFO_PC_GLOBAL, 0)
        assert(self.pc_id != qdis.INVALID)

    def start_block(self, block, pc, iflag):
        # All globals and locals are undefined at the start of every block
        self.globals[:] = [UNDEFINED] * len(self.globals)
        self.temps = [UNDEFINED]*len(block.syms)

        self.ops = block.ops
        self.labels = block.labels
        self.globals[self.pc_id] = pc
        self.worklist = []
        self.pcs_out = set()
        self.ptr = 0
        self.jump_iflag = iflag # if instruction flags not changed, leave them as now
        while self.ptr is not None:
            i = self.ops[self.ptr]
            if trace_microcode:
                self.trace_func(TRACE_INSTRUCTION, i)
            self.eval_inst(i)

        return (self.pcs_out)
    
    # Save/store state, for forked paths
    def clone_state(self):
        return SavedState(self.globals, self.temps, self.jump_iflag)
    def apply_saved_state(self, state):
        self.globals = state.globals
        self.temps = state.temps
        self.jump_iflag = state.jump_iflag

    def eval_inst(self, inst):
        '''Symbolically evaluate an instruction'''
        self.handlers[inst.opcode](inst)
    def _unhandled(self, op, inst):
        '''Called when an instruction is unhandled'''
        self.warning_func('unhandled %s (%i)' % (op,inst.opcode))
        # set all output arguments to UNDEFINED
        for arg in inst.args:
            if arg.flags & qdis.ARG_OUTPUT:
                self.store(arg, UNDEFINED)
            elif arg.flags & qdis.ARG_INPUT:
                self.load(arg) # dummy load
        self.ptr += 1
    def store(self, dest, expr):
        '''
        Store symbolic value into global or temporary.
        '''
        if dest.flags & qdis.ARG_GLOBAL:
            if trace_global_stores:
                self.trace_func(self.global_by_id[dest.value], expr)
            self.globals[dest.value] = expr
        elif dest.flags & qdis.ARG_TEMP:
            if trace_temp_stores:
                self.trace_func('tmp%i' % dest.value, expr)
            self.temps[dest.value] = expr
        else:
            raise AssertionError('Invalid argument')
    def load(self, dest):
        '''
        Load symbolic value from global or temp.
        '''
        if dest.flags & qdis.ARG_GLOBAL:
            return self.globals[dest.value]
        elif dest.flags & qdis.ARG_TEMP:
            return self.temps[dest.value]
        else:
            raise AssertionError('Invalid argument')

    def clear_temps(self):
        '''
        Clear temps between basic blocks
        '''
        # TODO
    
    #### Instructions ####
    def eval_discard(self, inst):
        '''discard dest'''
        self.store(inst.args[0], UNDEFINED)
        self.ptr += 1
    def eval_mov_i32(self, inst):
        '''mov_i32 dest,src'''
        self.store(inst.args[0], self.load(inst.args[1]))
        self.ptr += 1
    def eval_movi_i32(self, inst):
        '''movi_i32 dest,src'''
        self.store(inst.args[0], inst.args[1].value)
        self.ptr += 1

    def eval_brcond_i32(self, inst):
        '''brcond_i32 t0,t1,cond,label'''
        label = inst.args[3].value
        self.worklist.append((label, self.clone_state()))
        self.clear_temps()
        self.ptr += 1

    def eval_set_label(self, inst):
        '''set_label $label'''
        self.clear_temps()
        self.ptr += 1

    def eval_st_i32(self, inst):
        '''st_i32 t0,basereg,offset'''
        # Check for thumb flag
        if inst.args[1].value == self.env_id and inst.args[2].value == ENV_ARM_THUMB_FLAG:
            val = self.load(inst.args[0])
            if val is not UNDEFINED:
                self.jump_iflag = self.jump_iflag & (~qdis.INST_ARM_THUMB_MASK)
                self.jump_iflag |= val << qdis.INST_ARM_THUMB_SHIFT
            else:
                self.jump_iflag = None # ouch
        self.ptr += 1

    def eval_qemu_ld32(self, inst):
        self.ptr += 1

    def eval_goto_tb(self, inst):
        '''goto_tb''' # ignored
        self.ptr += 1
    def eval_exit_tb(self, inst):
        '''exit_tb t1''' # interpreted as 'br to end'
        self.clear_temps()
        # append current value of PC to possible outputs
        self.pcs_out.add((self.globals[self.pc_id], self.jump_iflag))
        if self.worklist:
            # Still another path to follow?
            (label, state) = self.worklist.pop()
            self.ptr = self.labels[label]
            self.apply_saved_state(state)
        else:
            self.ptr = None

