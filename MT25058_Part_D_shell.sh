#!/bin/bash

# Part D: Scaling Analysis
# Graduate Systems PA01 - Processes and Threads
# Roll Number: MT25058
# 
# Tests multiple process/thread counts and measures performance metrics
# Output: MT25058_Part_D_CSV.csv

OUT="MT25058_Part_D_CSV.csv"

# Header: Type,Count,CPU_Percent,Memory_MB,User_CPU_s,Sys_CPU_s,Real_Time_s
echo "Type,Count,CPU_Percent,Memory_MB,User_CPU_s,Sys_CPU_s,Real_Time_s" > "$OUT"

echo "==============================================="
echo "Part D: Process/Thread Scaling Analysis"
echo "==============================================="

# Function to extract metrics from time -v output
extract_scaling_metrics() {
    local output="$1"
    local cpu_percent=$(echo "$output" | grep "Percent of CPU this job got:" | awk '{print $NF}' | sed 's/%//' || echo "0")
    local max_rss_kb=$(echo "$output" | grep "Maximum resident set size" | awk '{print $NF}' || echo "0")
    local max_rss=$(echo "scale=2; $max_rss_kb / 1024" | bc)
    local user_cpu=$(echo "$output" | grep "User time (seconds):" | awk '{print $NF}' || echo "0")
    local sys_cpu=$(echo "$output" | grep "System time (seconds):" | awk '{print $NF}' || echo "0")
    local real_time=$(echo "$output" | grep "Elapsed (wall clock) time" | awk '{print $NF}' || echo "0")
    
    echo "$cpu_percent,$max_rss,$user_cpu,$sys_cpu,$real_time"
}

# Test Program A (Processes) with varying counts
echo ""
echo "Testing Program A (Processes) with CPU worker..."
echo "================================================="
for P in 2 3 4 5; do
  echo "  Testing with $P processes..."
  OUTPUT=$(/usr/bin/time -v ./program_A cpu $P 2>&1)
  
  METRICS=$(extract_scaling_metrics "$OUTPUT")
  echo "Process,$P,$METRICS" >> "$OUT"
  sleep 1
done

# Test Program B (Threads) with varying counts
echo ""
echo "Testing Program B (Threads) with CPU worker..."
echo "=============================================="
for T in 2 3 4 5 6 7 8; do
  echo "  Testing with $T threads..."
  OUTPUT=$(/usr/bin/time -v ./program_B cpu $T 2>&1)
  
  METRICS=$(extract_scaling_metrics "$OUTPUT")
  echo "Thread,$T,$METRICS" >> "$OUT"
  sleep 1
done

echo ""
echo "==============================================="
echo "Part D Scaling Analysis Complete!"
echo "Output saved to: $OUT"
echo "CSV format: Type,Count,CPU_Percent,Memory_MB,User_CPU_s,Sys_CPU_s,Real_Time_s"
echo "==============================================="

# Display results if column command is available
if command -v column &> /dev/null; then
    echo ""
    echo "Summary of Results:"
    column -t -s',' "$OUT"
fi
