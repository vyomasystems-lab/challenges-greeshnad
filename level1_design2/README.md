# Sequence detector 1011 Design Verification

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

*The Gitpod id used for hackathon is the below screenshot*

![](https://github.com/vyomasystems-lab/challenges-greeshnad/blob/master/level2_design/bitmanip_ss/gitpod_ss.PNG)

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The design under test (DUT) is a overlapping 1011 sequence detector. If the sequence is detected seq_seen bit goes high.
The design overlaps only with non sequences as confirmed in LMS video and slack channel of hackathon.

The 1 bit value is driven on the input port inp_bit. The output is triggered at positive edge of clock. The output is updated at the next positive edge of when inp_bit is updated.
The assert statement is used at the end of the sequence to check if seq_seen is asserted. 
The input sequence ``101011`` is overlapping 1011 sequence with a non-sequence.
```
input_array=[1,0,1,0,1,1]
for inp in input_array:
        
  dut.inp_bit.value=inp
  dut._log.info('current_state=%s',dut.current_state.value)
  await RisingEdge(dut.clk)
  await Timer(1, units='ns')
  dut._log.info('final_state=%s',dut.current_state.value)
  i=i+1
  if dut.seq_seen.value == 1:
      j=j+1
  if(i==le):
      print("The number of 1011 sequence overlap with non-sequence detected=",j)
      assert dut.seq_seen.value == 1, "Sequence_detector failed" 
```

The following section shows different test scenarios and their corresponding bugs
## Test Scenario 
**Scenario 1**
- input_seq=101011 
- Next state updated every posedge of clock

The final_state in all screenshots corresponds to next_state in the design.
The following screenshot shows the assertion error for above scenario. After 101 sequence when 4th bit 0 is forced on inp_bit the FSM goes to IDLE(000) state(yellow highlighted final state) instead of expected SEQ_10(010)state.
![](https://github.com/vyomasystems-lab/challenges-greeshnad/blob/master/level1_design2/seq_ss/fail_101011.PNG)
**Scenario 2**
- input_seq=11011 
- Next state updated every posedge of clock

The following screenshot shows the assertion error for above scenario. After first bit 1,  when 2nd bit 1 is forced on inp_bit the FSM goes to IDLE(000) state(yellow highlighted final state) instead of expected SEQ_1(001)state.
![](https://github.com/vyomasystems-lab/challenges-greeshnad/blob/master/level1_design2/seq_ss/fail_11011.PNG)

**Scenario 3**
- input_seq=10111011 
- Two valid 1011 sequence with no overlap between them
- Next state updated every posedge of clock

The following screenshot shows the assertion error for above scenario. First sequence is detected and marked by state SEQ_1011(100). However when next valid sequence starts again 1011, it goes to IDLE state as shown in yellow instead of going to SEQ_1 state.
![](https://github.com/vyomasystems-lab/challenges-greeshnad/blob/master/level1_design2/seq_ss/fail_10111011.PNG)

## Design Bug
Based on the above test input and analysing the design, we see the following bugs in the design

```
SEQ_1:
      begin
        if(inp_bit == 1)
          next_state = IDLE; => BUG
        else
          next_state = SEQ_10;
```

```
SEQ_101:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1011;
        else
          next_state = IDLE; => BUG
```
```
SEQ_1011:
      begin
        next_state = IDLE; =>BUG
      end
```

The screenshot below shows all the bugs above fixed
![](https://github.com/vyomasystems-lab/challenges-greeshnad/blob/master/level1_design2/seq_ss/bug_fix.PNG)

## Design Fix
All the scenarios described above are ran with fixed code and the pass outputs are shown.

**Scenario 1 pass**
![](https://github.com/vyomasystems-lab/challenges-greeshnad/blob/master/level1_design2/seq_ss/pass_101011.PNG)

**Scenario 2 pass**
![](https://github.com/vyomasystems-lab/challenges-greeshnad/blob/master/level1_design2/seq_ss/pass_11011.PNG)

**Scenario 3 pass**
![](https://github.com/vyomasystems-lab/challenges-greeshnad/blob/master/level1_design2/seq_ss/pass_10111011.PNG)

The fixed code is checked in design_fix folder under seq_detect_1011_fix.v name.

## Verification Strategy

- The goal is to check check overlapping non-sequence. So test different scenarios are tested as above.
- Reset=1 scenario is tested and verified that current_state is IDLE.
- Scenario 3 bug presented and fixed above is done assuming the original bug-free DUT is supposed to detect two valid sequences with no overlap between them. If that scenario is not needed then, SEQ_1011 state will always have next state as IDLE.
- Two Valid sequences with overlap between them will give a failed test as described in LMS video. eg- 1011011 input_sequence will fail even in seq_detect_1011_fix.v 
## Is the verification complete ?
Yes, the verification is complete and different scenarios can be tested
