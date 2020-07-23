"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0, 0, 0, 0, 0, 0, 0, 0xF4]
        self.pc = 0
        self.running = False
        self.sp = 7
        self.branch_table = {
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100010: self.MUL,
            0b10100000: self.ADD,
            0b01000101: self.PUSH,
            0b01000110: self.POP,
            0b01010000: self.CALL,
            0b00010001: self.RET,
            0b00000001: self.HLT
        }

    def load(self):
        """Load a program into memory."""

        address = 0

        with open(sys.argv[1], 'r') as f:
            for current_line in f:
                if current_line == "\n" or current_line[0] == "#":
                    continue
                else:
                    self.ram[address] = int(current_line.split()[0], 2)

                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
            self.pc += 3
        elif op == "MUL":
            self.registers[self.ram[reg_a]] *= self.registers[self.ram[reg_b]]
            self.pc += 3
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.registers[i], end='')

        print()

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def HLT(self):
        self.running = False

    def LDI(self):
        reg = self.ram_read(self.pc+1)
        val = self.ram_read(self.pc+2)
        self.registers[reg] = val
        self.pc += 3

    def PRN(self):
        reg = self.ram_read(self.pc+1)
        print(self.registers[reg])
        self.pc += 2

    def ADD(self):
        self.alu("ADD", self.ram[self.pc+1], self.ram[self.pc+2])

    def MUL(self):
        self.alu("MUL", self.pc+1, self.pc+2)

    def PUSH(self):
        self.registers[self.sp] -= 1
        reg_number = self.ram[self.pc+1]
        value = self.registers[reg_number]
        self.ram[self.registers[self.sp]] = value
        self.pc += 2

    def POP(self):
        address = self.registers[self.sp]
        value = self.ram[address]
        self.registers[self.ram[self.pc+1]] = value
        self.registers[self.sp] += 1
        self.pc += 2

    def CALL(self):
        reg = self.ram[self.pc+1]
        address = self.registers[reg]

        return_address = self.pc + 2

        self.registers[7] -= 1
        sp = self.registers[7]

        self.ram[sp] = return_address

        self.pc = address

    def RET(self):
        sp = self.registers[7]
        return_address = self.ram[sp]
        self.registers[7] += 1

        self.pc = return_address

    def run(self):
        """Run the CPU."""
        self.running = True
        while self.running:
            ir = self.ram_read(self.pc)
            if ir in self.branch_table:
                self.branch_table[ir]()
                
            # for instruction in self.ram:
            #     if instruction in self.branch_table:
            #         self.branch_table[instruction]()
