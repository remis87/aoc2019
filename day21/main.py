class IntCodeProgram():

    def __init__(self, name, program):
        self.program = program
        self.name = name
        self.output = []
        self.switch = {1: self.opt1, 2: self.opt2, 3: self.opt3,
                       4: self.opt4, 5: self.opt5, 6: self.opt6, 7: self.opt7,
                       8: self.opt8, 9: self.opt9, 99: self.opt99}
        self.halt = False
        self.relative_base = 0
        self.memory = {}
        self.return_pointer = 0
        self.default_input = 0

    def run(self):
        pp = self.return_pointer
        while pp >= 0:
            opt_code = self.program[pp] % 100
            mode = str(self.program[pp])[:-2].zfill(3)
            pp = self.switch[opt_code](self.program, pp, mode)
        return self.output

    def _read_value(self, pp, pp_offset, mode):
        index = 0
        if mode == '0':
            index = self.program[pp + pp_offset]
        if mode == '1':
            index = pp + pp_offset
        if mode == '2':
            index = self.relative_base + self.program[pp + pp_offset]
        if index >= len(self.program):
            return self.memory.get(index, 0)
        return self.program[index]

    def _write_to_memory(self, index, value, mode):
        if mode == '2':
            index = self.relative_base + index
        if index >= len(self.program):
            self.memory[index] = value
        else:
            self.program[index] = value

    def _get_input(self):
        return self.default_input

    def _handle_output(self, out):
        pass

    def opt1(self, _program, pp, opt_mode):
        m1 = opt_mode[2]
        m2 = opt_mode[1]
        a = self._read_value(pp, 1, m1)
        b = self._read_value(pp, 2, m2)
        self._write_to_memory(_program[pp + 3], a + b, opt_mode[0])
        return pp + 4

    def opt2(self, _program, pp, mode):
        m1 = mode[2]
        m2 = mode[1]
        a = self._read_value(pp, 1, m1)
        b = self._read_value(pp, 2, m2)
        self._write_to_memory(_program[pp + 3], a * b, mode[0])
        return pp + 4

    def opt3(self, _program, pp, mode):
        self._write_to_memory(_program[pp + 1], self._get_input(), mode[2])
        return pp + 2

    def opt4(self, _program, pp, mode):
        out = self._read_value(pp, 1, mode[2])
        self.output.append(out)
        self._handle_output(out)
        self.return_pointer = pp + 2
        return pp + 2

    def opt5(self, _program, pp, mode):
        m1 = mode[2]
        m2 = mode[1]
        x = self._read_value(pp, 1, m1)
        if x != 0:
            return self._read_value(pp, 2, m2)
        return pp + 3

    def opt6(self, _program, pp, mode):
        m1 = mode[2]
        m2 = mode[1]
        x = self._read_value(pp, 1, m1)
        if x == 0:
            return self._read_value(pp, 2, m2)
        return pp + 3

    def opt7(self, _program, pp, mode):
        m1 = mode[2]
        m2 = mode[1]
        x = self._read_value(pp, 1, m1)
        y = self._read_value(pp, 2, m2)
        ret = 0
        if x < y:
            ret = 1
        self._write_to_memory(_program[pp + 3], ret, mode[0])
        return pp + 4

    def opt8(self, _program, pp, mode):
        m1 = mode[2]
        m2 = mode[1]
        m3 = mode[0]
        x = self._read_value(pp, 1, m1)
        y = self._read_value(pp, 2, m2)
        ret = 0
        if x == y:
            ret = 1
        self._write_to_memory(_program[pp + 3], ret, m3)
        return pp + 4

    def opt9(self, _program, pp, mode):
        inc = self._read_value(pp, 1, mode[2])
        self.relative_base += inc
        return pp + 2

    def opt99(self, *_):
        self.halt = True
        return -1


class Springscript(IntCodeProgram):
    def __init__(self, file_name, inp: []):
        with open(file_name) as f:
            int_code = [int(x) for x in f.readline().split(',')]
            super().__init__("spring", int_code)
        self.input = inp
        self.ascii_output = []
        self.ipr = 0

    def _get_input(self):
        inp = self.input[self.ipr]
        self.ipr += 1
        return inp

    def _handle_output(self, out):
        try:
            self.ascii_output.append(chr(out))
        except ValueError:
            print("got answer: {}".format(out))

    def print_output(self):
        print(''.join(self.ascii_output))


def get_command_as_ascii(command):
    return [ord(c) for c in command] + [ord('\n')]


def get_commands(s_str: str):
    ret = []
    for c in s_str:
        if c != ';':
            ret.append(ord(c))
        else:
            ret.append(10)
    return ret


commands = 'NOT B J;NOT C T;OR T J;AND D J;AND H J;NOT A T;OR T J;RUN;'

s = Springscript('input', get_commands(commands))
s.run()

s.print_output()
