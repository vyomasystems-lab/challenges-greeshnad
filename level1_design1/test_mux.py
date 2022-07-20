# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""
    
    # for i in range(0,31):
    #     inp[i]=random.randint(0, 3)

    input_0=3
    # input_0=2'b00

    dut.inp2.value=input_0
    selection=2
    dut.sel.value=selection
    await Timer(2, units='ns')
    dut._log.info(f'Mux_sel={selection} Test_input={input_0} Output_Mux={int(dut.out.value)}')
    assert dut.out.value == input_0, "Multiplexer test failed with: {select} = {output}".format(
            select=dut.sel.value,  output=dut.out.value)


    # cocotb.log.info('##### CTB: Develop your test here ########')
