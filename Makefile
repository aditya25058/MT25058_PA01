# Makefile for MT25058_PA01: Processes and Threads
# Graduate Systems - CSE638

CC = gcc
CFLAGS = -Wall -Wextra -pthread -O2 -std=c99
LDFLAGS = -lm -lpthread

# Source files
WORKERS_SRC = MT25058_Part_B_workers.c
PROG_A_SRC = MT25058_Part_A_Program_A.c
PROG_B_SRC = MT25058_Part_A_Program_B.c

# Object files
WORKERS_OBJ = MT25058_Part_B_workers.o
PROG_A_OBJ = MT25058_Part_A_Program_A.o
PROG_B_OBJ = MT25058_Part_A_Program_B.o

# Executables
PROG_A = program_A
PROG_B = program_B

# Default target
all: $(PROG_A) $(PROG_B)

# Compile worker functions
$(WORKERS_OBJ): $(WORKERS_SRC) MT25058_Part_B_workers.h
	$(CC) $(CFLAGS) -c $(WORKERS_SRC) -o $(WORKERS_OBJ)

# Program A: Processes
$(PROG_A_OBJ): $(PROG_A_SRC) MT25058_Part_B_workers.h
	$(CC) $(CFLAGS) -c $(PROG_A_SRC) -o $(PROG_A_OBJ)

$(PROG_A): $(PROG_A_OBJ) $(WORKERS_OBJ)
	$(CC) $(CFLAGS) $(PROG_A_OBJ) $(WORKERS_OBJ) -o $(PROG_A) $(LDFLAGS)
	@echo "[Build] Created executable: $(PROG_A)"

# Program B: Threads
$(PROG_B_OBJ): $(PROG_B_SRC) MT25058_Part_B_workers.h
	$(CC) $(CFLAGS) -c $(PROG_B_SRC) -o $(PROG_B_OBJ)

$(PROG_B): $(PROG_B_OBJ) $(WORKERS_OBJ)
	$(CC) $(CFLAGS) $(PROG_B_OBJ) $(WORKERS_OBJ) -o $(PROG_B) $(LDFLAGS)
	@echo "[Build] Created executable: $(PROG_B)"

# Clean up object files and executables (but not data)
clean:
	rm -f $(PROG_A) $(PROG_B) $(WORKERS_OBJ) $(PROG_A_OBJ) $(PROG_B_OBJ)
	rm -f io_test_file.txt
	@echo "[Clean] Cleaned up build artifacts"

# Run all tests
test: all
	@echo "Testing Program A..."
	./$(PROG_A) cpu 2
	@echo "Testing Program B..."
	./$(PROG_B) cpu 2

.PHONY: all clean test
