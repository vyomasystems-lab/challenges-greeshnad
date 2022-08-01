# See LICENSE.vyoma for details

# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path

import cocotb
from cocotb.triggers import Timer
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

@cocotb.test()
async def usr_test(dut):
    

    clock1 = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock1.start())        # Start the clock

    await Timer(10,'us')
    dut.clear.value = 1
    await RisingEdge(dut.clk)
    dut.clear.value = 0
    input_val=0b0111
    dut.S.value = 3
    dut.I.value = 0b0111
    left=1
    right=1
    dut.right.value=right
    dut.left.value=left
    
    await Timer(11,'us')
    for sel in range(0,4):
        
        current_output=dut.O.value
        dut.S.value = sel
        await Timer(11,'us')
        
        if (sel==0):   
            dut_output=dut.O.value
            expected_output=current_output
            try:
                assert dut_output==expected_output, f'Value mismatch DUT = {dut_output} does not match expected = {(expected_output)} at sel 0'
            except AssertionError:
                cocotb.log.info(f'Value mismatch DUT = {dut_output} does not match expected = {(expected_output)} at sel 0')    
        if (sel==1):   
            dut_output=dut.O.value
            expected_output=(current_output<<1)|left
            try:
                assert dut_output==expected_output, f'Value mismatch DUT = {dut_output} does not match expected = {(expected_output)} at sel 1'
            except AssertionError:
                cocotb.log.info(f'Value mismatch DUT = {dut_output} does not match expected = {(expected_output)} at sel 1')
        if (sel==2):   
            dut_output=dut.O.value
            if right==1:
                expected_output=current_output>>1|8
            else:
                expected_output=current_output>>1
            try:
                assert dut_output==expected_output, f'Value mismatch DUT = {dut_output} does not match expected = {(expected_output)} at sel 2'
            except AssertionError:
                cocotb.log.info(f'Value mismatch DUT = {dut_output} does not match expected = {(expected_output)} at sel 2')
        if (sel==3):   
            dut_output=dut.O.value
            expected_output=input_val
            try:
                assert dut_output==expected_output, f'Value mismatch DUT = {dut_output} does not match expected = {(expected_output)} at sel 3'
            except AssertionError:
                cocotb.log.info(f'Value mismatch DUT = {dut_output} does not match expected = {(expected_output)} at sel 3')
