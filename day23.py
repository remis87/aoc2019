from threading import Thread, Lock
import time


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
        self.suspend = False
        self.idle = False

    def run(self):
        pp = self.return_pointer
        while pp >= 0 and not self.suspend:
            opt_code = self.program[pp] % 100
            mode = str(self.program[pp])[:-2].zfill(3)
            pp = self.switch[opt_code](self.program, pp, mode)
        return self.output

    def resume(self):
        self.suspended = False
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
        inp = self._get_input()
        if isinstance(inp, int):
            self._write_to_memory(_program[pp + 1], inp, mode[2])
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


class Networker(IntCodeProgram):
    def __init__(self, name, file_name, inp: []):
        with open(file_name) as f:
            int_code = [int(x) for x in f.readline().split(',')]
            super().__init__(name, int_code)
        self.input = inp
        self.ipr = 0
        self.opr = 0
        self.input_mutex = Lock()
        self.attempts = 0

    def _get_input(self):
        self.input_mutex.acquire()
        if self.ipr >= len(self.input):
            if self.attempts > 4:
                self.idle = True
                self.attempts = 0
            self.attempts += 1
            self.input_mutex.release()
            return -1
        self.idle = False
        inp = self.input[self.ipr]
        self.ipr += 1
        self.attempts = 0
        self.input_mutex.release()
        return inp

    def add_input(self, new_input: []):
        self.input_mutex.acquire()
        self.input += new_input
        self.input_mutex.release()

    def _handle_output(self, out):
        self.input_mutex.acquire()

        if len(self.output[self.opr:]) == 3:
            addr, x, y = self.output[self.opr], self.output[self.opr + 1], self.output[self.opr + 2]
            # print(self.name + " Sending {} {} {}".format(addr, x, y))
            computers[addr].add_input([x, y])
            self.opr += 3
        self.input_mutex.release()

    def is_idle(self):
        self.input_mutex.acquire()
        idle = self.idle
        self.input_mutex.release()
        return idle


class NAT:
    def __init__(self):
        self.x = -1
        self.y = -1
        self.last_sent = None
        self.mutex = Lock()

    def is_idle(self):
        return True

    def add_input(self, inp: []):
        self.mutex.acquire()
        print("NAT getting package: {}".format(inp))
        self.x = inp[0]
        self.y = inp[1]
        self.mutex.release()

    def check_idle(self):
        print("NAT checking idle")
        return all(map(lambda x: x.is_idle(), computers.values()))

    def run(self):
        print("starting NAT")
        time.sleep(15)
        while True:
            if self.check_idle() and self.x > 0 and self.y > 0:
                print("NAT sending package {}".format((self.x, self.y)))
                if self.last_sent and self.last_sent[1] == self.y:
                    print("********\n********\n********\n********\n********\n{}".format(self.last_sent))
                computers[0].add_input([self.x, self.y])
                self.last_sent = (self.x, self.y)


computers = {}
for i in range(50):
    computers[i] = Networker("n{}".format(i), 'input', [i])
computers[255] = NAT()
Thread(target=computers[255].run).start()
for i in range(50):
    t = Thread(target=computers[i].run)
    print("Starting {}".format(i))
    t.start()
