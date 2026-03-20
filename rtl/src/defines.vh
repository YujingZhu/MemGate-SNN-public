// =============================================================================
// MPCG Module Parameter Definitions
// Fixed-point: Q8.8 format (8-bit integer + 8-bit fraction, signed)
// Target: Xilinx Zynq-7000 (xc7z020clg400-1)
// =============================================================================

`ifndef MPCG_DEFINES_VH
`define MPCG_DEFINES_VH

// ---------- Fixed-point format ----------
parameter DATA_WIDTH    = 16;          // Q8.8 total bits
parameter FRAC_BITS     = 8;           // fractional bits
parameter INT_BITS      = 8;           // integer bits (including sign)

// ---------- Network dimensions ----------
parameter NUM_CLASSES   = 10;          // output classes (MNIST/CIFAR-10)
parameter TIMESTEPS     = 4;           // T = 4 temporal steps
parameter LOG2_T        = 2;           // log2(TIMESTEPS) for shift-divide

// ---------- LUT parameters ----------
// Softmax LUT range: exp(x) for x in [-8.0, 0.0] (subtract-max stable)
// Address mapping: addr = (diff_q + 2048) >> 3, where diff_q = v[i] - max(v) in Q8.8
parameter LUT_ADDR_BITS = 8;           // 256 entries
parameter LUT_DEPTH     = 256;         // 2^LUT_ADDR_BITS
parameter LUT_DATA_BITS = 16;          // Q8.8 output

// ---------- EMA parameters (Q8.8 fixed-point) ----------
// beta = 0.9 ≈ 230/256 = 0.8984 in Q0.8
parameter [7:0] BETA_FRAC       = 8'd230;    // 230/256 ≈ 0.898
parameter [7:0] ONE_MINUS_BETA  = 8'd26;     // 26/256 ≈ 0.102
parameter [DATA_WIDTH-1:0] COLD_START_THETA = 16'h00B3;  // 0.7 in Q8.8 = 179 ≈ 0xB3

// ---------- Cold start ----------
parameter COLD_START_BATCHES = 100;

// ---------- DNLP parameters ----------
// steepness k = 5 (used to pre-compute sigmoid LUT)
// min_weight = 0.05 in Q8.8 = 13 ≈ 0x000D
parameter [DATA_WIDTH-1:0] MIN_WEIGHT = 16'h000D;  // 0.05 * 256 ≈ 13
// 1.0 - min_weight = 0.95 in Q8.8 = 243 ≈ 0x00F3
parameter [DATA_WIDTH-1:0] WEIGHT_RANGE = 16'h00F3;

// ---------- Q8.8 constants ----------
parameter [DATA_WIDTH-1:0] ONE_Q8  = 16'h0100;  // 1.0 in Q8.8
parameter [DATA_WIDTH-1:0] ZERO_Q8 = 16'h0000;  // 0.0 in Q8.8

`endif
