#!/usr/bin/env python3

"""
Part D Plotting Script
Generates comprehensive visualizations for process/thread scaling analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_scaling_analysis():
    """Generate plots from Part D scaling CSV data"""
    
    csv_file = "MT25058_Part_D_CSV.csv"
    
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found")
        return
    
    df = pd.read_csv(csv_file)
    
    # Convert Real_Time_s from string format (0:00.04) to float
    def time_to_seconds(time_str):
        if isinstance(time_str, str):
            parts = time_str.split(':')
            if len(parts) == 2:
                return float(parts[0]) * 60 + float(parts[1])
        return float(time_str)
    
    df['Real_Time_s'] = df['Real_Time_s'].apply(time_to_seconds)
    
    # Convert numeric strings if needed
    for col in ['CPU_Percent', 'Memory_MB', 'User_CPU_s', 'Sys_CPU_s']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Separate processes and threads data
    processes = df[df['Type'] == 'Process'].sort_values('Count')
    threads = df[df['Type'] == 'Thread'].sort_values('Count')
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Process and Thread Scaling Analysis (MT25058)', fontsize=16, fontweight='bold')
    
    # Plot 1: CPU Percentage
    ax = axes[0, 0]
    ax.plot(processes['Count'], processes['CPU_Percent'], marker='o', label='Processes', linewidth=2)
    ax.plot(threads['Count'], threads['CPU_Percent'], marker='s', label='Threads', linewidth=2)
    ax.set_xlabel('Number of Processes/Threads')
    ax.set_ylabel('CPU Usage (%)')
    ax.set_title('CPU Usage Scaling')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 2: Execution Time
    ax = axes[0, 1]
    ax.plot(processes['Count'], processes['Real_Time_s'], marker='o', label='Processes', linewidth=2)
    ax.plot(threads['Count'], threads['Real_Time_s'], marker='s', label='Threads', linewidth=2)
    ax.set_xlabel('Number of Processes/Threads')
    ax.set_ylabel('Execution Time (seconds)')
    ax.set_title('Execution Time Scaling')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Memory Usage
    ax = axes[1, 0]
    ax.plot(processes['Count'], processes['Memory_MB'], marker='o', label='Processes', linewidth=2)
    ax.plot(threads['Count'], threads['Memory_MB'], marker='s', label='Threads', linewidth=2)
    ax.set_xlabel('Number of Processes/Threads')
    ax.set_ylabel('Memory Usage (MB)')
    ax.set_title('Memory Usage Scaling')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 4: Total CPU Time (User + Sys)
    ax = axes[1, 1]
    processes['Total_CPU'] = processes['User_CPU_s'] + processes['Sys_CPU_s']
    threads['Total_CPU'] = threads['User_CPU_s'] + threads['Sys_CPU_s']
    ax.plot(processes['Count'], processes['Total_CPU'], marker='o', label='Processes', linewidth=2)
    ax.plot(threads['Count'], threads['Total_CPU'], marker='s', label='Threads', linewidth=2)
    ax.set_xlabel('Number of Processes/Threads')
    ax.set_ylabel('Total CPU Time (seconds)')
    ax.set_title('Total CPU Time Scaling')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('MT25058_Part_D_scaling_analysis.png', dpi=300, bbox_inches='tight')
    print("Saved: MT25058_Part_D_scaling_analysis.png")
    plt.close()
    
    # Generate individual comparative plots
    
    # Efficiency comparison
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Process vs Thread Efficiency Metrics', fontsize=14, fontweight='bold')
    
    # CPU efficiency (CPU% / count)
    ax = axes[0]
    processes['CPU_Efficiency'] = processes['CPU_Percent'] / processes['Count']
    threads['CPU_Efficiency'] = threads['CPU_Percent'] / threads['Count']
    ax.plot(processes['Count'], processes['CPU_Efficiency'], marker='o', label='Processes', linewidth=2)
    ax.plot(threads['Count'], threads['CPU_Efficiency'], marker='s', label='Threads', linewidth=2)
    ax.set_xlabel('Number of Processes/Threads')
    ax.set_ylabel('CPU Efficiency (% per unit)')
    ax.set_title('CPU Efficiency Comparison')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Time efficiency (Real_Time / count)
    ax = axes[1]
    processes['Time_Efficiency'] = processes['Real_Time_s'] / processes['Count']
    threads['Time_Efficiency'] = threads['Real_Time_s'] / threads['Count']
    ax.plot(processes['Count'], processes['Time_Efficiency'], marker='o', label='Processes', linewidth=2)
    ax.plot(threads['Count'], threads['Time_Efficiency'], marker='s', label='Threads', linewidth=2)
    ax.set_xlabel('Number of Processes/Threads')
    ax.set_ylabel('Time per unit (seconds)')
    ax.set_title('Time Efficiency Comparison')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('MT25058_Part_D_efficiency_metrics.png', dpi=300, bbox_inches='tight')
    print("Saved: MT25058_Part_D_efficiency_metrics.png")
    plt.close()

def plot_part_c_analysis():
    """Generate plots from Part C measurement data"""
    
    csv_file = "MT25058_Part_C_CSV.csv"
    
    if not os.path.exists(csv_file):
        print(f"Warning: {csv_file} not found, skipping Part C plots")
        return
    
    df = pd.read_csv(csv_file)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Part C: Program+Worker Combinations Analysis (MT25058)', fontsize=16, fontweight='bold')
    
    # Separate by program
    prog_a = df[df['Program'] == 'A']
    prog_b = df[df['Program'] == 'B']
    
    # Plot 1: CPU % comparison
    ax = axes[0, 0]
    workers = sorted(df['Worker'].unique())
    x = np.arange(len(workers))
    width = 0.35
    cpu_a = [prog_a[prog_a['Worker'] == w]['CPU_Percent'].values[0] if len(prog_a[prog_a['Worker'] == w]) > 0 else 0 for w in workers]
    cpu_b = [prog_b[prog_b['Worker'] == w]['CPU_Percent'].values[0] if len(prog_b[prog_b['Worker'] == w]) > 0 else 0 for w in workers]
    ax.bar(x - width/2, cpu_a, width, label='Program A (Processes)', alpha=0.8)
    ax.bar(x + width/2, cpu_b, width, label='Program B (Threads)', alpha=0.8)
    ax.set_ylabel('CPU Usage (%)')
    ax.set_title('CPU Usage by Worker Type')
    ax.set_xticks(x)
    ax.set_xticklabels(workers)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Plot 2: Memory usage comparison
    ax = axes[0, 1]
    mem_a = [prog_a[prog_a['Worker'] == w]['Memory_MB'].values[0] if len(prog_a[prog_a['Worker'] == w]) > 0 else 0 for w in workers]
    mem_b = [prog_b[prog_b['Worker'] == w]['Memory_MB'].values[0] if len(prog_b[prog_b['Worker'] == w]) > 0 else 0 for w in workers]
    ax.bar(x - width/2, mem_a, width, label='Program A (Processes)', alpha=0.8)
    ax.bar(x + width/2, mem_b, width, label='Program B (Threads)', alpha=0.8)
    ax.set_ylabel('Memory Usage (MB)')
    ax.set_title('Memory Usage by Worker Type')
    ax.set_xticks(x)
    ax.set_xticklabels(workers)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Plot 3: I/O throughput
    ax = axes[1, 0]
    io_a = [prog_a[prog_a['Worker'] == w]['IO_KB_s'].values[0] if len(prog_a[prog_a['Worker'] == w]) > 0 else 0 for w in workers]
    io_b = [prog_b[prog_b['Worker'] == w]['IO_KB_s'].values[0] if len(prog_b[prog_b['Worker'] == w]) > 0 else 0 for w in workers]
    ax.bar(x - width/2, io_a, width, label='Program A (Processes)', alpha=0.8)
    ax.bar(x + width/2, io_b, width, label='Program B (Threads)', alpha=0.8)
    ax.set_ylabel('I/O Throughput (KB/s)')
    ax.set_title('I/O Throughput by Worker Type')
    ax.set_xticks(x)
    ax.set_xticklabels(workers)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Plot 4: Execution time
    ax = axes[1, 1]
    time_a = [prog_a[prog_a['Worker'] == w]['Exec_Time_s'].values[0] if len(prog_a[prog_a['Worker'] == w]) > 0 else 0 for w in workers]
    time_b = [prog_b[prog_b['Worker'] == w]['Exec_Time_s'].values[0] if len(prog_b[prog_b['Worker'] == w]) > 0 else 0 for w in workers]
    ax.bar(x - width/2, time_a, width, label='Program A (Processes)', alpha=0.8)
    ax.bar(x + width/2, time_b, width, label='Program B (Threads)', alpha=0.8)
    ax.set_ylabel('Execution Time (seconds)')
    ax.set_title('Execution Time by Worker Type')
    ax.set_xticks(x)
    ax.set_xticklabels(workers)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('MT25058_Part_C_analysis.png', dpi=300, bbox_inches='tight')
    print("Saved: MT25058_Part_C_analysis.png")
    plt.close()

if __name__ == "__main__":
    print("Generating plots for Part D scaling analysis...")
    plot_scaling_analysis()
    
    print("\nGenerating plots for Part C analysis...")
    plot_part_c_analysis()
    
    print("\nAll plots generated successfully!")
