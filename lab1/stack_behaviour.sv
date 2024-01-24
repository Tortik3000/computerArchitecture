
module stack_behaviour_easy(
   
    output wire[3:0] O_DATA, 
    input wire RESET, 
    input wire CLK, 
    input wire[1:0] COMMAND, 
    input wire[2:0] INDEX,
    input wire[3:0] I_DATA
    ); 
    reg [19:0] arr ;
    reg [3:0]od;
    reg  [3:0]a0;
    wire push = (COMMAND[0] & !COMMAND[1]);
    wire pop = (!COMMAND[0] & COMMAND[1]);
    wire get = (COMMAND[0] & COMMAND[1]);
    assign O_DATA = od;
    

    always @(posedge CLK) begin
        if (push) begin
            arr[19:4] = arr[15:0];
            arr[3:0] = I_DATA;
            od[3:0] = arr[3:0];
        end

        if (pop) begin
            a0[3:0] = arr[3:0];
            arr[15:0] = arr[19:4];
            arr[19:16] = a0[3:0];
            od = a0;
        end

        if (get) begin
            if (INDEX == 3'd0) begin
                od = arr[3:0];
            end

            if (INDEX == 3'd1) begin
                od = arr[7:4];
            end

            if (INDEX == 3'd2) begin
                od = arr[11:8];
            end

            if (INDEX == 3'd3) begin
                od = arr[15:12];
            end

            if (INDEX == 3'd4) begin
                od = arr[19:16];
            end
   
        end
    end

    always @(posedge RESET) begin
        arr = 20'b0;
    end

endmodule




// module stack_behaviour_normal(
//     inout wire[3:0] IO_DATA, 
//     input wire RESET, 
//     input wire CLK, 
//     input wire[1:0] COMMAND,
//     input wire[2:0] INDEX
//     ); 
//     reg [19:0] arr ;
//     reg [3:0]od;
//     reg  [3:0]a0;
//     wire push = (COMMAND[0] & !COMMAND[1]);
//     wire pop = (!COMMAND[0] & COMMAND[1]);
//     wire get = (COMMAND[0] & COMMAND[1]);
//     assign IO_DATA = od;
    

//     always @(posedge CLK) begin
//         if (push) begin
//             arr[19:4] = arr[15:0];
//             arr[3:0] = IO_DATA;
//             od[3:0] = arr[3:0];
//         end

//         if (pop) begin
//             a0[3:0] = arr[3:0];
//             arr[15:0] = arr[19:4];
//             arr[19:16] = a0[3:0];
//             od = a0;
//         end

//         if (get) begin
//             if (INDEX == 3'd0) begin
//                 od = arr[3:0];
//             end

//             if (INDEX == 3'd1) begin
//                 od = arr[7:4];
//             end

//             if (INDEX == 3'd2) begin
//                 od = arr[11:8];
//             end

//             if (INDEX == 3'd3) begin
//                 od = arr[15:12];
//             end

//             if (INDEX == 3'd4) begin
//                 od = arr[19:16];
//             end
   
//         end
//     end

//     always @(posedge RESET) begin
//         arr = 20'b0;
//     end
//     // put your code here, the other module (stack_behaviour_easy) must be deleted

// endmodule
