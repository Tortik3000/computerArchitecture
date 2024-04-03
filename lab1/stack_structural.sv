
module DTrigger(
    output q, nq,
    input d, clk, reset
);
    wire _1, _2, _3, _4;
    not(_1, d);
    and(_2, clk, _1);
    and(_3, clk, d);
    nor(q, _2, nq);
    nor(_4, q, _3);
    or(nq, reset, _4);
endmodule


module _3to8decodder(
    output [7:0]q,
    input bit0, bit1, bit2
    
);
    wire nbit0, nbit1, nbit2;
    not(nbit0, bit0);
    not(nbit1, bit1);
    not(nbit2, bit2);
   

    and(q[0], nbit0, nbit1, nbit2);
    and(q[1], bit0,  nbit1, nbit2);
    and(q[2], nbit0, bit1,  nbit2);
    and(q[3], bit0,  bit1,  nbit2);
    and(q[4], nbit0, nbit1, bit2);
    and(q[5], bit0,  nbit1, bit2);
    and(q[6], nbit0, bit1,  bit2);
    and(q[7], bit0,  bit1,  bit2);
endmodule


module littleCellue(
    output q0, q1, q2, q3, q4,
    input d0, d1, d2, d3, d4,
    input clk, reset
    
);
    DTrigger trigger0(.d(d0), .clk(clk), .reset(reset), .q(q0));
    DTrigger trigger1(.d(d1), .clk(clk), .reset(reset), .q(q1));
    DTrigger trigger2(.d(d2), .clk(clk), .reset(reset), .q(q2));
    DTrigger trigger3(.d(d3), .clk(clk), .reset(reset), .q(q3));
    DTrigger trigger4(.d(d4), .clk(clk), .reset(reset), .q(q4));
endmodule


module convert(
    output q,
    input pushQ, push, pop, popQ
    
);
    wire w1, w2;
    and(w1, push, pushQ);
    and(w2, pop, popQ);
    or(q, w1, w2);
endmodule


module MUX(
    output q,
    input bit0, bit1, bit2,
    input d0, d1, d2, d3, d4
    

);
    wire [7:0]out;
    wire a0, a1, a2, a3, a4;
    wire index0, index1, index2;

    _3to8decodder dec(.bit0(bit0), .bit1(bit1), .bit2(bit2), .q(out));
    or(index0, out[0], out[5]);
    or(index1, out[1], out[6]);
    or(index2, out[2], out[7]);
    and(a0, d0, index0);
    and(a1, d1, index1);
    and(a2, d2, index2);
    and(a3, d3, out[3]);
    and(a4, d4, out[4]);
    or(q, a0, a1, a2, a3, a4);
endmodule


module cellue(
    output outBit,
    input [2:0]index,
    input push, pop, get, inBit,reset
    
);
    wire shift, notShift;
    or(shift, push, pop);
    not(notShift, shift);

    littleCellue mainCellue(.clk(shift), .reset(reset), .d0(d0), .d1(d1), .d2(d2), .d3(d3), .d4(d4), .q0(c0), .q1(c1), .q2(c2), .q3(c3), .q4(c4));
    littleCellue pushCellue(.clk(notShift), .reset(reset), .d0(c4), .d1(c0), .d2(c1), .d3(c2), .d4(c3), .q0(q0Push), .q1(q1Push), .q2(q2Push), .q3(q3Push), .q4(q4Push));
    littleCellue popCellue(.clk(notShift), .reset(reset), .d0(c1), .d1(c2), .d2(c3), .d3(c4), .d4(c0), .q0(q0Pop), .q1(q1Pop), .q2(q2Pop), .q3(q3Pop), .q4(q4Pop));

    wire _1, _2, _3, _4, getBit, pushBit, popBit;
    and(_1, shift, inBit);
    and(_2, notShift, q0Push);
    or(_3, _1, _2);

    convert Pu0(.pushQ(_3), .push(push), .pop(pop), .popQ(q0Pop), .q(d0));
    convert Pu1(.pushQ(q1Push), .push(push), .pop(pop), .popQ(q1Pop), .q(d1));
    convert Pu2(.pushQ(q2Push), .push(push), .pop(pop), .popQ(q2Pop), .q(d2));
    convert Pu3(.pushQ(q3Push), .push(push), .pop(pop), .popQ(q3Pop), .q(d3));
    convert Pu4(.pushQ(q4Push), .push(push), .pop(pop), .popQ(q4Pop), .q(d4));

    MUX Index(.bit0(index[0]), .bit1(index[1]), .bit2(index[2]), .d0(c0), .d1(c1), .d2(c2), .d3(c3), .d4(c4), .q(_4));
    and(getBit, get, _4);
    and(pushBit, push, _3);
    and(popBit, pop, q1Push);
    or(outBit, getBit, pushBit, popBit);
endmodule




module stack_structural_normal(
 inout wire[3:0] IO_DATA, 
input wire RESET, 
   input wire CLK, 
   input wire[1:0] COMMAND,
   input wire[2:0] INDEX
   ); 
   wire [7:0]outDec;
   wire [3:0]out;
    _3to8decodder dec(.bit0(COMMAND[0]), .bit1(COMMAND[1]), .bit2(1'b0), .q(outDec));
    wire push, pop, get;
    and(push, CLK, outDec[1]);
    and(pop, CLK, outDec[2]);
    and(get, CLK, outDec[3]);

    cellue cel0(.push(push), .reset(RESET), .pop(pop), .get(get), .index(INDEX), .inBit(IO_DATA[0]), .outBit(out[0]));
    cellue cel1(.push(push), .reset(RESET), .pop(pop), .get(get), .index(INDEX), .inBit(IO_DATA[1]), .outBit(out[1]));
    cellue cel2(.push(push), .reset(RESET), .pop(pop), .get(get), .index(INDEX), .inBit(IO_DATA[2]), .outBit(out[2]));
    cellue cel3(.push(push), .reset(RESET), .pop(pop), .get(get), .index(INDEX), .inBit(IO_DATA[3]), .outBit(out[3]));

    wire write, show;
    
    and(show, COMMAND[1], CLK);
    not(write, show);
    
    cmos(IO_DATA[0], out[0], show, write);
    cmos(IO_DATA[1], out[1], show, write);
    cmos(IO_DATA[2], out[2], show, write);
    cmos(IO_DATA[3], out[3], show, write);

    


endmodule
