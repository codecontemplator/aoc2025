import math


with open('input.txt', 'r') as f:
    lines = f.read().splitlines()

ops = lines.pop().split()
matrix = list(map(lambda r: list(map(int, r.split())), lines))

#print(matrix)
transposed = [list(row) for row in zip(*matrix)]
#print(transposed)

def calc(row):
    op, data = row
    match op:
        case '+': 
            return sum(data)
        case '*':
            return math.prod(data)
        
calcs = list(zip(ops, transposed))
print(sum(map(calc, calcs)))

# ncols = len(agg)
# nrows = len(lines)

# for j in range(nrows):
#     for i in range(ncols):
#         agg[i] += ops[j]
#         agg[i] += lines[j][i]


