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
    
    ######### CTB : Modify th0x76127fe test to expose the bug #############
    i=0
    # input transaction
    mav_putvalue_src1 = 56
    mav_putvalue_src2 = 0x2341073
    mav_putvalue_src3 = 0xff62537
    
    errors=[]
    # driving the input transaction
    dut.mav_putvalue_src1.value = mav_putvalue_src1
    dut.mav_putvalue_src2.value = mav_putvalue_src2
    dut.mav_putvalue_src3.value = mav_putvalue_src3
    dut.EN_mav_putvalue.value = 1
    #these two values below cover lsb 7 bits opcode combination of all possible instructions in model.py file
    opcode_array=[0x00000033,0x00000013]

    for opcode_1 in opcode_array:
        instruction=opcode_1
        for func3_1 in range(0,8):
            instruction1=(opcode_1>>12)| func3_1
            instruction=(instruction1<<12)|opcode_1
            
            for imm in range(0,32):
                instruction1=(instruction>>20)| imm
                instruction2=(instruction1<<20)| instruction
                for func7_1 in range(0,128):
                    instruction3=(instruction2>>25)| func7_1
                    
                    instruction_final=instruction3<<25|instruction2
                    expected_mav_putvalue1 = bitmanip(instruction_final, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)
                    
                    if expected_mav_putvalue1=='INVALID':
                        continue  #if instruction doesnt exist in model.py continue to next iteration
                    
                    dut.mav_putvalue_instr.value = instruction_final
                    
                    yield Timer(1)
                     
                    dut_output1 = dut.mav_putvalue.value #dut output
            
                    # comparison
                    error_message = f'Value mismatch DUT = {hex(dut_output1)} does not match MODEL = {hex(expected_mav_putvalue1)} at instruction={hex(instruction_final)}'
                    try:
                        assert dut_output1 == expected_mav_putvalue1, error_message
                    except AssertionError:
                        i=i+1
                        errors.append(hex(instruction_final))#stores all exception errors i.e model value is not equal to DUT value
                       

    print('No of exception erros',i)
    # convert all errors into hex int value
    errors_int = [int(numeric_string,16) for numeric_string in errors]
    #run all the error instructions and check which operation it corresponds to
    for instruc in errors_int:
        expected_mav_putvalue1 = bitmanip(instruc, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)
        
        dut.mav_putvalue_instr.value = instruc
        yield Timer(1)

        dut_output1 = dut.mav_putvalue.value
        
        # comparison
        error_message = f'Value mismatch DUT = {hex(dut_output1)} does not match MODEL = {hex(expected_mav_putvalue1)} at opcode={hex(instruc)}'
        try:
            assert dut_output1 == expected_mav_putvalue1, error_message
        except AssertionError:
            # i=i+1
            # errors.append(hex(instruction_final))
            cocotb.log.info(f'Value mismatch DUT = {hex(dut_output1)} does not match MODEL = {hex(expected_mav_putvalue1)} at opcode={hex(instruc)}')
  
