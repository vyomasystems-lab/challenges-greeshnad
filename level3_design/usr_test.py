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
    

    clock1 = Clock(dut.clock, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock1.start())        # Start the clock

    # dut.clock.value =0 
    dut.MODE.value = 0
    dut.DATAIN.value = 1
    dut.reset.value = 1; 
    await RisingEdge(dut.clock)

    dut.reset.value = 0; 
    await RisingEdge(dut.clock)

    dut_output1=dut.DATAOUT.value
    print("Output is",dut_output1)
    error_message=f'Failing test'
    assert dut_output1 == 1, error_message