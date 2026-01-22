#ifndef WORKERS_H
#define WORKERS_H

/*
 * Worker Functions Header
 * Roll Number: MT25058
 * 
 * Defines three worker function types for different workload characteristics:
 * - CPU-intensive
 * - Memory-intensive
 * - I/O-intensive
 */

#define LOOP_COUNT 8000   // Last digit of roll number (8) × 10^3

/**
 * CPU-intensive worker function
 * Performs heavy mathematical computations
 */
void cpu_worker();

/**
 * Memory-intensive worker function
 * Performs large memory allocations and accesses
 */
void mem_worker();

/**
 * I/O-intensive worker function
 * Performs extensive file I/O operations
 */
void io_worker();

#endif

