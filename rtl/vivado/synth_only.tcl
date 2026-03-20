# =============================================================================
# Phase A: Synthesis Only — extract area data quickly
# Target: Xilinx Zynq-7000 xc7z020clg400-1
# Usage: vivado -mode batch -source synth_only.tcl
# =============================================================================

set_param general.maxThreads 8

set project_name "mpcg_synth"
set project_dir  "./vivado_project"
set part_name    "xc7z020clg400-1"
set top_module   "mpcg_top"

# Create project
create_project $project_name $project_dir -part $part_name -force

# Add RTL sources
add_files [glob ../src/*.v]
add_files [glob ../src/*.vh]

# Add constraint file
add_files -fileset constrs_1 constraints.xdc

# Add LUT initialization files
add_files ../scripts/softmax_lut.mem
add_files ../scripts/sigmoid_lut.mem

# Set top module
set_property top $top_module [current_fileset]
set_property include_dirs {../src} [current_fileset]

# Update compile order
update_compile_order -fileset sources_1

# =============================================================================
# Synthesis
# =============================================================================
puts "=== Starting Synthesis ==="

set_property strategy Flow_PerfOptimized_high [get_runs synth_1]
set_property STEPS.SYNTH_DESIGN.ARGS.DIRECTIVE AreaOptimized_high [get_runs synth_1]

launch_runs synth_1 -jobs 8
wait_on_run synth_1

if {[get_property STATUS [get_runs synth_1]] != "synth_design Complete!"} {
    puts "ERROR: Synthesis failed!"
    exit 1
}
puts "=== Synthesis Complete ==="

# Generate post-synthesis reports
open_run synth_1
report_utilization -file ${project_dir}/synth_util.txt
report_utilization -hierarchical -file ${project_dir}/synth_util_hier.txt
report_timing_summary -file ${project_dir}/synth_timing.txt

puts ""
puts "========================================"
puts "Phase A: Synthesis Complete"
puts "Reports: ${project_dir}/synth_util*.txt"
puts "========================================"

# Do NOT exit — leave project for impl_only.tcl to open
exit 0
