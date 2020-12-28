from enum import Enum


class IntCodeProgram():
    class SuspendCode(Enum):
        AWATING_INPUT = 1
        OUTPUT = 2
        HALT = 3

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
        self.input_ptr = 0
        self.need_input = False
        self.output_ready = False
        self.input: [int] = []

    def run(self):
        pp = self.return_pointer
        while pp >= 0 and not self.need_input and not self.output_ready:
            opt_code = self.program[pp] % 100
            mode = str(self.program[pp])[:-2].zfill(3)
            pp = self.switch[opt_code](self.program, pp, mode)
        if self.need_input:
            return self.SuspendCode.AWATING_INPUT
        if self.output_ready:
            return self.SuspendCode.OUTPUT
        return self.SuspendCode.HALT

    def resume(self, inp: [int]):
        self.need_input = False
        self.output_ready = False
        self.input += inp
        self.run()

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
        if self.input_ptr >= len(self.input):
            self.return_pointer = pp
            self.need_input = True
            return -1
        inp = self.input[self.input_ptr]
        self.input_ptr += 1
        self._write_to_memory(_program[pp + 1], inp, mode[2])
        return pp + 2

    def opt4(self, _program, pp, mode):
        out = self._read_value(pp, 1, mode[2])
        self.output.append(out)
        self._handle_output(out)
        self.output_ready = True
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
