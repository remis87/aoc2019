input = 5
output = 0
def opt1(prog, pp, mode):
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
    prog[prog[pp + 3]] = a + b
    return pp + 4


def opt2(prog, pp, mode):
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


def opt3(prog, pp, mode):
    global input
    prog[prog[pp+1]] = input
    return pp + 2

def opt4(prog, pp, mode):
    global output
    output = prog[prog[pp+1]]
    print("output: {}".format(output))
    return pp + 2


def opt5(prog, pp, mode):
    m1 = mode[2]
    m2 = mode[1]
    if m1 == '0':
        x = prog[prog[pp + 1]]
    else:
        x = prog[pp+1]
    if x != 0:
        if m2 == '0':
            return prog[prog[pp + 2]]
        else:
            return prog[pp + 2]
    return pp + 3


def opt6(prog, pp, mode):
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


def opt7(prog, pp, mode):
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
    prog[prog[pp+3]] = ret
    return pp + 4


def opt8(prog, pp, mode):
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


def opt99(prog, _1, _2):
    return -1


switch = {1: opt1, 2: opt2, 3: opt3, 4: opt4, 5: opt5, 6: opt6, 7: opt7, 8: opt8, 99: opt99}

with open('input') as f:
    program = list(map(lambda x: int(x), f.readline().split(',')))

pp = 0
while pp >= 0:
    opt_code = program[pp] % 100
    mode = str(program[pp])[:-2].zfill(3)
    pp = switch[opt_code](program, pp, mode)
