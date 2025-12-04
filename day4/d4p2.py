with open('input.txt', 'r') as file:
    rows = list(map(list, file.read().splitlines()))

height = len(rows)
width = len(rows[0])

deltas = [ 
        (dx,dy) for dx in [-1,0,1] 
        for dy in [-1,0,1] 
        if not (dx == 0 and dy == 0) 
    ]

def single_round():
    frees = []
    for y in range(height):
        for x in range(width):
            if rows[y][x] == '@':
                ns = sum([ 
                        1
                        for (dx,dy) in deltas
                        if 0 <= x+dx < width and 0 <= y+dy < height                    
                        if rows[y+dy][x+dx] == '@'
                    ])
                if ns < 4:
                    frees.append( (x,y) )
    return frees

removed = 0
while True:
    frees = single_round()
    if len(frees) == 0:
        break
    removed += len(frees)
    for (x,y) in frees:
        rows[y][x] = '.'

print(removed)