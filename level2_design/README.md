# Bit manipulator co-processor Design Verification

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

*The Gitpod id used for hackathon is the below screenshot*

![](https://github.com/vyomasystems-lab/challenges-greeshnad/blob/master/level2_design/bitmanip_ss/gitpod_ss.PNG)

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The design under test (DUT) is a bit manipulator co-processor which takes instruction code and performs the operation corresponding to that instruction.
The problem statement for the design is to compare the output of DUT with output model python file provided. The model python file is bug-free.

All the relevant bits in the 32 bit instruction is looped in python. On assessing the model file, the relevant bits include opcode bits(lsb 7 bits), func7 bits(MSB 7 bits) and variations of func7 like func7_2bit, func3, imm_value among others.

The DUT file has three 32 bit input values which are driven on ``mav_putvalue_src1``, ``mav_putvalue_src2`` and ``mav_putvalue_src1``. The operations are performed on either two or all three inputs.
The LSB of output is 1 if the output is valid.
```
opcode_array=[0x00000033,0x00000013]
for opcode_1 in opcode_array:
instruction=opcode_1
for func3_1 in range(0,8):
  instruction1=(opcode_1>>12)| func3_1
  instruction=(instruction1<<12)|opcode_1

  for imm in range(0,32):
      instruction1=(instruction>>20)| imm
      instruction2=(instruction1<<20)| instruction
      for func7_1 in range(0,128):
          instruction3=(instruction2>>25)| func7_1

          instruction_final=instruction3<<25|instruction2
          expected_mav_putvalue1 = bitmanip(instruction_final, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)

          if expected_mav_putvalue1=='INVALID':
              continue  #if instruction doesnt exist in model.py continue to next iteration

          dut.mav_putvalue_instr.value = instruction_final

          yield Timer(1)

          dut_output1 = dut.mav_putvalue.value #dut output

          # comparison
          error_message = f'Value mismatch DUT = {hex(dut_output1)} does not match MODEL = {hex(expected_mav_putvalue1)} at instruction={hex(instruction_final)}'
          try:
              assert dut_output1 == expected_mav_putvalue1, error_message
          except AssertionError:
              i=i+1
              errors.append(hex(instruction_final))#stores all exception errors i.e model value is not equal to DUT value
```
The assert statement is used for comparing the DUT'S output to the expected model value.
All the errors are stored without stopping simulation using try and except block

## Test Scenario 
```
dut.mav_putvalue_src1.value = 0x76127f56
dut.mav_putvalue_src2.value = 0x2341073
dut.mav_putvalue_src3.value = 0xff62537
dut.EN_mav_putvalue.value = 1
```
Every single valid instruction is tested for above inputs using the python loop code described in previous section.
The error is highlighted in following screenshot.
![](https://github.com/vyomasystems-lab/challenges-greeshnad/blob/master/level2_design/bitmanip_ss/andn_errors.PNG)

The **bugs** identified with the above test is all for one instruction **ANDN**.

## Design Bug
In the DUT mkbitmanip.v file it was difficult to isolate the code where bug is. 
However, I manipulated the model.py file to prove exactly why there is a mismatch in model output and DUT output.
```
if((func7 == "0100000") and (func3 == "111") and (opcode == "0110011") ):
        print('--ANDN 1')
        mav_putvalue=mav_putvalue_src1 & (~mav_putvalue_src2) 
        mav_putvalue=mav_putvalue & 0xffffffff
        mav_putvalue=(mav_putvalue<<1)|1
        return mav_putvalue
```
In the above code snippet of model file if we change ``mav_putvalue=mav_putvalue_src1 & (~mav_putvalue_src2)`` to ``mav_putvalue=mav_putvalue_src1 & (mav_putvalue_src2)`` the assertion error does not occur.
The below screenshot proves it.
![](https://github.com/vyomasystems-lab/challenges-greeshnad/blob/master/level2_design/bitmanip_ss/andn_pass.PNG)

To further prove the test efficacy, I made the 32-bit inputs zero. So, the output must be zero for both ``mav_putvalue=mav_putvalue_src1 & (~mav_putvalue_src2)`` and ``mav_putvalue=mav_putvalue_src1 & (mav_putvalue_src2)``
```
dut.mav_putvalue_src1.value = 0
dut.mav_putvalue_src2.value = 0
dut.mav_putvalue_src3.value = 0
dut.EN_mav_putvalue.value = 1
```
![](https://github.com/vyomasystems-lab/challenges-greeshnad/blob/master/level2_design/bitmanip_ss/andn_0input.PNG)


## Design Fix

From the above section, it can be concluded that if the AND operation in buggy DUT is changed to ANDn operation (like model file) then the bug will be fixed.

## Verification Strategy

- The strategy to test every single instruction in model.py file was achieved through python loop in test file
- Different input values including corner cases like all zeroes and all ones were tested.

## Is the verification complete ?
Yes the verification is complete
