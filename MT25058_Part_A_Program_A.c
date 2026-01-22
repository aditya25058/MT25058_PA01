#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <string.h>
#include "MT25058_Part_B_workers.h"

/*
 * Program A: Creates N child processes using fork()
 * Roll Number: MT25058
 * Usage: ./program_A <cpu|mem|io> <num_processes>
 * 
 * Creates N child processes (excluding parent process) and each executes
 * the specified worker function.
 */

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s <cpu|mem|io> <num_processes>\n", argv[0]);
        exit(1);
    }

    int n = atoi(argv[2]);
    if (n <= 0) {
        printf("Number of processes must be > 0\n");
        exit(1);
    }

    printf("[Program A] Creating %d child processes with %s worker\n", n, argv[1]);

    // Create N child processes
    for (int i = 0; i < n; i++) {
        pid_t pid = fork();

        if (pid == 0) {
            // Child process
            if (strcmp(argv[1], "cpu") == 0)
                cpu_worker();
            else if (strcmp(argv[1], "mem") == 0)
                mem_worker();
            else if (strcmp(argv[1], "io") == 0)
                io_worker();
            exit(0);
        } else if (pid < 0) {
            perror("fork failed");
            exit(1);
        }
    }

    // Parent process waits for all children
    for (int i = 0; i < n; i++)
        wait(NULL);

    printf("[Program A] All child processes completed\n");
    return 0;
}

