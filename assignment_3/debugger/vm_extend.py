import sys
from architecture import VMState
from vm_step import VirtualMachineStep

class VirtualMachineExtend(VirtualMachineStep):
    def __init__(self, reader=input, writer=sys.stdout):
        super().__init__(reader, writer)
        self.handlers = {
            "disassemble": self._do_disassemble,
            "ip": self._do_ip,
            "memory": self._do_memory,
            "quit": self._do_quit,
            "run": self._do_run,
            "step": self._do_step
        }

    def interact(self, addr):
        prompt = "".join(sorted({key[0] for key in self.handlers}))
        interacting = True
        while interacting:
            try:
                command = self.read(f"{addr:06x} [{prompt}]> ")
                if not command:
                    continue
                command_args = command.split()
                command_name = command_args[0]
                args = command_args[1:]
                if command_name in self.handlers:
                    interacting = self.handlers[command_name](addr, args)
                elif any(cmd.startswith(command_name) for cmd in self.handlers):
                    full_command = next(cmd for cmd in self.handlers if cmd.startswith(command_name))
                    interacting = self.handlers[full_command](addr, args)
                else:
                    self.write(f"Unknown command '{command_name}'\n")
            except EOFError:
                self.state = VMState.FINISHED
                interacting = False

    def _do_disassemble(self, addr, *args):
        self.write(self.disassemble(addr, self.ram[addr]))
        return True

    def _do_ip(self, addr, *args):
        self.write(f"{self.ip:06x}")
        return True

    def _do_memory(self, addr, *args):
        try:
            if args:
                addr_args = [int(a, 16) for a in args[0]]
                self.show(addr_args)
            else:
                self.show()
        except ValueError:
            self.write("Invalid address format\n")
        return True

    def _do_quit(self, addr, *args):
        self.state = VMState.FINISHED
        return False

    def _do_run(self, addr, *args):
        self.state = VMState.RUNNING
        return False

    def _do_step(self, addr, *args):
        self.state = VMState.STEPPING
        return False

if __name__ == "__main__":
    VirtualMachineExtend.main()
