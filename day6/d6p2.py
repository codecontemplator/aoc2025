# import math
import math
import re


with open('input.txt', 'r') as f:
    lines = f.read().splitlines()

ops = lines.pop()

matches = [m.start()-1 for m in re.finditer(r"[+*]", ops) if m.start() > 0]
#print(matches)


def split_and_skip(s, indices):
    idx = sorted(set(indices))
    parts = []
    prev = 0

    for i in idx:
        parts.append(s[prev:i])  # part before the cut
        prev = i + 1             # skip the char at index i

    parts.append(s[prev:])        # remainder
    return parts

matrix = []
for line in lines:
    matrix.append(split_and_skip(line, matches))

def f2(ss, i):
    result = int("".join([ s[i] for s in ss if s[i] != ' ']))
    #print(result)
    return result

def f(ss):
    result = []
    for i in range(len(ss[0])):
        result.append(f2(ss, i))
    return result

transposed = [list(row) for row in zip(*matrix)]
transposed = list(map(f, transposed))

calcs = list(zip(ops.split(), transposed))
print(calcs)

def calc(row):
    op, data = row
    match op:
        case '+': 
            return sum(data)
        case '*':
            return math.prod(data)

print(sum(map(calc, calcs)))

