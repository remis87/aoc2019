"""Day 19: Tractor Beam

Usage:
    python 19.py < data/19.txt

Algorithm:
    1. Find a candidate solution using trigonometry
       1.1. Pick a large arbitrary Y (e.g. 1e6)
       1.2. Find the span of the beam (range [a, b]); I use binary search
       1.3. Determine the beam angles (theta and alpha)
       1.4. Determine the offset from a from which the solution starts
       1.5. Determine the candidate height y
       1.6. Determine the candidate beam start a

    2. Search neighborhood for solution
"""

import math
import sys

import intcode


def check(x, y):
    global puzzle

    result, *_ = intcode.Computer(puzzle).run(x, y)
    return result


if __name__ == "__main__":
    if any(arg in {"-t", "--test"} for arg in sys.argv):
        sys.exit(25)  # No tests

    else:
        puzzle = [int(x) for x in sys.stdin.read().split(",")]

        total = 0
        fst = 0
        for y in range(50):
            seen = False
            for x in range(fst, y + 1):
                if check(x, y):
                    total += 1
                    if not seen:
                        seen = True
                        fst = x

                elif seen:
                    break
        print(total)

        lo, hi = 0, 1e6
        while lo < hi:
            x = (lo + hi) / 2
            if check(x, 1e6 - 1):
                hi = x - 1
            else:
                lo = x + 1
        a = x

        lo, hi = a, 1e6
        while lo < hi:
            x = (lo + hi) / 2
            if check(x, 1e6 - 1):
                lo = x + 1
            else:
                hi = x - 1
        b = x

        theta = math.atan((a + 1) / 1e6)
        alpha = math.atan((b + 1) / 1e6)
        offset = math.floor(100 * math.tan(theta))
        y = math.floor((offset + 100) / (math.tan(alpha) - math.tan(theta)))
        a = math.floor(math.tan(theta) * y)

        neighborhood = (
            (i + offset, j) for j in range(y - 5, y + 5) for i in range(a - 5, a + 5)
        )

        for (x, y) in neighborhood:
            if check(x + 99, y) and check(x, y + 99):
                print(x * 10000 + y)
                break