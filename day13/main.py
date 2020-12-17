class IntCodeProgram():
    def __init__(self, name, program):
        self.program = program
        self.name = name
        self.output = []
        self.switch = {1: self.opt1, 2: self.opt2, 3: self.opt3, 4: self.opt4, 5: self.opt5, 6: self.opt6, 7: self.opt7,
                       8: self.opt8, 9: self.opt9, 99: self.opt99}
        self.inputp = 0
        self.halt = False
        self.relative_base = 0
        self.memory = {}
        self.retpt = 0
        self.ball_last_pos = None
        self.ball_pos = None
        self.bar_x = 0
        self.projected_ball_x = 0
        self.score = 0

    def run(self, inputs):
        if not self.halt:
            pp = self.retpt
            while pp >= 0:
                # console.log("executing pp {}".format(pp))
                opt_code = program[pp] % 100
                mode = str(program[pp])[:-2].zfill(3)
                pp = self.switch[opt_code](self.program, pp, mode, inputs)
        print("Done. Score: {}".format(self.score))
        return self.output

    def read_value(self, pp, pp_offset, mode):
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

    def write_to_memory(self, index, value, mode):
        if mode == '2':
            index = self.relative_base + index
        if index >= len(self.program):
            self.memory[index] = value
        else:
            self.program[index] = value

    def update_bar_position(self):
        self.bar_x = self.output[-3]

    def update_ball_position(self):
        if self.ball_last_pos:
            self.ball_last_pos = self.ball_pos
        self.ball_pos = (self.output[-3], self.output[-2])
        if not self.ball_last_pos:
            self.ball_last_pos = (self.output[-3], self.output[-2])
        self.projected_ball_x = self.ball_pos[0]

    def opt1(self, prog, pp, opt_mode, _):
        m1 = opt_mode[2]
        m2 = opt_mode[1]
        a = self.read_value(pp, 1, m1)
        b = self.read_value(pp, 2, m2)
        self.write_to_memory(prog[pp + 3], a + b, opt_mode[0])
        return pp + 4

    def opt2(self, prog, pp, mode, _):
        m1 = mode[2]
        m2 = mode[1]
        a = self.read_value(pp, 1, m1)
        b = self.read_value(pp, 2, m2)
        self.write_to_memory(prog[pp + 3], a * b, mode[0])
        return pp + 4

    def opt3(self, prog, pp, mode, inputs):
        inp = 0
        if self.projected_ball_x < self.bar_x:
            inp = -1
        elif self.projected_ball_x > self.bar_x:
            inp = 1
        self.write_to_memory(prog[pp + 1], inp, mode[2])
        return pp + 2

    def opt4(self, prog, pp, mode, _):
        out = self.read_value(pp, 1, mode[2])
        self.output.append(out)
        if len(self.output) % 3 == 0 and self.output[-3] >= 0:
            # print("updating position: {}".format(self.output[-3:]))
            if self.output[-1] == 4:
                self.update_ball_position()

            elif self.output[-1] == 3:
                self.update_bar_position()
        elif len(self.output) % 3 == 0 and self.output[-3] == -1:
            self.score = self.output[-1]
        self.retpt = pp + 2
        return pp + 2

    def opt5(self, prog, pp, mode, _):
        m1 = mode[2]
        m2 = mode[1]
        x = self.read_value(pp, 1, m1)
        if x != 0:
            return self.read_value(pp, 2, m2)
        return pp + 3

    def opt6(self, prog, pp, mode, _):
        m1 = mode[2]
        m2 = mode[1]
        x = self.read_value(pp, 1, m1)
        if x == 0:
            return self.read_value(pp, 2, m2)
        return pp + 3

    def opt7(self, prog, pp, mode, _):
        m1 = mode[2]
        m2 = mode[1]
        x = self.read_value(pp, 1, m1)
        y = self.read_value(pp, 2, m2)
        ret = 0
        if x < y:
            ret = 1
        self.write_to_memory(prog[pp + 3], ret, mode[0])
        return pp + 4

    def opt8(self, prog, pp, mode, _):
        m1 = mode[2]
        m2 = mode[1]
        m3 = mode[0]
        x = self.read_value(pp, 1, m1)
        y = self.read_value(pp, 2, m2)
        ret = 0
        if x == y:
            ret = 1
        self.write_to_memory(prog[pp + 3], ret, m3)
        return pp + 4

    def opt9(self, prog, pp, mode, _2):
        inc = self.read_value(pp, 1, mode[2])
        self.relative_base += inc
        return pp + 2

    def opt99(self, prog, _1, _2, _3):
        self.halt = True
        return -1


with open('input') as f:
    program = list(map(lambda x: int(x), f.readline().split(',')))

drawer = IntCodeProgram('draw', program)
drawer.run([])

