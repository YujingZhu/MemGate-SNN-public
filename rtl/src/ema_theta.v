// =============================================================================
// Block 2c: EMA Theta Update
// Exponential Moving Average for adaptive threshold:
//   theta_{k+1} = beta * theta_k + (1-beta) * mpcg_mean
// With cold-start: theta = 0.7 for first 100 batches
// =============================================================================

`include "defines.vh"

module ema_theta (
    input  wire                  clk,
    input  wire                  rst_n,
    input  wire                  update_en,     // pulse to trigger EMA update
    input  wire [DATA_WIDTH-1:0] mpcg_mean,     // batch mean MPCG confidence (Q8.8)
    output reg  [DATA_WIDTH-1:0] theta           // current threshold (Q8.8)
);

    // =========================================================================
    // Implementation removed for IP protection.
    // Contact the authors for the full implementation.
    // =========================================================================

    // Tie off outputs (stub only - not functional)
    assign theta = COLD_START_THETA;

endmodule
