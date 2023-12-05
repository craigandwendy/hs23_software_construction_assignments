import sys
from ex2_architecture import NUM_REG, OP_SHIFT, OPS, RAM_LEN

# [class]
class Assembler:
    def assemble(self, lines):
        lines = self._get_lines(lines)  # cleaned up lines including labels
        labels = self._find_labels(lines)  # example: {"loop": 2}
        instructions = [
            ln for ln in lines if not self._is_label(ln)  # removing labels
        ]
        compiled = [
            self._compile(instr, labels) for instr in instructions
        ]
        program = self._to_text(compiled)  # create hexadecimal
        return program
# [/class]

    # [labels]
    def _find_labels(self, lines):
        result = {}
        loc = 0
        for ln in lines:
            if self._is_label(ln):
                label = ln[:-1].strip()
                assert label not in result, f"Duplicated {label}"
                result[label] = loc
            else:
                loc += 1
        return result

    def _is_label(self, line):
        return line.endswith(":")
    # [/labels]

    # [compile]
    def _compile(self, instruction, labels):
        # labels = {"loop": 2}
        # instruction = "ldc R0 1"
        tokens = instruction.split()
        # tokens = ["ldc", "R0", "1"]
        op, args = tokens[0], tokens[1:]
        fmt, code = OPS[op]["fmt"], OPS[op]["code"]

        if fmt == "--":
            return self._combine(code)

        elif fmt == "r-":
            return self._combine(self._reg(args[0]), code)

        elif fmt == "rr":
            return self._combine(
                self._reg(args[1]), self._reg(args[0]), code
            )

        elif fmt == "rv":
            print(tokens)
            print("_val() result:")
            print(self._val(args[1], labels))

            print("_reg() result:")
            print(self._reg(args[0]))


            tmp = self._combine(
                self._val(args[1], labels),
                self._reg(args[0]), code
            )
            print(hex(tmp))
            print()
            return self._combine(
                self._val(args[1], labels),
                self._reg(args[0]), code
            )
    # [/compile]

    # [value]
    def _val(self, token, labels):
        # print("token = ", token, "labels = ", labels)
        if token[0] != "@":
            return int(token)
        # only if beq or bne
        lbl = token[1:]
        assert lbl in labels, f"Unknown label '{token}'"
        return labels[lbl]  # return value at key @loop -> {"loop": 2} -> 2
    # [/value]

    # [combine]
    def _combine(self, *args):
        assert len(args) > 0, "Cannot combine no arguments"
        result = 0
        for a in args:
            result <<= OP_SHIFT
            result |= a
        # print("*args = ", args, "result = ", result)
        return result
    # [/combine]

    def _to_text(self, program):
        return [f"{op:06x}" for op in program]

    def _get_lines(self, lines):
        lines = [ln.strip() for ln in lines]  # remove \n
        lines = [ln for ln in lines if len(ln) > 0]  # remove empty line
        lines = [ln for ln in lines if not self._is_comment(ln)]  # remove #-line (comment lines)
        return lines

    def _is_comment(self, line):
        return line.startswith("#")

    def _reg(self, token):
        # Getting register number: R0 -> 0, R1 -> 1, etc.
        assert token[0] == "R", f"Register '{token}' does not start with 'R'"
        r = int(token[1:])
        assert 0 <= r < NUM_REG, f"Illegal register {token}"
        return r

def main(assembler_cls):
    assert len(sys.argv) == 3, f"Usage: {sys.argv[0]} input|- output|-"
    reader = open(sys.argv[1], "r") if (sys.argv[1] != "-") else sys.stdin
    writer = open(sys.argv[2], "w") if (sys.argv[2] != "-") else sys.stdout
    lines = reader.readlines()
    assembler = assembler_cls()
    program = assembler.assemble(lines)  # list (lines) of instructions from .as file in hexadecimal format
    for instruction in program:
        print(instruction, file=writer)  # write hexadecimal lines to .mx files -> will be processed by vm

""""
class DataAllocator(Assembler):

    # [assemble]
    DIVIDER = ".data"

    def assemble(self, lines):
        lines = self._get_lines(lines)
        to_compile, to_allocate = self._split(lines)
        print("To Compile:")
        print(to_compile)
        print("To Allocate:")
        print(to_allocate)

        labels = self._find_labels(lines)
        print("Labels:")
        print(labels)
        instructions = [ln for ln in to_compile if not self._is_label(ln)]

        base_of_data = len(instructions)
        self._add_allocations(base_of_data, labels, to_allocate)
        print("Labels after allocations:")
        print(labels)

        compiled = [self._compile(instr, labels) for instr in instructions]
        program = self._to_text(compiled)
        return program

    def _split(self, lines):
        try:
            split = lines.index(self.DIVIDER)
            return lines[0:split], lines[split + 1:]
        except ValueError:
            return lines, []
    # [/assemble]

    # [allocate]
    def _add_allocations(self, base_of_data, labels, to_allocate):
        for alloc in to_allocate:
            fields = [a.strip() for a in alloc.split(":")]
            assert len(fields) == 2, f"Invalid allocation directive '{alloc}'"
            lbl, num_words_text = fields
            assert lbl not in labels, f"Duplicate label '{lbl}' in allocation"
            num_words = int(num_words_text)
            assert (base_of_data + num_words) < RAM_LEN, \
                f"Allocation '{lbl}' requires too much memory"
            labels[lbl] = base_of_data
            base_of_data += num_words
    # [/allocate]
"""

# [main]
if __name__ == "__main__":
    # main(DataAllocator)
    main(Assembler)
# [/main]
