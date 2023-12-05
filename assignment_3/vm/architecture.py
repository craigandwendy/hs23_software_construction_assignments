NUM_REG = 4  # number of registers
RAM_LEN = 256  # number of words in RAM

OPS = {
    "hlt": {"code": 0x1, "fmt": "--"},  # Halt program -> sys.exit(0)
    "ldc": {"code": 0x2, "fmt": "rv"},  # Load value -> R0 = 99
    "ldr": {"code": 0x3, "fmt": "rr"},  # Load register -> R0 = memory[R1]
    "cpy": {"code": 0x4, "fmt": "rr"},  # Copy register -> R0 = R1
    "str": {"code": 0x5, "fmt": "rr"},  # Store register -> memory[R1] = R0
    "add": {"code": 0x6, "fmt": "rr"},  # Add -> R0 = R0 + R1
    "sub": {"code": 0x7, "fmt": "rr"},  # Subtract -> R0 = R0 - R1
    "beq": {"code": 0x8, "fmt": "rv"},  # Branch if equal -> if (R0 == 0) goto line
    "bne": {"code": 0x9, "fmt": "rv"},  # Branch if not equal -> if (R0 != 0) goto line
    "prr": {"code": 0xA, "fmt": "r-"},  # Print register -> print(R0)
    "prm": {"code": 0xB, "fmt": "r-"},  # Print memory -> print(memory[R0])
    "inc": {"code": 0xC, "fmt": "r-"},  # Increase value at register by 1 R0 = R0 + 1
    "dec": {"code": 0xD, "fmt": "r-"},  # Decrease value at register by 1 R0 = R0 - 1
    "swp": {"code": 0xE, "fmt": "rr"},  # swap two registers R0 = R1 && R1 = R0
    "bge": {"code": 0xF, "fmt": "rv"}   # Branch if greater equal 0 -> if (R0 >= 0) go to line -> used for task 3_3
}

OP_MASK = 0xFF  # select a single byte
OP_SHIFT = 8  # shift up by one byte
OP_WIDTH = 6  # op width in characters when printing
