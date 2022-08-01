# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""
    for i in range(0,31):
        input_val=random.randint(1,3)
        selection=i
        dut.sel.value=i 
        dut.inp0.value=input_val
        dut.inp1.value=input_val
        dut.inp2.value=input_val
        dut.inp3.value=input_val
        dut.inp4.value=input_val
        dut.inp5.value=input_val
        dut.inp6.value=input_val
        dut.inp7.value=input_val
        dut.inp8.value=input_val
        dut.inp9.value=input_val
        dut.inp10.value=input_val
        dut.inp11.value=input_val
        dut.inp12.value=input_val
        dut.inp13.value=input_val
        dut.inp14.value=input_val
        dut.inp15.value=input_val
        dut.inp16.value=input_val
        dut.inp17.value=input_val
        dut.inp18.value=input_val
        dut.inp19.value=input_val
        dut.inp20.value=input_val
        dut.inp21.value=input_val
        dut.inp22.value=input_val
        dut.inp23.value=input_val
        dut.inp24.value=input_val
        dut.inp25.value=input_val
        dut.inp26.value=input_val
        dut.inp27.value=input_val
        dut.inp28.value=input_val
        dut.inp29.value=input_val
        dut.inp30.value=input_val
        await Timer(2, units='ns')
        dut._log.info(f'Mux_sel={selection} Test_input={input_val} Output_Mux={int(dut.out.value)}')
        # try:
        assert dut.out.value == input_val, f"Multiplexer test failed with: {selection}" 
        # except AssertionError as e:
            # cocotb.log.info(f'The MUX operation failed at selection value {selection}')
            # continue
