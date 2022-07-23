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
async def test_seq_bug1(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)
    dut._log.info('current_state_before_rst=%s',dut.current_state.value)  
    dut.reset.value = 0
    await FallingEdge(dut.clk)
    dut._log.info('current_state_after_rst=%s',dut.current_state.value)

    #test_vector
    await Timer(10, units='us')
    dut.inp_bit.value=1
    dut._log.info('current_state_bit1=%s',dut.current_state.value)


    await Timer(10, units='us')
    dut.inp_bit.value=0
    dut._log.info('current_state_bit1=%s',dut.current_state.value)
    
    await Timer(10, units='us')
    dut.inp_bit.value=1
    dut._log.info('current_state_bit1=%s',dut.current_state.value)

    await Timer(10, units='us')
    dut.inp_bit.value=0
    dut._log.info('current_state_bit1=%s',dut.current_state.value)

    await Timer(10, units='us')
    dut.inp_bit.value=1
    dut._log.info('current_state_bit1=%s',dut.current_state.value)

    await Timer(10, units='us')
    dut.inp_bit.value=1
    dut._log.info('current_state_bit1=%s',dut.current_state.value)



    await Timer(10, units='us')
    dut._log.info('current_state_bit1=%s',dut.current_state.value)
    assert dut.seq_seen.value == 1, "Sequence_detector failed with sequence 101011")
    
