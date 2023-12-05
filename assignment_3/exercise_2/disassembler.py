import sys
from architecture import NUM_REG, OP_SHIFT, OPS, RAM_LEN

# [class]
class Disassembler:
    def disassemble(self, lines):
        lines = self._get_lines(lines)
        instructions = self._to_text(lines)   # convert hexadecimal lines to text
        program = []
        
        # Process each instruction individually and handle errors
        for instruction in instructions:
            try:
                compiled_instruction = self._compile(instruction)
                program.append(compiled_instruction)
            except Exception as e:
                print(f"Error processing instruction '{instruction}': {e}", file=sys.stderr)

        return program

    # [compile]
    def _compile(self, instruction):
        # instruction = "00 01 11" -> in assembler: instruction = "ldc R0 1"
        tokens = instruction.split()
        # tokens = ["01", "01", "11"] (reverse format as assembler) -> in assembler: tokens = ["ldc", "R0", "1"]
        tokens = tokens[::-1]
        # create inverse mapping for operations
        reversed_ops = {value['code']: key for key, value in OPS.items()}
        # extract the operation code (raise error in case it doesn't exist in reversed_ops)
        op_code = int(tokens[0])
        if op_code not in reversed_ops:
            raise ValueError(f"Unknown operation code {op_code}")
        # get name and format of the operation 
        op = reversed_ops[op_code]
        fmt = OPS[op]["fmt"]

        if fmt == "--":
            return op
        elif fmt == "r-":
            return f"{op} R{int(tokens[1])}"
        elif fmt == "rr":
            # format as "op Rarg0 Rarg1"
            return f"{op} R{int(tokens[1])} R{int(tokens[2])}"
        elif fmt == "rv":
            # format as "op Rarg0 value"
            return f"{op} R{int(tokens[1])} {int(tokens[2])}"

        raise ValueError(f"Unhandled instruction format: {fmt}")
    # [/compile]
    
    # Function for converting a list of hexadecimal instructions to text format
    def _to_text(self, program):
        # Splits each line in 3 parts
        return [f"{int(line[0:2], 16):02d} {int(line[2:4], 16):02d} {int(line[4:6], 16):02d}" for line in program]

    # Function for preparing the input lines (ignores empty lines and comments)
    def _get_lines(self, lines):
        return [line.strip() for line in lines if line.strip() and not line.startswith('#')]

# [/class] 

def main(disassembler_cls):
    assert len(sys.argv) == 3, f"Usage: {sys.argv[0]} input|- output|-"
    reader = open(sys.argv[1], "r") if (sys.argv[1] != "-") else sys.stdin
    writer = open(sys.argv[2], "w") if (sys.argv[2] != "-") else sys.stdout
    lines = reader.readlines()
    disassembler = disassembler_cls()
    program = disassembler.disassemble(lines)
    for instruction in program:
        print(instruction, file=writer)

# [main]
if __name__ == "__main__":
    # main(DataAllocator)
    main(Disassembler)
# [/main]
