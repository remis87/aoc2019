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

    def run(self, inputs):
        if not self.halt:
            pp = self.retpt
            while pp >= 0:
                opt_code = program[pp] % 100
                mode = str(program[pp])[:-2].zfill(3)
                pp = self.switch[opt_code](self.program, pp, mode, inputs)
        return self.output

    def read_value(self, pp, pp_offset, mode):
        index = 0
        if mode == '0':
            index = self.program[pp+pp_offset]
        if mode == '1':
            index = pp+pp_offset
        if mode == '2':
            index = self.relative_base + self.program[pp+pp_offset]
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

    def opt1(self, prog, pp, opt_mode, _):
        m1 = opt_mode[2]
        m2 = opt_mode[1]
        a = self.read_value(pp, 1, m1)
        b = self.read_value(pp, 2, m2)
        self.write_to_memory(prog[pp + 3], a+b, opt_mode[0])
        return pp + 4

    def opt2(self, prog, pp, mode, _):
        m1 = mode[2]
        m2 = mode[1]
        a = self.read_value(pp, 1, m1)
        b = self.read_value(pp, 2, m2)
        self.write_to_memory(prog[pp + 3], a * b, mode[0])
        return pp + 4

    def opt3(self, prog, pp, mode, inputs):
        inp = inputs[self.inputp]
        self.write_to_memory(prog[pp + 1], inp, mode[2])
        if self.inputp + 1 < len(inputs):
            self.inputp += 1
        return pp + 2

    def opt4(self, prog, pp, mode, _):
        out = self.read_value(pp, 1, mode[2])
        self.output.append(out)
        self.retpt = pp +2
        return -1

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


colors = {}
dirs = ['u', 'r', 'd', 'l']


def get_color(x):
    return colors.get(x, 0)


def paint(x, color):
    print('painting {}'.format(x))
    colors[x] = color



def move(current_position, current_dir):
    x = current_position[0]
    y = current_position[1]
    if current_dir == 'u':
        return x, y+1
    if current_dir == 'r':
        return x+1, y
    if current_dir == 'd':
        return x, y-1
    if current_dir == 'l':
        return x-1, y


def get_new_dir(current_dir, turn_dir):
    current_index = dirs.index(current_dir)
    if turn_dir == 1:
        return dirs[(current_index + 1) % len(dirs)]
    else:
        return dirs[(current_index - 1) % len(dirs)]


pos = (0, 0)
paint(pos, 1)
direction = 'u'
painted = set()
robot = IntCodeProgram('robby', program)
while not robot.halt:
    current_col = get_color(pos)
    col = robot.run([current_col])[-1]
    paint(pos, col)
    painted.add(pos)
    turn_dir = robot.run([current_col])[-1]
    direction = get_new_dir(direction, turn_dir)
    pos = move(pos, direction)
print(len(painted))

for j in range(50,-50,-1):
    row = ''
    for i in range(-50,50):
        if get_color((i, j)) == 0:
            row += '#'
        else:
            row += ' '
    print(row)
