#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include "MT25058_Part_B_workers.h"

/*
 * Worker Functions: cpu_worker, mem_worker, io_worker
 * Roll Number: MT25058 (Last digit: 8)
 * Loop Count: 8 × 10^3 = 8000
 * 
 * These functions represent different types of workloads:
 * - CPU-intensive: Performs heavy mathematical calculations
 * - Memory-intensive: Allocates and processes large amounts of memory
 * - I/O-intensive: Performs extensive disk read/write operations
 */

/*
 * cpu_worker: CPU-intensive workload
 * 
 * Description: Performs complex mathematical calculations (square root).
 * This workload keeps the CPU busy with computation rather than waiting
 * for external resources like memory or disk I/O.
 * 
 * Examples of CPU-intensive work: Video encoding, mathematical simulations,
 * data compression algorithms.
 */
void cpu_worker() {
    printf("[CPU Worker] Starting CPU-intensive work (8000 iterations)\n");
    
    volatile double x = 0.0;
    
    // LOOP_COUNT = 8000, each iteration performs 1000 sqrt operations
    for (int i = 0; i < LOOP_COUNT; i++) {
        for (int j = 0; j < 1000; j++) {
            x += sqrt((double)(i * j + 1));
        }
    }
    
    printf("[CPU Worker] Completed CPU-intensive work\n");
}

/*
 * mem_worker: Memory-intensive workload
 * 
 * Description: Allocates large memory and performs repeated access patterns.
 * This workload stresses the memory subsystem by processing data that
 * exceeds CPU cache capacity, forcing memory bus traffic.
 * 
 * Examples of memory-intensive work: Large dataset sorting, in-memory
 * databases, image processing with large buffers.
 */
void mem_worker() {
    printf("[Memory Worker] Starting memory-intensive work\n");
    
    // Allocate 8000 * 100 = 800,000 integers (~3.2 MB)
    int size = LOOP_COUNT * 100;
    int *arr = (int*)malloc(size * sizeof(int));
    
    if (arr == NULL) {
        fprintf(stderr, "[Memory Worker] Failed to allocate memory\n");
        return;
    }

    // Initialize array
    for (int i = 0; i < size; i++) {
        arr[i] = i;
    }

    // Process array multiple times
    for (int i = 0; i < size; i++) {
        arr[i] += 1;
    }

    // Clean up
    free(arr);
    
    printf("[Memory Worker] Completed memory-intensive work\n");
}

/*
 * io_worker: I/O-intensive workload
 * 
 * Description: Performs extensive file write operations.
 * This workload causes the process to wait for disk I/O completion,
 * during which the CPU is mostly idle.
 * 
 * Examples of I/O-intensive work: File operations, database queries,
 * network requests, user-interactive programs.
 */
void io_worker() {
    printf("[IO Worker] Starting I/O-intensive work\n");
    
    int fd;
    char buf[1024];
    memset(buf, 'A', sizeof(buf));

    // Open file for writing (create if doesn't exist)
    fd = open("io_test_file.txt", O_CREAT | O_WRONLY | O_TRUNC, 0644);
    if (fd < 0) {
        perror("[IO Worker] open failed");
        return;
    }

    // Write data to file 8000 times (1024 bytes per write = 8 MB total)
    for (int i = 0; i < LOOP_COUNT; i++) {
        ssize_t written = write(fd, buf, sizeof(buf));
        if (written < 0) {
            perror("[IO Worker] write failed");
            break;
        }
    }

    close(fd);
    
    printf("[IO Worker] Completed I/O-intensive work\n");
}
