from ex1_assembler import Assembler
import ex1_architecture as architecture
import ex1_vm as VM
import ex1_arrays as arrays
import pytest


# https://docs.pytest.org/en/7.1.x/how-to/parametrize.html


@pytest.mark.parametrize("actual, expected", [("ex1_test_1.as", "ex1_test_1exp.mx"), ("ex1_test_2.as", "ex1_test_2exp.mx"), ("ex1_test_3.as", "ex1_test_3exp.mx"), ("ex1_test_4.as", "ex1_test_4exp.mx")])
def test_assembler(actual, expected):
    # write test input
    act = arrays.DataAllocator()
    with open(actual, "r") as f:
        lines_act = f.readlines()  # input.as

    with open(expected, "r") as f:
        lines_exp = f.readlines()
        lines_exp = [ln[:-1] for ln in lines_exp]
    # write into .mx file
    new_file_name = actual[:-3] + ".mx"
    with open(new_file_name, "w") as f:
        assembled_lines = act.assemble(lines_act)  # assembled.mx
        assert lines_exp == assembled_lines, "Actual != Expected"
        for instruction in assembled_lines:
            f.write(instruction + "\n")
        #f.writelines(assembled_lines)


@pytest.mark.parametrize("actual, expected", [("ex1_test_1.mx", "ex1_test_1exp.out"), ("ex1_test_2.mx", "ex1_test_2exp.out"), ("ex1_test_3.mx", "ex1_test_3exp.out"), ("ex1_test_4.mx", "ex1_test_4exp.out")])
def test_vm(actual, expected):
    # compare if actual and expected .mx yield to the same result
    # prepare actual_input

    act = VM.VirtualMachine()
    # get lines
    with open(actual, "r") as f:
        lines = [ln.strip() for ln in f.readlines()]
        program = [int(ln, 16) for ln in lines if ln]

    # run lines through virtual machine
    new_file_name = actual[:-3] + ".out"
    with open(new_file_name, "w") as f:
        act.initialize(program)
        act.run()
        act.show(f)

    # store vm output inside a file
    with open(new_file_name, "r") as f:
        actual_output = f.readlines()

    # get expected
    with open(expected, "r") as f:
        expected_output = f.readlines()

    # check if virtual machine created actual as expected
    assert actual_output == expected_output, "Actual != Expected"


@pytest.mark.parametrize("actual", [("ex1_test_5c1.as")])
def test_out_of_memory(actual):
    # get test_input
    res = arrays.DataAllocator()
    with open(actual, "r") as f:
        lines_act = f.readlines()
    # Out of Memory must raise AssertionError
    try:
        res.assemble(lines_act)
    except AssertionError:
        # catch AssertionError -> Out of Memory handled well
        assert True
    except Exception:
        # Out of Memory not well handled
        assert False


@pytest.mark.parametrize("actual", [("ex1_test_6c2.as")])
def test_instruction_not_found(actual):
    # get actual
    res = arrays.DataAllocator()
    with open(actual, "r") as f:
        lines_act = f.readlines()
    # Undefinded instruction must raise KeyError
    try:
        res.assemble(lines_act)
    except KeyError:
        # catch KeyError -> undefined instruction handled well
        assert True
    except Exception:
        # Undefined instruction not well handled
        assert False
