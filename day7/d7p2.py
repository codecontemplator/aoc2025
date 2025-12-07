from functools import lru_cache

with open('input.txt', 'r') as f:
    rows = list(map(list, f.read().splitlines()))

ncols = len(rows[0])
nrows = len(rows)

@lru_cache(maxsize=None)
def count(pos):
    row,i = pos
    if row == nrows:
        return 0
    cur = rows[row]
    if cur[i] == '^':
        return 1 + count((row+1,i-1)) + count((row+1,i+1)) 
    else:
        return count((row+1,i))

istart = rows[0].index('S')
splits = count((1,istart))
print(splits+1)
