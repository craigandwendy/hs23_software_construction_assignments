from ex2_assembler import Assembler
from ex2_disassembler import Disassembler
import pytest


@pytest.mark.parametrize("input_", [("ex2_test1.as"), ("ex2_test2.as")])  # [("ex2_test_1.as", "ex2_test_1_disassembled.as")])
def test_disassembler(input_):
    # write test input
    act = Assembler()
    with open(input_, "r") as f:
        lines_act = f.readlines()  # input.as
    # write into .mx file
    new_file_name = input_[:-3] + ".mx"
    with open(new_file_name, "w") as f:
        assembled_lines = act.assemble(lines_act)  # assembled.mx
        #assembles_lines = [f"{ln}\n" for ln in assembled_lines]
        for instruction in assembled_lines:
            f.writelines(instruction + "\n")
        #f.writelines(assembled_lines)

    # disassemble .mx file
    exp = Disassembler()
    new_file_name = input_[:-3] + "_disassembled.as"
    with open(new_file_name, "w") as f:
        disassembled_lines = exp.disassemble(assembled_lines)  # disassembled.as
        disassembled_lines = [f"{ln}\n" for ln in disassembled_lines]
        f.writelines(ln for ln in disassembled_lines)

    # check is disassembler works correctly: input.as -> assembled.mx -> disassembled.as
    # if disassembler works perfectly: inputs.as == disassembled.as
    assert lines_act == disassembled_lines
