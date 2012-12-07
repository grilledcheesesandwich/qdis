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
from qdis.concrete_eval import ConcreteEval # used by NewPCIflagsExtractor

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

class CPUState(object):
    '''
    Saved state object for evaluator.
    '''
    def __init__(self):
        self.globals = []
        self.temps = []
        self.env = {}

    def clone(self):
        rv = CPUState()
        rv.globals = self.globals[:]
        rv.temps = self.temps[:]
        rv.env = self.env.copy()
        return rv

class PCIflagsExtractor(object):
    '''
    Manage VM state that influences instruction decoding.
    This class has two uses
    1) Inject the current pc and iflags into the virtual machine state
    2) Take the current state of the virtual machine and compute new pc and iflags
    for continuation of execution.
    '''
    def __init__(self, qd):
        # concrete interpreter used to extract new pc and iflags from CPUState
        self.interp = ConcreteEval(qd)
        self.helper_get_tb_cpu_state = qd.get_helper(qdis.HELPER_GET_TB_CPU_STATE)
        self.helper_get_cpu_state_tb = qd.get_helper(qdis.HELPER_GET_CPU_STATE_TB)
    
    def inject(self, state, pc, pc_base, flags):
        # Transfer globals and env
        self.interp.reset_state() 
        rv = self.interp.start_block(self.helper_get_cpu_state_tb, 
                args=[pc, pc_base, flags])
        
        state.globals = self.interp.state.globals
        state.env = self.interp.state.env

    def extract(self, state):
        # Transfer globals and env
        self.interp.state.globals = state.globals
        self.interp.state.env = state.env
        
        rv = self.interp.start_block(self.helper_get_tb_cpu_state)
        (pc,pc_base,flags) = (rv[0],rv[1],rv[2])
        return (pc,pc_base,flags) 
    
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
       
        self.state = CPUState()
        self.state.globals = [UNDEFINED] * num_globals 
        self.global_by_id = [None] * num_globals
        self.global_by_name = {}
        for globid in xrange(num_globals):
            name = d.lookup_name(qdis.INFO_GLOBAL, globid)
            self.global_by_id[globid] = name 
            self.global_by_name[name] = globid

        self.warning_func = lambda val: None
        self.trace_func = lambda key,value: None # dummy
        self.env_id = self.global_by_name['env']

        self.pc_extractor = PCIflagsExtractor(d)
        # globals
        self.pc_id = d.lookup_value(qdis.INFO_PC_GLOBAL, 0)
        assert(self.pc_id != qdis.INVALID)

    def start_block(self, block, pc, iflag):
        # All globals and locals are undefined at the start of every block
        self.state.globals[:] = [UNDEFINED] * len(self.state.globals)
        self.state.temps = [UNDEFINED]*len(block.syms)
        self.state.env = {}
        self.pc_extractor.inject(self.state, pc, 0, iflag)

        self.ops = block.ops
        self.labels = block.labels
        self.state.globals[self.pc_id] = pc
        self.worklist = []
        self.pcs_out = set()
        self.ptr = 0
        while self.ptr is not None:
            i = self.ops[self.ptr]
            if trace_microcode:
                self.trace_func(TRACE_INSTRUCTION, i)
            self.eval_inst(i)

        return (self.pcs_out)
    
    # Save/store state, for forked paths
    def clone_state(self):
        return self.state.clone()
    def apply_saved_state(self, state):
        self.state = state

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
            self.state.globals[dest.value] = expr
        elif dest.flags & qdis.ARG_TEMP:
            if trace_temp_stores:
                self.trace_func('tmp%i' % dest.value, expr)
            self.state.temps[dest.value] = expr
        else:
            raise AssertionError('Invalid argument')
    def load(self, dest):
        '''
        Load symbolic value from global or temp.
        '''
        if dest.flags & qdis.ARG_GLOBAL:
            return self.state.globals[dest.value]
        elif dest.flags & qdis.ARG_TEMP:
            return self.state.temps[dest.value]
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
        expr = self.load(inst.args[0])
        self.state.env[inst.args[2].value] = expr
        if trace_global_stores:
            self.trace_func('[env+0x%x]' % inst.args[2].value, expr)
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
        (newpc, _, newflags) = self.pc_extractor.extract(self.state)
        self.pcs_out.add((newpc, newflags))

        if self.worklist:
            # Still another path to follow?
            (label, state) = self.worklist.pop()
            self.ptr = self.labels[label]
            self.apply_saved_state(state)
        else:
            self.ptr = None

