import sys
from architecture import OPS, VMState
from vm_extend import VirtualMachineExtend

class VirtualMachineBreak(VirtualMachineExtend):
    def __init__(self):
        super().__init__()
        self.breaks = {}
        self.watchpoints = {}
        self.handlers |= {
            "b": self._do_add_breakpoint,
            "break": self._do_add_breakpoint,
            "c": self._do_clear_breakpoint,
            "clear": self._do_clear_breakpoint,
            "w": self._do_add_watchpoint,
            "watch": self._do_add_watchpoint,
            "cw": self._do_clear_watchpoint,
            "clearwatch": self._do_clear_watchpoint,
        }

    def show(self, *args):
        try:
            super().show(args[0])
        except:
            super().show()
        if self.breaks:
            self.write("-" * 6)
            for key, instruction in self.breaks.items():
                self.write(f"{key:06x}: {self.disassemble(key, instruction)}")

    def run(self):
        self.state = VMState.STEPPING
        while self.state != VMState.FINISHED:
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

    def _do_add_breakpoint(self, addr, addr_arg=None):
        if addr_arg is not None:
            try:
                addr = int(addr_arg[0], 16)  # Convert hexadecimal string to integer
            except ValueError:
                self.write("Invalid address format\n")
                return True
        else:
            self.write("No address specified for breakpoint\n")
            return True

        if addr in self.breaks:
            self.write(f"Breakpoint already set at {addr:06x}\n")
            return True

        self.breaks[addr] = self.ram[addr]
        self.ram[addr] = OPS["brk"]["code"]
        self.write(f"Breakpoint set at {addr:06x}\n")
        return True


    def _do_clear_breakpoint(self, addr, addr_arg=None):
        if addr_arg is not None:
            try:
                addr = int(addr_arg[0], 16)  # Convert hexadecimal string to integer
            except ValueError:
                self.write("Invalid address format\n")
                return True
        else:
            self.write("No address specified to clear breakpoint\n")
            return True

        if addr not in self.breaks:
            self.write(f"No breakpoint set at {addr:06x}\n")
            return True

        self.ram[addr] = self.breaks[addr]
        del self.breaks[addr]
        self.write(f"Breakpoint cleared at {addr:06x}\n")
        return True


    def _do_add_watchpoint(self, addr, addr_arg=None):
        if addr_arg is not None:
            try:
                addr = int(addr_arg[0], 16)  # Convert hexadecimal string to integer
            except ValueError:
                self.write("Invalid address format\n")
                return True
        else:
            self.write("No address specified for watchpoint\n")
            return True

        self.watchpoints[addr] = self.ram[addr]
        self.write(f"Watchpoint set at {addr:06x}\n")
        return True


    def _do_clear_watchpoint(self, addr, addr_arg=None):
        if addr_arg is not None:
            try:
                addr = int(addr_arg[0], 16)  # Convert hexadecimal string to integer
            except ValueError:
                self.write("Invalid address format\n")
                return True
        else:
            self.write("No address specified to clear watchpoint\n")
            return True

        if addr in self.watchpoints:
            del self.watchpoints[addr]
            self.write(f"Watchpoint cleared at {addr:06x}\n")
        else:
            self.write(f"No watchpoint set at {addr:06x}\n")


if __name__ == "__main__":
    VirtualMachineBreak.main()
