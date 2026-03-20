// =============================================================================
// Block 2a: Softmax LUT (Subtract-Max Stable, Area-Optimized)
// Numerically stable softmax using subtract-max trick:
//   Stage 0: 10-way comparator finds V_max
//   Stage 1: diff[i] = V_i - V_max, LUT lookup for exp(diff)
//   Stage 2: Sum exp values
//   Stage 3: max_prob = ONE / sum  (16-stage pipelined restoring divider)
//
// Key optimization: argmax(exp_val) == argmax(softmax), so prob_out carries
// unnormalized exp values — downstream argmax_comparator still finds the
// correct class.  Only max_prob (MPCG_n) needs the single division.
//
// Input:  signed Q8.8 values (10 classes)
// Output: Q8.8 exp values (unnormalized) + max probability (MPCG_n)
// =============================================================================

`include "defines.vh"

module softmax_lut (
    input  wire                    clk,
    input  wire                    rst_n,
    input  wire                    valid_in,
    input  wire [NUM_CLASSES*DATA_WIDTH-1:0] mean_v,  // 10 x Q8.8
    output reg                     valid_out,
    output reg  [NUM_CLASSES*DATA_WIDTH-1:0] prob_out, // 10 x Q8.8 (unnormalized exp)
    output reg  [DATA_WIDTH-1:0]   max_prob             // max(prob), i.e., MPCG_n
);

    // =========================================================================
    // Implementation removed for IP protection.
    // Contact the authors for the full implementation.
    // =========================================================================

    // Tie off outputs (stub only - not functional)
    assign valid_out = 1'b0;
    assign prob_out = {NUM_CLASSES*DATA_WIDTH{1'b0}};
    assign max_prob = {DATA_WIDTH{1'b0}};

endmodule
