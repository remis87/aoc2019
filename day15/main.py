from random import choice
from os import system
from dijkstar import Graph, find_path, NoPathError
import curses
import time

stdscr = curses.initscr()
pad = curses.newwin(50, 50, 0, 0)


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
        self.new_position = (0, 0)
        self.position = (0, 0)
        self.area = {(0, 0): 'X'}
        self.graph = Graph()
        self.graph.add_node((0, 0))
        self.oxygen = (0, 0)
        self.unexplored = set()
        self.explored = set([(0, 0)])
        self.graph.add_node((0, 0))
        self.path = []

    def run(self, inputs):
        if not self.halt:
            pp = self.retpt
            while pp >= 0:
                # console.log("executing pp {}".format(pp))
                opt_code = program[pp] % 100
                mode = str(program[pp])[:-2].zfill(3)
                pp = self.switch[opt_code](self.program, pp, mode, inputs)
        return self.output

    def print_area(self, cl=True):
        sz = 21
        min_x = -sz
        min_y = -sz
        for point in self.unexplored:
            area_x = point[0] - min_x
            area_y = point[1] - min_y
            pad.addch(area_y, area_x, '?')
        for point in self.area.keys():
            area_x = point[0] - min_x
            area_y = point[1] - min_y
            pad.addch(area_y, area_x, self.area[point])
        cursor_x = self.position[0] - min_x
        cursor_y = self.position[1] - min_y
        pad.move(cursor_y, cursor_x)
        pad.refresh()

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

    def get_new_pos(self, direction):
        if direction == 1:
            np = self.position[0], self.position[1] + 1
        if direction == 2:
            np = self.position[0], self.position[1] - 1
        if direction == 3:
            np = self.position[0] + 1, self.position[1]
        if direction == 4:
            np = self.position[0] - 1, self.position[1]
        return np

    def get_input(self):
        p = self.position
        neighbors = [(p[0], p[1] + 1), (p[0], p[1] - 1), (p[0] + 1, p[1]), (p[0] - 1, p[1])]
        choices = []
        for i in range(4):
            if self.area.get(neighbors[i], '.') != '#':
                choices.append(i + 1)
                if not neighbors[i] in self.area:
                    choices.append(i + 1)
                    choices.append(i + 1)
        c = choice(choices)
        newly_unexplored = set(neighbors).difference(self.explored)
        self.unexplored.update(newly_unexplored)
        return c

    def get_dir_to_next_pos(self, new_pos):
        pos = self.position
        x_diff = pos[0] - new_pos[0]
        y_diff = pos[1] - new_pos[1]
        out = -1
        if x_diff == -1:
            out = 3
        if x_diff == 1:
            out = 4
        if y_diff == -1:
            out = 1
        if y_diff == 1:
            out = 2
        newly_unexplored = set(self.get_neighbors(self.position)).difference(self.explored)
        self.unexplored.update(newly_unexplored)
        return out

    def get_path_to_unexplored(self, unex):
        paths = []
        for candidate in self.get_neighbors(unex).intersection(self.explored):
            paths.append(find_path(self.graph, self.position, candidate))
        node_seq = min(paths, key=lambda x: x.total_cost).nodes
        node_seq.append(unex)
        return node_seq[1:]

    def opt3(self, prog, pp, mode, inputs):
        if len(self.path) == 0 and len(self.unexplored) > 0:
            closest_unex = min(self.unexplored,
                               key=lambda x: abs(self.position[0] - x[0]) + abs(self.position[1] - x[1]))
            path = self.get_path_to_unexplored(closest_unex)
            self.path = path
        if len(self.path) > 0:
            inp = self.get_dir_to_next_pos(self.path.pop(0))
        else:
            inp = self.get_input()
        self.new_position = self.get_new_pos(inp)
        self.unexplored = self.unexplored.difference(set(self.area.keys()))
        self.write_to_memory(prog[pp + 1], inp, mode[2])
        return pp + 2

    def get_symbol(self, code):
        code_map = {0: '#', 1: '.', 2: 'O'}
        return code_map[code]

    def get_neighbors(self, p):
        return {(p[0], p[1] + 1), (p[0], p[1] - 1), (p[0] + 1, p[1]), (p[0] - 1, p[1])}

    def addNodeToGraph(self, u, v):
        if u not in self.graph:
            self.graph.add_node(u)
        if v not in self.graph:
            self.graph.add_node(v)
        self.graph.add_edge(u, v, 1)
        self.graph.add_edge(v, u, 1)

    def opt4(self, prog, pp, mode, _):
        out = self.read_value(pp, 1, mode[2])
        self.output.append(out)
        self.area[self.new_position] = self.get_symbol(out)

        if out == 1:
            self.explored.add(self.new_position)
            self.addNodeToGraph(self.position, self.new_position)
            self.position = self.new_position
        if out == 2:
            self.explored.add(self.new_position)
            self.addNodeToGraph(self.position, self.new_position)
            self.oxygen = self.new_position
            self.position = self.new_position
        if len(self.unexplored) == 0 and len(self.explored) > 1:
            self.halt = True
            return -1
        self.print_area()
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

drawer = IntCodeProgram('robot', program)
drawer.run([])
drawer.print_area(False)

ox = drawer.oxygen
max = 0
for x in drawer.explored:
    distance_from_oxy = find_path(drawer.graph, ox, x).total_cost
    if distance_from_oxy > max:
        max = distance_from_oxy
print(max)
