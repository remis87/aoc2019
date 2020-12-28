from intcode.intcode import IntCodeProgram


class Santa(IntCodeProgram):
    def __init__(self):
        super().__init__("name", [1])


x = Santa()
print("Hello World")
