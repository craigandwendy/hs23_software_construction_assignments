import sys

from architecture import OPS, VMState
from vm_base import VirtualMachineBase

# [lookup]
OPS_LOOKUP = {value["code"]: key for key, value in OPS.items()}
# [/lookup]

# [derive]
class VirtualMachineStep(VirtualMachineBase):
# [/derive]
    # [init]
    def __init__(self, reader=input, writer=sys.stdout):
        super().__init__(writer)
        self.reader = reader
    # [/init]

    # [run]
    def run(self):
        self.state = VMState.STEPPING
        while True:
            if self.state == VMState.STEPPING:
                self.interact(self.ip)
            if self.state == VMState.FINISHED:
                break
            instruction = self.ram[self.ip]
            self.ip += 1
            op, arg0, arg1 = self.decode(instruction)
            self.execute(op, arg0, arg1)
    # [/run]

    # [interact]
    def interact(self, addr):
        while self.state == VMState.STEPPING:
            try:
                command = self.read(f"{addr:06x} [dmqrs]> ")
                if not command:
                    continue
                elif "disassemble".startswith(command):  # catch casses such as d, dis, disas, etc.
                    self.write(self.disassemble(addr, self.ram[addr]))
                elif "memory".startswith(command):  # catch cases such as m, me, mem, etc.
                    self.show()
                elif "quit".startswith(command):
                    self.state = VMState.FINISHED
                    break
                elif "run".startswith(command):
                    self.state = VMState.RUNNING
                    break
                elif "step".startswith(command):
                    break
                else:
                    self.write(f"Unknown command '{command}'")
            except EOFError:
                self.state = VMState.FINISHED
    # [/interact]

    # [disassemble]
    def disassemble(self, addr, instruction):
        op, arg0, arg1 = self.decode(instruction)
        assert op in OPS_LOOKUP, f"Unknown op code {op} at {addr}"
        return f"{OPS_LOOKUP[op]} | {arg0} | {arg1}"
    # [/disassemble]

    # [read]
    def read(self, prompt, *args):
        # print(f"\n*args = {args}\n")  # delete this line
        return self.reader(prompt).strip()
    # [/read]

if __name__ == "__main__":
    VirtualMachineStep.main()
