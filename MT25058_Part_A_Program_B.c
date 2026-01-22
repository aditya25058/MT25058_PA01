#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include "MT25058_Part_B_workers.h"

/*
 * Program B: Creates N threads using pthread library
 * Roll Number: MT25058
 * Usage: ./program_B <cpu|mem|io> <num_threads>
 * 
 * Creates N threads (excluding main thread) and each executes
 * the specified worker function.
 */

void* thread_runner(void* arg) {
    char* type = (char*)arg;

    if (strcmp(type, "cpu") == 0)
        cpu_worker();
    else if (strcmp(type, "mem") == 0)
        mem_worker();
    else if (strcmp(type, "io") == 0)
        io_worker();

    pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s <cpu|mem|io> <num_threads>\n", argv[0]);
        exit(1);
    }

    int n = atoi(argv[2]);
    if (n <= 0) {
        printf("Number of threads must be > 0\n");
        exit(1);
    }

    printf("[Program B] Creating %d threads with %s worker\n", n, argv[1]);

    pthread_t threads[n];

    // Create N threads
    for (int i = 0; i < n; i++) {
        if (pthread_create(&threads[i], NULL, thread_runner, argv[1]) != 0) {
            perror("pthread_create failed");
            exit(1);
        }
    }

    // Wait for all threads to complete
    for (int i = 0; i < n; i++) {
        if (pthread_join(threads[i], NULL) != 0) {
            perror("pthread_join failed");
            exit(1);
        }
    }

    printf("[Program B] All threads completed\n");
    return 0;
}
