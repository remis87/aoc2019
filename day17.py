import dijkstar
import itertools


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
        if not self.halt:
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

    def _handle_output(self):
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
        self._handle_output()
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


class ScaffoldingIntcode(IntCodeProgram):
    def __init__(self, program):
        super().__init__("Scaffolder", program)


with open('input') as f:
    int_code = [int(x) for x in f.readline().split(',')]
    print(int_code)


def print_map(m):
    for row in m:
        print(''.join(row))


def idx(x, y, m):
    return m[y][x]


def get_neighbors(t, m):
    x, y = t
    unfiltered = {(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)}
    return set(filter(lambda tpl: 0 <= tpl[0] < len(m[0]) and 0 <= tpl[1] < len(m),
                      unfiltered))


def build_scaffolding(m):
    g = dijkstar.Graph()
    for y, row in enumerate(m):
        for x, col in enumerate(row):
            if m[y][x] == '#' or m[y][x] == '^':
                neighbors = get_neighbors((x, y), m)
                t = (x, y)
                if t not in g:
                    g.add_node((x, y))
                for neighbor in neighbors:
                    n1, n2 = neighbor
                    if m[n2][n1] == '#' or m[n2][n1] == '^':
                        if neighbor not in g:
                            g.add_node(neighbor)
                        g.add_edge(t, neighbor, 1)
                        g.add_edge(neighbor, t, 1)
    return g


def add_horizontal_bridge(g: dijkstar.Graph, position):
    x, y = position
    print("adding {},{} and {},{}".format((x - 1, y), (x + 1, y),(x + 1, y), (x - 1, y)))
    g.add_edge((x - 1, y), (x + 1, y))
    g.add_edge((x + 1, y), (x - 1, y))


def remove_horizontal_bridge(g: dijkstar.Graph, position):
    print("removing horizontal for {}".format(position))
    x, y = position
    g.remove_edge((x - 1, y), (x + 1, y))
    g.remove_edge((x + 1, y), (x - 1, y))


def add_vertical_bridge(g: dijkstar.Graph, position):
    x, y = position
    g.add_edge((x, y + 1), (x, y - 1))
    g.add_edge((x, y - 1), (x, y) + 1)


def remove_vertical_bridge(g: dijkstar.Graph, position):
    x, y = position
    g.remove_edge((x, y + 1), (x, y - 1))
    g.remove_edge((x, y - 1), (x, y) + 1)


def try_combination(comb, crossings, graph: dijkstar.Graph, start_end):
    for i, c in enumerate(comb):
        if c == 0:
            add_horizontal_bridge(graph, crossings[i])
        else:
            add_vertical_bridge(graph, crossings[i])
    try:
        path = dijkstar.find_path(graph, start_end[0], start_end[1])
        print("Path for comb {} has length {}".format(comb, path.total_cost))
    except dijkstar.NoPathError:
        print("No path for {}".format(comb))
    for i, c in enumerate(comb):
        if c == 0:
            remove_horizontal_bridge(graph, crossings[i])
        else:
            remove_vertical_bridge(graph, crossings[i])


s = ScaffoldingIntcode(int_code)
s.run()
ascii_list = [chr(x) for x in s.output]
game_map = ''.join(ascii_list).split('\n')
game_map = [[c for c in s] for s in game_map if len(s) > 0]
graph = build_scaffolding(game_map)
num_nodes = len(graph)
crossings = [n for n in graph.keys() if len(graph.get_incoming(n)) == 4]
start_end = [n for n in graph.keys() if len(graph.get_incoming(n)) == 1]
combinations = list(itertools.product(range(2), repeat=len(crossings)))
print(crossings)
print(graph.get_incoming((17,8)))
for crossing in crossings:
    graph.remove_node(crossing)
print(graph.get_incoming((17,8)))
print(start_end)
for comb in combinations:
    try_combination(comb, crossings, graph, start_end)
