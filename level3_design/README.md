# Universal Shift Register Design Verification

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

*The Gitpod id used for hackathon is the below screenshot*

![](https://github.com/vyomasystems-lab/challenges-greeshnad/blob/master/level2_design/bitmanip_ss/gitpod_ss.PNG)

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The design under test (DUT) is a 4 bit Universal Shift register.
It is implemented using 4:1 MUX and D flip-flops. The select lines for MUX decide the operation which includes no change to current output, left shift, right shift and parallel load

The input values driven are 2 bit select lines, the input for parallel load, right bit will be MSB for right shift and left bit will be LSB for left shift. 
The clear bit acts as active high synchronous reset. The D flip-flop updates on positive edge of input clock 
```
    dut.clear.value = 0
    input_val=0b0111
    dut.S.value = 3
    dut.I.value = 0b0111
    left=1
    right=1
    dut.right.value=right
    dut.left.value=left
```
The assert statement is used for comparing the USR's output to the expected value.


The following section shows the test scenario for all the selection values and how to show both fail cases shown in above screenshots.
## Test Scenario 
- 2 bit select value
- Use try except block to run through all selection values to check for output mismatch
- left=1 and right=1
- Input=7 (3'b0111)

The following mismatch between expected value and DUT output are seen:
![](https://github.com/vyomasystems-lab/challenges-greeshnad/blob/master/level3_design/usr_ss/usr_fails.PNG)
![](https://github.com/vyomasystems-lab/challenges-greeshnad/blob/master/level3_design/usr_ss/usr_fail.PNG)

The **bugs** identified with the above test is for **sel=2** and **sel=3**

## Design Bug
Based on the above test input and analysing the design, we see the following bugs in mux.v

```
Mux_4_to_1 inst1(D_temp[0] , S , O[0] , left , O[1] , I[0] );
Mux_4_to_1 inst2(D_temp[1] , S , O[1] , O[0] , O[2] , I[1] );
Mux_4_to_1 inst3(D_temp[2] , S , O[2] , O[1] , O[3] , I[3] );=>BUG
Mux_4_to_1 inst4(D_temp[3] , S , O[3] , O[2] , 1'b0 ,I[3] );=>BUG
```
The bug for sel=3 must be fixed by changing ``Mux_4_to_1 inst3(D_temp[2] , S , O[2] , O[1] , O[3] , I[3] );`` to ``Mux_4_to_1 inst3(D_temp[2] , S , O[2] , O[1] , O[3] , I[2] );``
The bug for sel=2 must be fixed by changing ``Mux_4_to_1 inst4(D_temp[3] , S , O[3] , O[2] , 1'b0 ,I[3] );`` to ``Mux_4_to_1 inst4(D_temp[3] , S , O[3] , O[2] , right ,I[3] );`` 
![](https://github.com/vyomasystems-lab/challenges-greeshnad/blob/master/level3_design/usr_ss/usr_bug.PNG)

## Design Fix
Updating the design as shown in previous section and re-running the test makes the test pass.

![](https://github.com/vyomasystems-lab/challenges-greeshnad/blob/master/level3_design/usr_ss/usr_pass.PNG)

The expected value and DUT output are the same and the bugs are fixed

The updated design is checked in as usr_fix.v in fix_design folder

## Verification Strategy

- The strategy to use all possible selection value tests all the scenarios
- Since assertion error stops simulation, use try and except block to test all scenarios and print the failed cases
- Test clear=1 case too

## Is the verification complete ?
Yes, all test scenarios are verified and all bugs are identified. The bugs are fixed as shown in above sections.
