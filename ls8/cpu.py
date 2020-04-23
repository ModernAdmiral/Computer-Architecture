"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101
SP = 0b00000111


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.register[SP] = 0xF4
        # self.running = False

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        print(sys.argv[1])
        with open(sys.argv[1]) as file:
            for line in file:
                line = line.split("#")[0].strip()
                if line == "":
                    continue
                instruction = int(line, 2)
                self.ram[address] = instruction
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == "MUL":
            self.ram[reg_a] *= self.ram[reg_b]
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

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if IR == LDI:
                self.ram_write(operand_a, operand_b)
                # self.register[operand_a] = operand_b
                self.pc += 3

            elif IR == PRN:
                # print
                print(self.ram_read(operand_a))
                self.pc += 2
                # increment the PC by 2 to skip the argument
            elif IR == MUL:
                # call alu passing in params not sure if correct cuz registers not ram
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            elif IR == HLT:
                running = False
            elif IR == PUSH:
                # Decrement the 'SP'
                value = self.register[operand_a]
                self.register[SP] -= 1
                # Copy the value in the given register to the address pointed to by SP
                self.ram_write(self.register[SP], value)

            elif IR == POP:
                # Copy the value from the address pointed to by `SP` to the given register.
                last_val = self.ram_read(
                    self.register[SP])  # last value in stack
                # put that in the register at operan_a
                self.register[operand_a] = last_val
                # Increment SP
                self.register[SP] += 1
            else:
                print("unknown instruction")
                running = False
