"""Intcode computer

Notes:
    Starting on day 15, I got tired of copy pasting my Intcode computer
    implmentation every other day.

    This file aims to replace all Intcode, starting from day 9 - the challenge
    the spec was completed.
"""

from enum import Enum, Flag, auto, unique


class IO(Flag):
    READ = auto()
    WRITE = auto()


@unique
class Mode(Enum):
    POS = 0
    IMM = 1
    REL = 2


@unique
class Opcode(Enum):
    HALT = 99, ()
    ADD = 1, (IO.READ, IO.READ, IO.WRITE)
    MULT = 2, (IO.READ, IO.READ, IO.WRITE)
    INPUT = 3, (IO.WRITE,)
    OUTPUT = 4, (IO.READ,)
    JUMP_TRUE = 5, (IO.READ, IO.READ)
    JUMP_FALSE = 6, (IO.READ, IO.READ)
    LESS_THAN = 7, (IO.READ, IO.READ, IO.WRITE)
    EQUALS = 8, (IO.READ, IO.READ, IO.WRITE)
    RB_OFFSET = 9, (IO.READ,)

    def __new__(cls, opcode, params):
        obj = object.__new__(cls)
        obj._value_ = opcode
        obj.io = params

        return obj


class Computer:
    def __init__(self, code):
        self.mem = dict(enumerate(code))
        self.ip = 0
        self.rb = 0
        self.cold = True
        self.program = self._compute()

    def __getitem__(self, ip):
        return self.mem.get(ip, 0)

    def __setitem__(self, ip, value):
        self.mem[ip] = value

    def _load_params(self, kinds, modes):
        p = [None] * 3
        for i, t in enumerate(zip(kinds, modes)):
            kind, mode = t
            v = self[self.ip + 1 + i]

            if mode is Mode.POS:
                if kind is IO.WRITE:
                    p[i] = v
                elif kind is IO.READ:
                    p[i] = self[v]
                else:
                    raise ValueError

            elif mode is Mode.IMM:
                if kind is IO.READ:
                    p[i] = v
                else:
                    raise ValueError

            elif mode is Mode.REL:
                if kind is IO.WRITE:
                    p[i] = self.rb + v
                elif kind is IO.READ:
                    p[i] = self[self.rb + v]
                else:
                    raise ValueError

            else:
                raise ValueError

        return p

    def _compute(self):
        out = []

        while True:
            instr = self[self.ip]

            op = Opcode(instr % 100)
            modes = tuple(Mode((instr // v) % 10) for v in (100, 1000, 10000))
            a, b, c = self._load_params(op.io, modes)

            self.ip += len(op.io) + 1

            if op is Opcode.HALT:
                break

            elif op is Opcode.ADD:
                self[c] = a + b

            elif op is Opcode.MULT:
                self[c] = a * b

            elif op is Opcode.INPUT:
                self[a] = yield out
                out.clear()

            elif op is Opcode.OUTPUT:
                out.append(a)

            elif op is Opcode.JUMP_TRUE:
                if a:
                    self.ip = b
                    continue

            elif op is Opcode.JUMP_FALSE:
                if not a:
                    self.ip = b
                    continue

            elif op is Opcode.LESS_THAN:
                self[c] = int(a < b)

            elif op is Opcode.EQUALS:
                self[c] = int(a == b)

            elif op is Opcode.RB_OFFSET:
                self.rb += a

            else:
                raise NotImplementedError

        yield out

        return None

    def run(self, *args):
        out = []

        if self.cold:
            out.extend(self.program.send(None))
            self.cold = False

        for a in args:
            out.extend(self.program.send(a))

        return out