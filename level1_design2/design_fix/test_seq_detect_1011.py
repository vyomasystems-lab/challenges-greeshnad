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
    dut._log.info('current_state_with_rst_asserted=%s',dut.current_state.value) 

    await Timer(10, units='ns')
    dut.inp_bit.value=1
    dut._log.info('current_state_bit1=%s',dut.current_state.value)


    await Timer(10, units='ns')
    dut.inp_bit.value=0
    dut._log.info('current_state=%s',dut.current_state.value)
    
    await Timer(10, units='ns')
    dut.inp_bit.value=1
    dut._log.info('current_state=%s',dut.current_state.value)

    await Timer(10, units='ns')
    dut.inp_bit.value=0
    dut._log.info('current_state=%s',dut.current_state.value)
    # assert dut.seq_seen.value == 1, "Sequence_detector failed with sequence 101011"

    dut.reset.value = 0
    await FallingEdge(dut.clk)
    dut._log.info('current_state_rst_deasserted=%s',dut.current_state.value)

    #test_vector
    input_array=[1,0,1,1,1,0,1,1]
    le=len(input_array)
    i=0
    await Timer(10, units='us')
    for inp in input_array:
        
        dut.inp_bit.value=inp
        dut._log.info('current_state=%sh',dut.current_state.value)
        await Timer(11, units='us')
        dut._log.info('final_status=%s',dut.current_state.value)
        i=i+1
        if(i==le):
            assert dut.seq_seen.value == 1, "Sequence_detector failed" 
        # try:
        #     assert dut.seq_seen.value == 1, "Sequence_detector failed"
        # except AssertionError as e:


    # await Timer(10, units='us')
    # dut.inp_bit.value=0
    # dut._log.info('current_state=%s',dut.current_state.value)
    
    # await Timer(10, units='us')
    # dut.inp_bit.value=1
    # dut._log.info('current_state=%s',dut.current_state.value)

    # await Timer(10, units='us')
    # dut.inp_bit.value=1
    # dut._log.info('current_state=%s',dut.current_state.value)

    # await Timer(10, units='us')
    # dut.inp_bit.value=0
    # dut._log.info('current_state=%s',dut.current_state.value)

    # await Timer(10, units='us')
    # dut.inp_bit.value=1
    # dut._log.info('current_state=%s',dut.current_state.value)

    # await Timer(10, units='us')
    # dut.inp_bit.value=1
    # dut._log.info('current_state=%s',dut.current_state.value)

    # await Timer(10, units='us')
    # dut._log.info('final_status=%s',dut.current_state.value)
    # assert dut.seq_seen.value == 1, "Sequence_detector failed with sequence 1011011"
    
