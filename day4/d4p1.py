with open('input.txt', 'r') as file:
    content = file.read().splitlines()

height = len(content)
width = len(content[0])

deltas = [ 
        (dx,dy) for dx in [-1,0,1] 
        for dy in [-1,0,1] 
        if not (dx == 0 and dy == 0) 
    ]

frees = []
for y in range(height):
    for x in range(width):
        if content[y][x] == '@':
            ns = sum([ 
                    1
                    for (dx,dy) in deltas
                    if 0 <= x+dx < width and 0 <= y+dy < height                    
                    if content[y+dy][x+dx] == '@'
                ])
            if ns < 4:
                frees.append( (x,y) )

print(len(frees))