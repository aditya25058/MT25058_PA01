#!/bin/bash

# Part C: Comprehensive Measurement Collection Script
# Graduate Systems PA01 - Processes and Threads
# Roll Number: MT25058
# 
# This script measures CPU%, Memory, and I/O metrics for all 6 combinations:
# - Program A (Processes) + CPU worker
# - Program A (Processes) + Memory worker
# - Program A (Processes) + I/O worker
# - Program B (Threads) + CPU worker
# - Program B (Threads) + Memory worker
# - Program B (Threads) + I/O worker

OUT="MT25058_Part_C_CSV.csv"

# CSV Header: Program,Worker,CPU_Percent,Memory_MB,IO_KB_s,Exec_Time_s
echo "Program,Worker,CPU_Percent,Memory_MB,IO_KB_s,Exec_Time_s" > "$OUT"

WORKERS=("cpu" "mem" "io")

echo "==============================================="
echo "Part C: Program and Worker Combination Measurements"
echo "==============================================="

# Function to extract metrics from time -v output
extract_metrics() {
    local output="$1"
    # Extract CPU percentage: "Percent of CPU this job got: 82%"
    local cpu_percent=$(echo "$output" | grep "Percent of CPU this job got:" | awk '{print $NF}' | sed 's/%//' || echo "0")
    # Extract maximum resident set size (in kbytes): "Maximum resident set size (kbytes): 1792"
    local max_rss_kb=$(echo "$output" | grep "Maximum resident set size" | awk '{print $NF}' || echo "0")
    # Convert KB to MB
    local max_rss=$(echo "scale=2; $max_rss_kb / 1024" | bc)
    echo "$cpu_percent,$max_rss"
}

# Function to measure Program A (Processes)
measure_program_a() {
    local worker=$1
    echo "  [Program A] Testing with $worker worker (2 processes)..."
    
    # Get initial I/O counters from diskstats
    local io_before=$(cat /proc/diskstats 2>/dev/null | awk 'NR==2 {print $6}' || echo "0")
    
    # Run program with time command
    local start_time=$(date +%s%N)
    local output=$(/usr/bin/time -v ./program_A "$worker" 2 2>&1)
    local end_time=$(date +%s%N)
    
    # Get final I/O counters
    local io_after=$(cat /proc/diskstats 2>/dev/null | awk 'NR==2 {print $6}' || echo "0")
    
    # Calculate metrics
    local exec_time=$(echo "scale=4; ($end_time - $start_time) / 1000000000" | bc)
    local io_diff=$(echo "$io_after - $io_before" | bc)
    
    # Extract CPU% and Memory from time output
    local metrics=$(extract_metrics "$output")
    
    echo "A,$worker,$metrics,$io_diff,$exec_time" >> "$OUT"
}

# Function to measure Program B (Threads)
measure_program_b() {
    local worker=$1
    echo "  [Program B] Testing with $worker worker (2 threads)..."
    
    # Get initial I/O counters
    local io_before=$(cat /proc/diskstats 2>/dev/null | awk 'NR==2 {print $6}' || echo "0")
    
    # Run program with time command
    local start_time=$(date +%s%N)
    local output=$(/usr/bin/time -v ./program_B "$worker" 2 2>&1)
    local end_time=$(date +%s%N)
    
    # Get final I/O counters
    local io_after=$(cat /proc/diskstats 2>/dev/null | awk 'NR==2 {print $6}' || echo "0")
    
    # Calculate metrics
    local exec_time=$(echo "scale=4; ($end_time - $start_time) / 1000000000" | bc)
    local io_diff=$(echo "$io_after - $io_before" | bc)
    
    # Extract CPU% and Memory from time output
    local metrics=$(extract_metrics "$output")
    
    echo "B,$worker,$metrics,$io_diff,$exec_time" >> "$OUT"
}

# Run measurements for all combinations
for w in "${WORKERS[@]}"; do
    echo ""
    echo "Testing worker type: $w"
    measure_program_a "$w"
    sleep 1
    measure_program_b "$w"
    sleep 1
done

echo ""
echo "==============================================="
echo "Part C Measurements Complete!"
echo "Output saved to: $OUT"
echo "CSV Format: Program,Worker,CPU_Percent,Memory_MB,IO_KB_s,Exec_Time_s"
echo "==============================================="

# Display results if column command is available
if command -v column &> /dev/null; then
    echo ""
    echo "Summary of Results:"
    column -t -s',' "$OUT"
fi

