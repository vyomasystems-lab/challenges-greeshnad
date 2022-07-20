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

    dut.inp12.value=input_0
    selection=12
    dut.sel.value=selection
    await Timer(2, units='ns')
    dut._log.info(f'sel={selection} model={input_0} DUT={int(dut.out.value)}')
    assert dut.out.value == input_0, "Randomised test failed with: {A} = {SUM}".format(
            A=dut.sel.value,  SUM=dut.out.value)


    # cocotb.log.info('##### CTB: Develop your test here ########')
