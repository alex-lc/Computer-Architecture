PRINT_ALEX = 0b01
HALT = 0b10  # 2
PRINT_NUM = 0b11  # opcode 3
SAVE = 0b100 # opcode 4
PRINT_REG = 0b101 # opcode 5

# save the number 99 into R2
# print whatever is inside R2

memory = [
    PRINT_ALEX,
    PRINT_ALEX,
    PRINT_NUM,
    42,
    SAVE,
    2, # register to put it in
    99, # number to save
    PRINT_REG,
    2,
    HALT
]

# write a program to pull each command out of memory and execute

# we can loop over it

# register aka memory
registers = [0] * 8
# [0, 0, 99, 0, 0, 0, 0, 0]
# save the number 99 into R2
# R0-R7

pc = 0  # program counter
running = True
while running:
    command = memory[pc]

    if command == PRINT_ALEX:
        print("Alex!")

    if command == PRINT_NUM:
        num_to_print = memory[pc+1]
        print(num_to_print)

        pc += 1

    if command == SAVE:
        reg = memory[pc+1]
        num_to_save = memory[pc+2]
        registers[reg] = num_to_save

        pc += 2

    if command == PRINT_REG:
        reg_index = memory[pc+1]

        print(registers[reg_index])

        pc += 1

    if command == HALT:
        running = False

    pc += 1
