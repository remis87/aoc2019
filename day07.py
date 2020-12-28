import itertools


class IntCodeProgram():
    def __init__(self, name, program):
        self.program = program
        self.name = name
        self.output = 0
        self.switch = {1: self.opt1, 2: self.opt2, 3: self.opt3, 4: self.opt4, 5: self.opt5, 6: self.opt6, 7: self.opt7,
                       8: self.opt8, 99: self.opt99}
        self.inputp = 0
        self.halt = False
        self.retp = 0

    def run(self, inputs):
        if not self.halt:
            pp = self.retp
            while pp >= 0:
                opt_code = program[pp] % 100
                mode = str(program[pp])[:-2].zfill(3)
                pp = self.switch[opt_code](self.program, pp, mode, inputs)
        return self.output

    def opt1(self, prog, pp, opt_mode, _):
        m1 = opt_mode[2]
        m2 = opt_mode[1]
        if m1 == '0':
            a = prog[prog[pp + 1]]
        else:
            a = prog[pp + 1]
        if m2 == '0':
            b = prog[prog[pp + 2]]
        else:
            b = prog[pp + 2]
        prog[prog[pp + 3]] = a + b
        return pp + 4

    def opt2(self, prog, pp, mode, _):
        m1 = mode[2]
        m2 = mode[1]
        if m1 == '0':
            a = prog[prog[pp + 1]]
        else:
            a = prog[pp + 1]
        if m2 == '0':
            b = prog[prog[pp + 2]]
        else:
            b = prog[pp + 2]
        prog[prog[pp + 3]] = a * b
        return pp + 4

    def opt3(self, prog, pp, mode, inputs):
        input = inputs[self.inputp]
        prog[prog[pp + 1]] = input
        if self.inputp == 0:
            self.inputp += 1
        return pp + 2

    def opt4(self, prog, pp, mode, _):
        self.output = prog[prog[pp + 1]]
        self.retp = pp + 2
        return -1

    def opt5(self, prog, pp, mode, _):
        m1 = mode[2]
        m2 = mode[1]
        if m1 == '0':
            x = prog[prog[pp + 1]]
        else:
            x = prog[pp + 1]
        if x != 0:
            if m2 == '0':
                return prog[prog[pp + 2]]
            else:
                return prog[pp + 2]
        return pp + 3

    def opt6(self, prog, pp, mode, _):
        m1 = mode[2]
        m2 = mode[1]
        if m1 == '0':
            x = prog[prog[pp + 1]]
        else:
            x = prog[pp + 1]
        if x == 0:
            if m2 == '0':
                return prog[prog[pp + 2]]
            else:
                return prog[pp + 2]
        return pp + 3

    def opt7(self, prog, pp, mode, _):
        m1 = mode[2]
        m2 = mode[1]
        m3 = mode[0]
        if m1 == '0':
            x = prog[prog[pp + 1]]
        else:
            x = prog[pp + 1]
        if m2 == '0':
            y = prog[prog[pp + 2]]
        else:
            y = prog[pp + 2]
        ret = 0
        if x < y:
            ret = 1
        prog[prog[pp + 3]] = ret
        return pp + 4

    def opt8(self, prog, pp, mode, _):
        m1 = mode[2]
        m2 = mode[1]
        m3 = mode[0]
        if m1 == '0':
            x = prog[prog[pp + 1]]
        else:
            x = prog[pp + 1]
        if m2 == '0':
            y = prog[prog[pp + 2]]
        else:
            y = prog[pp + 2]
        ret = 0
        if x == y:
            ret = 1
        prog[prog[pp + 3]] = ret
        return pp + 4

    def opt99(self, prog, _1, _2, _3):
        self.halt = True
        return -1


with open('input') as f:
    program = list(map(lambda x: int(x), f.readline().split(',')))

outputs = []
setting_list = itertools.permutations([5, 6, 7, 8, 9])

for settings in setting_list:
    signals = [0, 0, 0, 0, 0]
    A = IntCodeProgram('A', program.copy())
    B = IntCodeProgram('B', program.copy())
    C = IntCodeProgram('C', program.copy())
    D = IntCodeProgram('D', program.copy())
    E = IntCodeProgram('E', program.copy())
    while not (A.halt and B.halt and C.halt and D.halt and E.halt):
        signals[0] = A.run([settings[0], signals[4]])
        signals[1] = B.run([settings[1], signals[0]])
        signals[2] = C.run([settings[2], signals[1]])
        signals[3] = D.run([settings[3], signals[2]])
        signals[4] = E.run([settings[4], signals[3]])
    print("Signal for permutation {}: {}".format(settings, signals[4]))
    outputs.append(signals[4])
print(max(outputs))
