"""CPU functionality."""

import sys

# opcodes
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.pc = 0
        self.running = False

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            LDI,  # LDI R0,8
            0b00000000,
            0b00001000,
            PRN,  # PRN R0
            0b00000000,
            HLT   # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
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
            print(" %02X" % self.reg[i], end='')

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

    def PRN(self):
        reg = self.ram_read(self.pc+1)
        print(self.registers[reg])

    def run(self):
        """Run the CPU."""
        self.running = True
        while self.running:
            print('Program starting...')
            for instruction in self.ram:

                if instruction == LDI:
                    print('Setting register value...')
                    self.LDI()

                if instruction == HLT:
                    print('Running HLT and stopping program...')
                    self.HLT()

                if instruction == PRN:
                    self.PRN()
