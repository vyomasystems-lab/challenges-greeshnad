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
    dut.clear.value = 0
    dut.S.value = 3
    dut.I.value = 3
    
    await Timer(11,'us')
    print("Output is",dut.O.value)

    
    dut.S.value = 4
    await Timer(11,'us')
    print("Output1 is",dut.O.value)


    dut.S.value = 2
    await Timer(11,'us')

    dut_output1=dut.O.value
    print("Output_final is",dut.O.value)
    error_message=f'Failing test'
    assert dut_output1 == 6, error_message