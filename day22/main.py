import numpy as np


def build_polynomial(functions, N):
    a, b = 1, 0
    for f in functions:
        if f[0] == 0:
            a *= -1
            b = - 1 - b
        elif f[0] == 1:
            a = a * f[1]
            b = b * f[1]
        elif f[0] == 2:
            b = b - f[1]
    return a, b


def build_inverse_polynomial(functions, N):
    a, b = 1, 0
    for f in functions[::-1]:
        if f[0] == 0:
            a *= -1
            b = - 1 - b
        elif f[0] == 1:
            inv = pow(f[1], -1, N)
            a = a * inv
            b = b * inv
        elif f[0] == 2:
            b = b + f[1]
    return a, b

def polypow(a,b,m,n):
    if m==0:
        return 1,0
    if m%2==0:
        return polypow(a*a%n, (a*b+b)%n, m//2, n)
    else:
        c,d = polypow(a,b,m-1,n)
        return a*c%n, (a*d+b)%n


N = 119315717514047
num_iterations = 101741582076661
functions = []
with open('input') as f:
    for line in f.readlines():
        if line.startswith("deal into"):
            functions.append((0, None))
        elif line.startswith("deal with"):
            functions.append((1, int(line.strip().split(' ')[-1])))
        else:
            functions.append((2, int(line.strip().split(' ')[-1])))
idx = 2020
a, b = build_polynomial(functions, N)
x, y = build_inverse_polynomial(functions, N)


x2, y2 = polypow(x,y,num_iterations, N)

y = (2020*x2 + y2) % N
print(y)