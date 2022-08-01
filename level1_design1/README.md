# Multiplexer Design Verification

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

*The Gitpod id used for hackathon is the below screenshot*

![](https://github.com/vyomasystems-lab/challenges-greeshnad/blob/master/level1_design1/mux_ss/gitpod_ss.PNG)

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The design under test (DUT) is a 31:1 MUX with 5 bit selection line used to determine
which 2 input value to be driven to 2 bit output.

The number of possible values for 5-bit selection line for 31:1 MUX is 31. The 31 values are iterated in a loop variable ``i`` and the sel input of DUT is driven using ``dut.sel.value=i``
. A random 2-bit input_val is generated and driven to 31 input values from ``dut.inp0.value`` to ``dut.inp30.value``.
```
for i in range(0,31):
  input_val=random.randint(1,3)
  selection=i
  dut.sel.value=i 
```
The assert statement is used for comparing the MUX's output to the expected value.
The following two screenshots show the assertion error for failing scenarios.
![](https://github.com/vyomasystems-lab/challenges-greeshnad/blob/master/level1_design1/mux_ss/mux_fail_sel12.PNG)
![](https://github.com/vyomasystems-lab/challenges-greeshnad/blob/master/level1_design1/mux_ss/mux_fail_sel30.PNG)

The following section shows the test scenario for all the selection values and how to show both fail cases shown in above screenshots.
## Test Scenario 
- 31 sel values
- Use try except block to run through all selection values to check for output mismatch
- Random input generated for ``dut.inp0.value`` to ``dut.inp30.value``

The following mismatch highlighted in yellow between MUX expected value(Input_value) and DUT output(Mux_output) are seen:
![](https://github.com/vyomasystems-lab/challenges-greeshnad/blob/master/level1_design1/mux_ss/mux_fail_allcases.PNG)

The **bugs** identified with the above test is for **sel=12** and **sel=30**

## Design Bug
Based on the above test input and analysing the design, we see the following bugs in mux.v

```
5'b01101: out = inp12; =>BUG
//No test case for sel 5'b11110 =>BUG
```
For the MUX design, the logic should be ``5'b01100: out = inp12;`` instead of ``5'b01101: out = inp12;`` as in the design code.
For **sel=30** add ``5'b11110: out = inp30`` line as the last test case. 
The screenshot below shows the bugs fixed
![](https://github.com/vyomasystems-lab/challenges-greeshnad/blob/master/level1_design1/mux_ss/mux_fix.PNG)

## Design Fix
Updating the design as shown in previous section and re-running the test makes the test pass.

![](https://github.com/vyomasystems-lab/challenges-greeshnad/blob/master/level1_design1/mux_ss/mux_pass.PNG)

The expected value(input_value) and DUT output (Mux_output value) are the same and the bugs are fixed

The updated design is checked in as mux_fix.v in fix_design folder

## Verification Strategy

- The strategy to use all possible selection value tests all the scenarios
- Since assertion error stops simulation, use try and except block to test all 31 scenarios and print the failed cases
- Since in mux.v the default value in case block is ``2'b00`` , generate random inputs for inp0 to inp30 from 1 to 3. This ensures that all fail cases are asserted.
eg- For sel=30 if random input value for inp30 happens to be 0 then that test will show a pass case wrongly.

## Is the verification complete ?
Yes, all test scenarios are verified and all bugs are identified. The bugs are fixed as shown in above sections.
