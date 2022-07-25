# See LICENSE.iitm for details
# See LICENSE.vyoma for details

import random
import sys
import cocotb
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge
from cocotb.result import TestFailure
from cocotb.clock import Clock

from model_mkbitmanip import *

# Clock Generation
@cocotb.coroutine
def clock_gen(signal):
    while True:
        signal.value <= 0
        yield Timer(1) 
        signal.value <= 1
        yield Timer(1) 

# Sample Test
@cocotb.test()
def run_test(dut):

    # clock
    cocotb.fork(clock_gen(dut.CLK))

    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1

    ######### CTB : Modify the test to expose the bug #############
    # input transaction
    mav_putvalue_src1 = 0x5
    mav_putvalue_src2 = 0xffffffff
    mav_putvalue_src3 = 0x0
    # mav_putvalue_instr = 0x101010B3
    # mav_putvalue_instr = 0x201010B3
    mav_putvalue_instr = 51
    print("Outside loop",type(mav_putvalue_instr))
    # expected output from the model
    # expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)

    # driving the input transaction
    # mav_putvalue_instr[6:0] == 7'b0110011 
	# mav_putvalue_instr[6:0] == 7'b0010011
    dut.mav_putvalue_src1.value = mav_putvalue_src1
    dut.mav_putvalue_src2.value = mav_putvalue_src2
    dut.mav_putvalue_src3.value = mav_putvalue_src3
    dut.EN_mav_putvalue.value = 1
    opcode_array=[0x00000033]
    for opcode_1 in opcode_array:
        instruction=opcode_1
        for func3_1 in range(0,8):
            instruction1=(opcode_1>>16)| func3_1
            # print("func3_loop",instruction1)
            instruction=(instruction1<<16)|opcode_1
            # print(instruction)
            for func7_1 in range(0,128):
                instruction1=(instruction>>25)| func7_1
                # print("func7_loop",instruction1)
                instruction_final=instruction1<<25|instruction
                print("Inside loop",type(instruction_final))
                instruction_hex=hex(instruction_final)
                print(instruction_final)
                
                dut.mav_putvalue_instr.value = instruction_final
                expected_mav_putvalue = bitmanip(instruction_final, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)
                yield Timer(1) 
                dut_output = dut.mav_putvalue.value
                cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
                cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')

                # comparison
                error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)} at opcode={hex(instruction_final)}'
                assert dut_output == expected_mav_putvalue, error_message

    # dut.mav_putvalue_instr.value = mav_putvalue_instr
    yield Timer(1) 

    # obtaining the output
    dut_output = dut.mav_putvalue.value
    # valid_bit= dut.RDY_mav_putvalue.value
    # print("Valid bit:",valid_bit)

    cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
    cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
    
    # comparison
    error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
    assert dut_output == expected_mav_putvalue, error_message
