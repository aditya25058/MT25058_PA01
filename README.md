# MT25058_PA01: Processes and Threads

**Graduate Systems (CSE638) - PA01**
**Roll Number: MT25058**
**Deadline: January 23, 2026**

## Overview

This assignment implements comprehensive measurements and analysis of processes and threads in C, along with performance metrics collection and visualization.

## Project Structure

```
MT25058_PA01/
├── README.md                            # This file
├── makefile                             # Compilation instructions
├── MT25058_Part_A_Program_A.c           # Part A: Process creation using fork()
├── MT25058_Part_A_Program_B.c           # Part A: Thread creation using pthread
├── MT25058_Part_B_workers.h             # Part B: Worker function declarations
├── MT25058_Part_B_workers.c             # Part B: Worker function implementations
├── MT25058_Part_C_shell.sh              # Part C: Measurement collection script
├── MT25058_Part_C_CSV.csv               # Part C: Raw measurement data
├── MT25058_Part_C_analysis.png          # Part C: Analysis plots
├── MT25058_Part_D_shell.sh              # Part D: Scaling analysis script
├── MT25058_Part_D_CSV.csv               # Part D: Scaling measurement data
├── MT25058_Part_D_plot.py               # Part D: Plotting script
├── MT25058_Part_D_scaling_analysis.png  # Part D: Scaling plots
├── MT25058_Part_D_efficiency_metrics.png # Part D: Efficiency comparison plots
└── MT25058_Report.pdf                   # Final report with analysis and conclusions
```

## Part A: Process and Thread Programs

### Program A (Processes)
**File**: `MT25058_Part_A_Program_A.c`

Creates N child processes using `fork()` and executes specified worker functions in parallel.

**Usage**:
```bash
./program_A <cpu|mem|io> <num_processes>
```

**Example**:
```bash
./program_A cpu 2          # Create 2 child processes running CPU worker
./program_A mem 3          # Create 3 child processes running memory worker
./program_A io 4           # Create 4 child processes running I/O worker
```

### Program B (Threads)
**File**: `MT25058_Part_A_Program_B.c`

Creates N threads using POSIX pthread library and executes specified worker functions concurrently.

**Usage**:
```bash
./program_B <cpu|mem|io> <num_threads>
```

**Example**:
```bash
./program_B cpu 2          # Create 2 threads running CPU worker
./program_B mem 4          # Create 4 threads running memory worker
./program_B io 8           # Create 8 threads running I/O worker
```

## Part B: Worker Functions

**File**: `MT25058_Part_B_workers.c` and `MT25058_Part_B_workers.h`

Implements three worker functions with different workload characteristics:

### 1. CPU-Intensive Worker (`cpu_worker()`)

**Characteristics**:
- Performs heavy mathematical computations (square root operations)
- Keeps CPU busy with continuous computation
- Loop count: 8000 iterations (8 × 10³, where 8 is the last digit of roll number MT25058)
- Each iteration performs 1000 sqrt operations

**Real-world examples**:
- Video encoding
- Scientific simulations
- Complex mathematical calculations
- Data compression algorithms

**Expected behavior**:
- High CPU% usage
- Low memory footprint
- Minimal I/O operations

### 2. Memory-Intensive Worker (`mem_worker()`)

**Characteristics**:
- Allocates large memory blocks (800,000 integers ≈ 3.2 MB)
- Performs repeated memory access patterns
- Stresses memory subsystem and cache hierarchy
- Loop count: 8000 iterations

**Real-world examples**:
- Large dataset sorting
- In-memory databases
- Image processing with large buffers
- Scientific data analysis

**Expected behavior**:
- Medium CPU% usage
- Higher memory footprint
- Minimal I/O operations

### 3. I/O-Intensive Worker (`io_worker()`)

**Characteristics**:
- Performs extensive file write operations (8 MB total)
- Causes CPU to wait for disk I/O completion
- CPU largely idle during disk operations
- Loop count: 8000 iterations with 1024-byte writes

**Real-world examples**:
- File operations
- Database queries
- Network requests
- User-interactive programs

**Expected behavior**:
- Lower CPU% usage (due to I/O wait)
- Lower memory footprint
- High I/O activity

## Part C: Program and Worker Combination Measurements

### Script: `MT25058_Part_C_shell.sh`

Collects performance metrics for all 6 combinations:
- Program A (Processes) + CPU worker
- Program A (Processes) + Memory worker
- Program A (Processes) + I/O worker
- Program B (Threads) + CPU worker
- Program B (Threads) + Memory worker
- Program B (Threads) + I/O worker

**Metrics Collected**:
- **CPU_Percent**: Percentage of CPU time used by the program
- **Memory_MB**: Maximum resident set size in megabytes
- **IO_KB_s**: I/O disk statistics (KB/s)
- **Exec_Time_s**: Total execution time in seconds

**Usage**:
```bash
chmod +x MT25058_Part_C_shell.sh
./MT25058_Part_C_shell.sh
```

**Output**: `MT25058_Part_C_CSV.csv`

### Data Format

```csv
Program,Worker,CPU_Percent,Memory_MB,IO_KB_s,Exec_Time_s
A,cpu,166,1.87,0,.0476
B,cpu,161,2.12,0,.0477
...
```

### Analysis Output

Generates visualization plot: `MT25058_Part_C_analysis.png`

## Part D: Scaling Analysis

### Scripts

1. **`MT25058_Part_D_shell.sh`**: Collects scaling metrics
2. **`MT25058_Part_D_plot.py`**: Generates analysis plots

### Scaling Tests

**Program A (Processes)**: Tests with 2, 3, 4, 5 child processes
**Program B (Threads)**: Tests with 2, 3, 4, 5, 6, 7, 8 threads

Both use CPU worker for consistent comparison.

**Metrics Collected**:
- CPU_Percent
- Memory_MB
- User_CPU_s (user-mode CPU time)
- Sys_CPU_s (system-mode CPU time)
- Real_Time_s (wall clock time)

**Usage**:
```bash
chmod +x MT25058_Part_D_shell.sh
./MT25058_Part_D_shell.sh

# Generate plots
python3 MT25058_Part_D_plot.py
```

**Output Files**:
- `MT25058_Part_D_CSV.csv`: Raw scaling data
- `MT25058_Part_D_scaling_analysis.png`: Scaling metrics plots
- `MT25058_Part_D_efficiency_metrics.png`: Efficiency comparison plots

## Compilation

### Prerequisites
- GCC compiler
- POSIX-compliant Unix/Linux system (tested on WSL Ubuntu)
- Standard C libraries

### Build Instructions

```bash
# Clean previous builds
make clean

# Compile all programs
make

# Run tests
make test
```

### Generated Executables
- `program_A`: Process-based executable
- `program_B`: Thread-based executable

## Measurement Methodology

### Tools and Techniques

1. **Time Measurement**:
   - Using GNU `time -v` command
   - Captures: CPU%, Memory, User/System time, Wall-clock time

2. **CPU Affinity** (optional):
   - Uses `taskset` to pin processes to specific CPU cores
   - Ensures reproducible measurements

3. **I/O Monitoring**:
   - Collects from `/proc/diskstats`
   - Measures disk read/write activity

### Accuracy Considerations

- Multiple runs with sleep delays between them
- Metrics are system-reported via `/usr/bin/time -v`
- Processes run with 2 instances for baseline comparison

## Key Observations

### Part C Analysis

1. **CPU Worker**:
   - Processes (Program A): ~166% CPU, ~1.87 MB memory
   - Threads (Program B): ~161% CPU, ~2.12 MB memory
   - Threads show slightly better CPU efficiency
   - Both achieve >160% due to 2 workers and context switching

2. **Memory Worker**:
   - Processes: ~100% CPU, ~3.62 MB memory
   - Threads: ~108% CPU, ~7.62 MB memory
   - Threads use more memory (shared data structures)
   - Memory-bound workload shows balanced performance

3. **I/O Worker**:
   - Processes: ~19% CPU, ~1.75 MB memory, ~2.2s execution
   - Threads: ~19% CPU, ~2.25 MB memory, ~2.3s execution
   - Low CPU% due to I/O wait
   - Execution time dominated by disk operations

### Part D Scaling Analysis

1. **Process Scaling (CPU Worker)**:
   - CPU% increases with process count (167% → 385% for 2→5 processes)
   - Linear scaling observed
   - Memory relatively constant (~1.87 MB)
   - User CPU time increases linearly

2. **Thread Scaling (CPU Worker)**:
   - CPU% increases with thread count (158% → 512% for 2→8 threads)
   - Better scalability than processes
   - Memory increases slightly with threads
   - More efficient context switching overhead

3. **Efficiency Metrics**:
   - Threads show better CPU efficiency per unit at higher counts
   - Processes maintain more stable memory footprint
   - Threads benefit from shared memory access patterns

## AI Usage Declaration

**AI-Generated Components**:
1. Plot generation code structure (matplotlib usage patterns)
2. Shell script metric extraction functions
3. Time conversion and data parsing logic

**Human Implementation**:
1. All core C programs and logic
2. Worker function implementations
3. Measurement script design and integration
4. Data analysis and interpretation
5. Documentation and report writing

## Compilation and Execution Details

### System Requirements
- Linux/WSL environment
- GNU C compiler (gcc)
- Bash shell
- Python 3 with pandas and matplotlib libraries

### Environment Setup (WSL)

```bash
# Install dependencies
sudo apt-get update
sudo apt-get install build-essential python3-dev

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install pandas matplotlib
```

### Clean Build

```bash
make clean
make
```

## Testing

### Quick Test

```bash
# Test Program A with CPU worker
./program_A cpu 2

# Test Program B with CPU worker
./program_B cpu 2

# Test Program A with memory worker
./program_A mem 3

# Test Program B with I/O worker
./program_B io 4
```

### Full Measurement Suite

```bash
# Run Part C measurements
./MT25058_Part_C_shell.sh

# Run Part D scaling analysis
./MT25058_Part_D_shell.sh

# Generate plots
python3 MT25058_Part_D_plot.py
```

## Output Files

### CSV Data Files
- `MT25058_Part_C_CSV.csv`: Part C measurements (6 combinations)
- `MT25058_Part_D_CSV.csv`: Part D scaling data (11 measurements)

### Visualization Files
- `MT25058_Part_C_analysis.png`: Bar charts comparing program+worker combinations
- `MT25058_Part_D_scaling_analysis.png`: Line plots showing scaling trends
- `MT25058_Part_D_efficiency_metrics.png`: Efficiency comparison plots

## Report

**File**: `MT25058_Report.pdf`

Includes:
- Screenshots of measurements and plots
- Detailed analysis of observations
- Comparison of process vs. thread performance
- Scaling analysis discussion
- AI usage declaration
- GitHub repository URL

## GitHub Repository

**URL**: https://github.com/aditya25058/MT25058_PA01

Structure:
```
GRS_PA01/
├── MT25058_Part_A_Program_A.c
├── MT25058_Part_A_Program_B.c
├── MT25058_Part_B_workers.c
├── MT25058_Part_B_workers.h
├── MT25058_Part_C_shell.sh
├── MT25058_Part_C_CSV.csv
├── MT25058_Part_D_shell.sh
├── MT25058_Part_D_CSV.csv
├── MT25058_Part_D_plot.py
├── MT25058_Part_C_analysis.png
├── MT25058_Part_D_scaling_analysis.png
├── MT25058_Part_D_efficiency_metrics.png
├── makefile
└── README.md
```

## Cleanup

```bash
# Remove build artifacts and temporary files
make clean

# Remove Python virtual environment (if created)
rm -rf venv

# Remove measurement CSVs (to re-run measurements)
rm -f MT25058_Part_C_CSV.csv MT25058_Part_D_CSV.csv

# Remove all generated plots
rm -f *.png
```

## Notes

1. **Portability**: The code is designed for Unix/Linux systems with POSIX compliance
2. **Performance**: On multi-core systems, process/thread count should match or exceed available cores for meaningful scaling analysis
3. **I/O**: The I/O worker creates temporary files; ensure write permissions in the working directory
4. **Repeatability**: Results may vary slightly between runs due to system load; multiple measurements recommended for statistical significance

## Contact

**Roll Number**: MT25058
**Course**: Graduate Systems (CSE638)
**Assignment**: PA01: Processes and Threads
**Submitted**: January 2026

---

**Note**: This assignment demonstrates understanding of:
- Process creation and management using fork()
- Thread creation and synchronization using pthreads
- Workload characterization and performance measurement
- System resource utilization analysis
- Performance scaling analysis and benchmarking
- Data analysis and visualization techniques
