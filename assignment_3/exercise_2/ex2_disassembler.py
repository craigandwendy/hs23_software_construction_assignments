import sys
from ex2_architecture import NUM_REG, OP_SHIFT, OPS, RAM_LEN

# [class]
class Disassembler:
    def disassemble(self, lines):
        lines = self._get_lines(lines)  # cleaned up lines

        instructions = self._to_text(lines)  # convert to decimal format e.g.: ["03 00 02", "05 01 02", "00 00 01"]

        program = [self._compile(ln) for ln in instructions]

        return program
# [/class]


    # [compile]
    def _compile(self, instruction):
        # instruction = "00 01 11" -> in assembler: instruction = "ldc R0 1"
        tokens = instruction.split()
        # tokens = ["01", "01", "11"] (reverse format as assembler) -> in assembler: tokens = ["ldc", "R0", "1"]
        tokens = tokens[::-1]  # ["11", "01", "01"] same format as in assembler
        # change OPS to {"01": {"original_key": "hlt", "fmt": "--"}, "02": ...}
        reversed_ops = {f"{value['code']:02d}": {"original_key": key, **{k: v for k, v in value.items() if k != "code"}} for key, value in OPS.items()}
        # get op from reversed_ops -> .mx instruction "01" == .as instruction "hlt"
        op, args = reversed_ops[tokens[0]]["original_key"], tokens[1:]  # op = "hlt"
        # op, args = operations_helper[tokens[0]], tokens[1:]  # e.g.: op = "hlt", tokens = ["01", "01"]
        fmt, code = OPS[op]["fmt"], OPS[op]["code"]

        if fmt == "--":
            return op

        elif fmt == "r-":
            return f"{op} R{int(args[0])}"

        elif fmt == "rr":
            return f"{op} R{int(args[0])} R{int(args[1])}"
        elif fmt == "rv":
            return f"{op} R{int(args[0])} {int(args[1])}"
    # [/compile]

    def _to_text(self, program):
        #return [f"{op:06x}" for op in program]
        temp = []
        for lines in program:
            arg_2 = int(f"{lines[0:2]}", 16)  # can be v or r or empty
            arg_1 = int(f"{lines[2:4]}", 16)  # can be r or empty
            op_ = int(f"{lines[4:6]}", 16)  # must be element from OPS
            temp.append(f"{arg_2:02d} "+f"{arg_1:02d} "+f"{op_:02d}")
        return temp
        # return [f"{op:06d}" for op in program]

    def _get_lines(self, lines):
        lines = [ln.strip() for ln in lines]  # remove \n
        lines = [ln for ln in lines if len(ln) > 0]  # remove empty line
        # lines = [ln for ln in lines if not self._is_comment(ln)]  # remove #-line (comment lines)
        return lines


def main(disassembler_cls):
    assert len(sys.argv) == 3, f"Usage: {sys.argv[0]} input|- output|-"
    reader = open(sys.argv[1], "r") if (sys.argv[1] != "-") else sys.stdin
    writer = open(sys.argv[2], "w") if (sys.argv[2] != "-") else sys.stdout
    lines = reader.readlines()
    disassembler = disassembler_cls()
    program = disassembler.disassemble(lines)  # list (lines) of instructions from .as file in hexadecimal format
    for instruction in program:
        print(instruction, file=writer)  # write hexadecimal lines to .mx files -> will be processed by vm


# [main]
if __name__ == "__main__":
    # main(DataAllocator)
    main(Disassembler)
# [/main]
