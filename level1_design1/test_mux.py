# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""

    input_0=3
    dut.inp10.value=input_0
    selection=10
    dut.sel.value=selection
    await Timer(2, units='ns')
    dut._log.info(f'Mux_sel={selection} Test_input={input_0} Output_Mux={int(dut.out.value)}')
    assert dut.out.value == (input_0), "Multiplexer test failed with: {select} = {output}".format(
            select=dut.sel.value,  output=dut.out.value)
    

    input_1=2
    dut.inp12.value=input_1
    selection=12
    dut.sel.value=selection
    await Timer(2, units='ns')
    dut._log.info(f'Mux_sel={selection} Test_input={input_1} Output_Mux={int(dut.out.value)}')
    assert dut.out.value == (input_1), "Multiplexer test failed with: {select} = {output}".format(
            select=dut.sel.value,  output=dut.out.value)
    
    
