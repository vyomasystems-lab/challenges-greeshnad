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
    i=0
    # input transaction
    mav_putvalue_src1 = 0xffffffff
    mav_putvalue_src2 = 0xffffffff
    mav_putvalue_src3 = 0x0
    
    # mav_putvalue_instr = 0x101010B3
    # mav_putvalue_instr = 0x201010B3
    # mav_putvalue_instr = 537923635
    
    
    # expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)

    errors=[]
    # driving the input transaction
    dut.mav_putvalue_src1.value = mav_putvalue_src1
    dut.mav_putvalue_src2.value = mav_putvalue_src2
    dut.mav_putvalue_src3.value = mav_putvalue_src3
    dut.EN_mav_putvalue.value = 1
    opcode_array=[0x00000033,0x00000013]

    for opcode_1 in opcode_array:
        instruction=opcode_1
        for func3_1 in range(0,8):
            instruction1=(opcode_1>>12)| func3_1
            # print("func3_loop",instruction1)
            instruction=(instruction1<<12)|opcode_1
            # print(instruction)
            for imm in range(0,32):
                instruction1=(instruction>>20)| imm
                instruction2=(instruction1<<20)| instruction
                for func7_1 in range(0,128):
                    instruction3=(instruction2>>25)| func7_1
                    # print("func7_loop",instruction1)
                    instruction_final=instruction3<<25|instruction2
                    # print("Inside loop",type(instruction_final))
                    # instruction_hex=hex(instruction_final)
                    # print("is it printing",hex(instruction_final))
                    
                    
                    expected_mav_putvalue1 = bitmanip(instruction_final, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)
                    # print("Inside loop model value",expected_mav_putvalue1)
                    if expected_mav_putvalue1=='INVALID':
                        
                        # i=i+1
                        # print("i value",i)
                        continue 
                    # if(func3_1==7 and func7_1==127):
                    #         break
                    dut.mav_putvalue_instr.value = instruction_final
                    
                    # print(instruction_hex)
                    # await Timer(2,"ns")
                    yield Timer(1)
                    # i=i+1
                    # print(i)
                    # print(instruction_hex) 
                    dut_output1 = dut.mav_putvalue.value
                    # print("Buggy",dut_output1)
                    # cocotb.log.info(f'DUT OUTPUT={hex(dut_output1)}')
                    # cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue1)}')

                    # comparison
                    error_message = f'Value mismatch DUT = {hex(dut_output1)} does not match MODEL = {hex(expected_mav_putvalue1)} at opcode={hex(instruction_final)}'
                    try:
                        assert dut_output1 == expected_mav_putvalue1, error_message
                    except AssertionError as e:
                        i=i+1
                        errors.append(hex(instruction_final))
                        # cocotb.log.info(f'Value mismatch DUT = {hex(dut_output1)} does not match MODEL = {hex(expected_mav_putvalue1)} at opcode={hex(instruction_final)}')

    # dut.mav_putvalue_instr.value = mav_putvalue_instr
    # yield Timer(1) 

    # # obtaining the output
    # dut_output = dut.mav_putvalue.value
    # # valid_bit= dut.RDY_mav_putvalue.value
    # # print("Valid bit:",valid_bit)

    # cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
    # cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
    print('i value',i)
    # print(errors)
    errors_int = [int(numeric_string,16) for numeric_string in errors]
    for instruc in errors_int:
        expected_mav_putvalue1 = bitmanip(instruc, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)
        
        dut.mav_putvalue_instr.value = instruc
        yield Timer(1)

        dut_output1 = dut.mav_putvalue.value
        

        # comparison
        error_message = f'Value mismatch DUT = {hex(dut_output1)} does not match MODEL = {hex(expected_mav_putvalue1)} at opcode={hex(instruc)}'
        try:
            assert dut_output1 == expected_mav_putvalue1, error_message
        except AssertionError as e:
            # i=i+1
            # errors.append(hex(instruction_final))
            cocotb.log.info(f'Value mismatch DUT = {hex(dut_output1)} does not match MODEL = {hex(expected_mav_putvalue1)} at opcode={hex(instruc)}')
  
