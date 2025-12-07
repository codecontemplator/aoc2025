with open('input.txt', 'r') as f:
    rows = list(map(list, f.read().splitlines()))

ncols = len(rows[0])
nrows = len(rows)

def step(prev, cur):
    res = list(cur)
    splits = 0
    for i in range(ncols):
        if prev[i] == 'S':
            res[i] = '|'
        elif prev[i] == '|' and cur[i] == '.':
            res[i] = '|'
        elif prev[i] == '|' and cur[i] == '^':
            res[i-1] = '|'
            res[i+1] = '|'
            splits += 1
    return (splits, res)

res = [rows[0]]
gsplits = 0
for i in range(1, nrows):
    splits, next = step(res[-1], rows[i])
    res.append(next)
    gsplits += splits

#for x in res:
#    print(x)

print(gsplits)
# print(len(list(filter(lambda x: x == '|', res[-1]))))

