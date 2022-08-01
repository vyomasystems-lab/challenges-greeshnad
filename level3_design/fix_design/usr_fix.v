// Code your design here
`timescale 1ns / 1ps
module Universal_shift_reg(O , clk , clear, right, left , S , I);

input clk , clear ,right,left;
input [2 : 0] S ; 
input [3 : 0] I; 
output [3 : 0] O;
wire [3 : 0] D_temp;

Mux_4_to_1 inst1(D_temp[0] , S , O[0] , left , O[1] , I[0] );
Mux_4_to_1 inst2(D_temp[1] , S , O[1] , O[0] , O[2] , I[1] );
Mux_4_to_1 inst3(D_temp[2] , S , O[2] , O[1] , O[3] , I[2] );
Mux_4_to_1 inst4(D_temp[3] , S , O[3] , O[2] , right , I[3] );

D_FlipFlop D_inst1(O[0] , D_temp[0] , clk , clear);
D_FlipFlop D_inst2(O[1] , D_temp[1] , clk , clear);
D_FlipFlop D_inst3(O[2] , D_temp[2] , clk , clear);
D_FlipFlop D_inst4(O[3] , D_temp[3] , clk , clear);

endmodule

`timescale 1ns / 1ps

module Mux_4_to_1(Mux_Out , S , in0 , in1 , in2 , in3);

output reg Mux_Out;
input [2:0] S;
input in0 , in1 , in2 , in3 ;

always@(*)
begin
	case(S)
		
		2'b00 : Mux_Out = in0;
		2'b01 : Mux_Out = in1;
		2'b10 : Mux_Out = in2;
		2'b11 : Mux_Out = in3;
	endcase
end

endmodule
`timescale 1ns / 1ps

module D_FlipFlop(O , D , clk , clear);

input D , clk , clear;
output reg O;

always@(posedge clk)
begin
	
	if(clear == 1'b1)
		O <= 1'b0;
	else
		O <= D;
	
end
endmodule