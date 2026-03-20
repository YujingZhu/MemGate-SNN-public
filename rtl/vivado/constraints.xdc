# =============================================================================
# Constraints for MPCG module on Zynq-7000 (xc7z020clg400-1)
# =============================================================================

# Primary clock: 100 MHz
create_clock -period 10.000 -name sys_clk [get_ports clk]

# Clock uncertainty for setup/hold analysis
set_clock_uncertainty -setup 0.100 [get_clocks sys_clk]
set_clock_uncertainty -hold  0.050 [get_clocks sys_clk]

# Input delay constraints (relative to clock)
set_input_delay -clock sys_clk -max 2.0 [get_ports {v_in[*]}]
set_input_delay -clock sys_clk -min 0.5 [get_ports {v_in[*]}]
set_input_delay -clock sys_clk -max 2.0 [get_ports valid_in]
set_input_delay -clock sys_clk -min 0.5 [get_ports valid_in]
set_input_delay -clock sys_clk -max 2.0 [get_ports mode_train]
set_input_delay -clock sys_clk -min 0.5 [get_ports mode_train]
set_input_delay -clock sys_clk -max 2.0 [get_ports warmup]
set_input_delay -clock sys_clk -min 0.5 [get_ports warmup]
set_input_delay -clock sys_clk -max 2.0 [get_ports rst_n]
set_input_delay -clock sys_clk -min 0.5 [get_ports rst_n]

# Output delay constraints
set_output_delay -clock sys_clk -max 2.0 [get_ports {weight[*]}]
set_output_delay -clock sys_clk -min 0.5 [get_ports {weight[*]}]
set_output_delay -clock sys_clk -max 2.0 [get_ports weight_valid]
set_output_delay -clock sys_clk -min 0.5 [get_ports weight_valid]
set_output_delay -clock sys_clk -max 2.0 [get_ports {pred_class[*]}]
set_output_delay -clock sys_clk -min 0.5 [get_ports {pred_class[*]}]
set_output_delay -clock sys_clk -max 2.0 [get_ports pred_valid]
set_output_delay -clock sys_clk -min 0.5 [get_ports pred_valid]
set_output_delay -clock sys_clk -max 2.0 [get_ports {pred_conf[*]}]
set_output_delay -clock sys_clk -min 0.5 [get_ports {pred_conf[*]}]
set_output_delay -clock sys_clk -max 2.0 [get_ports {theta_out[*]}]
set_output_delay -clock sys_clk -min 0.5 [get_ports {theta_out[*]}]
set_output_delay -clock sys_clk -max 2.0 [get_ports {mpcg_conf[*]}]
set_output_delay -clock sys_clk -min 0.5 [get_ports {mpcg_conf[*]}]

# False paths for mode control signals (quasi-static)
set_false_path -from [get_ports mode_train]
set_false_path -from [get_ports warmup]
