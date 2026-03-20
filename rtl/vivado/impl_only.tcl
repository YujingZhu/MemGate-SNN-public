# =============================================================================
# Phase B: Implementation (P&R) + Power + Timing
# Requires: Phase A (synth_only.tcl) to have completed successfully
# Usage: vivado -mode batch -source impl_only.tcl
# =============================================================================

set_param general.maxThreads 8

set project_name "mpcg_synth"
set project_dir  "./vivado_project"

# Open existing project from Phase A
open_project ${project_dir}/${project_name}.xpr

# =============================================================================
# Implementation (Place & Route)
# =============================================================================
puts "=== Starting Implementation ==="

launch_runs impl_1 -jobs 8
wait_on_run impl_1

if {[get_property STATUS [get_runs impl_1]] != "route_design Complete!"} {
    puts "ERROR: Implementation failed!"
    # Write fail marker
    set fp [open "${project_dir}/IMPL_FAILED.txt" w]
    puts $fp "Implementation failed at [clock format [clock seconds]]"
    close $fp
    exit 1
}
puts "=== Implementation Complete ==="

# =============================================================================
# Post-Implementation Reports
# =============================================================================
open_run impl_1

# Utilization
report_utilization -file ${project_dir}/impl_util.txt
report_utilization -hierarchical -file ${project_dir}/impl_util_hier.txt

# Timing
report_timing_summary -file ${project_dir}/impl_timing.txt
report_timing -max_paths 10 -file ${project_dir}/impl_timing_detail.txt

# Check timing slack
set wns [get_property STATS.WNS [get_runs impl_1]]
puts "=== Worst Negative Slack (WNS): ${wns} ns ==="
if {$wns < 0} {
    puts "WARNING: Timing NOT met! WNS = ${wns} ns"
    set fp [open "${project_dir}/TIMING_FAIL.txt" w]
    puts $fp "WNS = ${wns} ns — timing constraint violated"
    close $fp
} else {
    puts "Timing met: WNS = ${wns} ns (100 MHz OK)"
}

# Power (with switching activity estimation)
set_switching_activity -toggle_rate 12.5 -static_probability 0.5 [get_nets *]
report_power -file ${project_dir}/impl_power.txt

puts ""
puts "========================================"
puts "Phase B: Implementation Complete"
puts "WNS: ${wns} ns"
puts "Reports: ${project_dir}/impl_*.txt"
puts "========================================"

exit 0
