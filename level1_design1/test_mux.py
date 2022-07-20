# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""
    for i in range(0,31):
        inp[i]=random.randint(0, 3)
    dut.inp0.value=inp[0]
    selection=0
    dut.sel.value=selection
    await Timer(2, units='ns')

    assert dut.out.value == inp[selection], "Randomised test failed with: {A} + {B} = {SUM}".format(
            A=dut.a.value, B=dut.b.value, SUM=dut.sum.value)


    cocotb.log.info('##### CTB: Develop your test here ########')
