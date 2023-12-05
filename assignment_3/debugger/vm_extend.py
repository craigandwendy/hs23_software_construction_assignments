import sys

from architecture import VMState
from vm_step import VirtualMachineStep


class VirtualMachineExtend(VirtualMachineStep):
    # [init]
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
    # [/init]

    # [interact]
    def interact(self, addr):
        # controls if user input is valid and calls functions
        prompt = "".join(sorted({key[0] for key in self.handlers}))
        # print(f"\nprompt = {prompt}\n")  # delete this line
        interacting = True
        while interacting:
            try:
                command = self.read(f"{addr:06x} [{prompt}]> ")  # command = user input
                # handle emtpy input
                if not command:  # empty input -> ""
                    continue
                # handle commands with additional parameters
                elif command not in self.handlers:  # can be "mem 0 4" or "r" or unknown command -> needs further clean-up
                    try:  # if out of any reason an error appears it will be caught and whole program stopped
                        command_args = command.split()  # split command: before "mem 0 4" -> ["mem", "0", "4"]
                        command_found = {key: value for key, value in self.handlers.items() if key.startswith(command_args[0])}
                        if command_found == {}:
                            self.write(f"Unknown command {command_args[0]}")
                        else:
                            key, value = command_found.popitem()
                            # handle memory commands
                            if key in self.handlers and key == "memory":  # only memory takes additional parameters
                                try:
                                    opt_args = [int(a) for a in command_args[1:]]  # address must be numeric!
                                    interacting = self.handlers[key](self.ip, opt_args)  # True or False
                                except:
                                    self.write(f"Expected numerical values but received: {command_args[1:]}")
                            # handle clear or break commands
                            elif key in self.handlers and (key == "clear" or key == "break"):  # clear/break can take 1 address
                                if len(command_args[1:]) > 1:
                                    self.write(f"Expected length 0 or 1 but received {command_args[1:]}")
                                else:
                                    try:
                                        interacting = self.handlers[key](int(command_args[1]))
                                    except:
                                        self.write(f"Exptected numerical address but received type {type(command_args[1])}")
                            # handle watchpoint commands
                            elif key in self.handlers and key == "watchpoint":  # takes exactly 1 address/parameter
                                if len(command_args[1:]) != 1:
                                    self.write(f"{key}: expected length 1 but received {command_args[1:]}")
                                else:
                                    try:
                                        interacting = self.handlers[key](int(command_args[1]))
                                    except:
                                        self.write(f"Exptected numerical address but received type {type(command_args[1])}")
                            # make sure other command do not contain additional parameters
                            elif key in self.handlers and command_args[1:]:  # other functions should not take memory address as additional parameters
                                self.write(f"Command {key} does not take additional parameters {command_args[1:]}")
                            # handle all other commands
                            elif key in self.handlers:
                                interacting = self.handlers[key](self.ip)
                            # handle unknown commands
                            else:
                                self.write(f"Unknown command {command_args[0]}")
                    # handle any other kind of invalid input or errors occured in try block
                    except:
                        self.write(f"Invalid input: {command}")
                        # self.state = VMState.FINISHED
                        # interacting = False
                        # raise AssertionError(f"Invalid input: {command}")
                # handle commands without additional parameters
                else:
                    try:
                        command_found = {key: value for key, value in self.handlers.items() if key.startswith(command)}
                        key, value = command_found.popitem()
                        if key in self.handlers:
                            if key == "watchpoint":
                                self.write(f"watchpoint takes memory address as argument. Missing 1 argument.")
                            else:
                                interacting = self.handlers[key](self.ip)
                    except:
                        interacting = self.handlers[command](self.ip)
            except EOFError:
                self.state = VMState.FINISHED
                interacting = False
    # [/interact]

    def _do_disassemble(self, addr):
        self.write(self.disassemble(addr, self.ram[addr]))
        return True

    def _do_ip(self, addr):
        self.write(f"{self.ip:06x}")
        return True

    # [memory]
    def _do_memory(self, addr, *args):
        # print(f"\n*args = {args[0]}\n")  # delete this line
        # print(f"\naddr = {addr}\n")  # delete this line
        try:
            addr_args = [int(a) for a in args[0]]  # make sure only numeric values
            self.show(addr_args)
        except:
            self.show()
        return True
    # [/memory]

    def _do_quit(self, addr):
        self.state = VMState.FINISHED
        return False

    def _do_run(self, addr):
        self.state = VMState.RUNNING
        return False

    # [step]
    def _do_step(self, addr):
        self.state = VMState.STEPPING
        return False
    # [/step]


if __name__ == "__main__":
    VirtualMachineExtend.main()
