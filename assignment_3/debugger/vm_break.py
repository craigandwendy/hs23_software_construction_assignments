import sys

from architecture import OPS, VMState
from vm_extend import VirtualMachineExtend


class VirtualMachineBreak(VirtualMachineExtend):
    # [init]
    def __init__(self):
        super().__init__()
        self.breaks = {}
        self.watchpoints = {}  # 4.4
        self.handlers |= {
            "b": self._do_add_breakpoint,
            "break": self._do_add_breakpoint,
            "c": self._do_clear_breakpoint,
            "clear": self._do_clear_breakpoint,
            "watchpoint": self._do_add_watchpoint  # 4.4
        }
    # [/init]

    # [show]
    def show(self, *args):  # *args added
        try:
            super().show(args[0])  # args added
        except:
            super().show()
        if self.breaks:
            self.write("-" * 6)
            for key, instruction in self.breaks.items():
                self.write(f"{key:06x}: {self.disassemble(key, instruction)}")
    # [/show]

    # [run]
    def run(self):
        self.state = VMState.STEPPING
        while self.state != VMState.FINISHED:

            # check if any value at address has changed compared to original memory
            for addr in self.watchpoints:
                if self.ram[addr] != self.watchpoints[addr]:  # value at address addr changed
                    self.state = VMState.STEPPING  # change state to stepping
                    self.write(f"Value at {addr} changed from {self.watchpoints[addr]} to {self.ram[addr]}")  # show message
                    self._do_add_watchpoint(addr)  # update value at address


            instruction = self.ram[self.ip]
            op, arg0, arg1 = self.decode(instruction)
            if op == OPS["brk"]["code"]:
                original = self.breaks[self.ip]
                op, arg0, arg1 = self.decode(original)
                self.interact(self.ip)
                self.ip += 1
                self.execute(op, arg0, arg1)
            else:
                if self.state == VMState.STEPPING:
                    self.interact(self.ip)
                self.ip += 1
                self.execute(op, arg0, arg1)
    # [/run]

    # [add]
    def _do_add_breakpoint(self, addr):
        if self.ram[addr] == OPS["brk"]["code"]:
            return
        self.breaks[addr] = self.ram[addr]
        self.ram[addr] = OPS["brk"]["code"]
        return True
    # [/add]

    # [clear]
    def _do_clear_breakpoint(self, addr):
        if self.ram[addr] != OPS["brk"]["code"]:
            return
        self.ram[addr] = self.breaks[addr]
        del self.breaks[addr]
        return True
    # [/clear]

    # [watchpoint]
    def _do_add_watchpoint(self, addr):
        # if self.ram[addr] == OPS["wtp"]["code"]:
        #     return
        self.watchpoints[addr] = self.ram[addr]  # original instructions saved in dict -> {4: 120401}
        # self.ram[addr] = OPS["wtp"]["code"]
        return True
    # [/watchpoint]


if __name__ == "__main__":
    VirtualMachineBreak.main()
