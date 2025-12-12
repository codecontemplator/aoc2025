def parse_region(line):
    dims_raw, quantities_raw = line.split(":")
    dims = tuple(map(int, dims_raw.split("x")))
    qauntities = list(map(int,quantities_raw.split()))
    return dims, qauntities

def parse_shape(lines):
    lines.pop(0)
    return list(map(list,lines))

def parse(lines):
    groups = []
    cg = []
    for line in lines:
        if len(line) == 0:
            groups.append(cg)
            cg = []
        else:
            cg.append(line)

    groups.append(cg)
    regions = groups.pop()
    return list(map(parse_shape,groups)), list(map(parse_region, regions))

def rotate90cw(grid):
    return [list(row) for row in zip(*grid[::-1])]

def mirror_lr(grid):
    return [row[::-1] for row in grid]    
    
def mirror_tb(grid):
    return grid[::-1]    

def print_shape(grid):    
    for j in range(len(grid)):
        print(grid[j])

with open('example.txt','r') as f:
    lines = f.read().splitlines()




shapes, regions = parse(lines)
print_shape(shapes[0])
print("------------")
print_shape(rotate90cw(shapes[0]))
print("------------")
print_shape(mirror_lr(shapes[0]))
print("------------")
print_shape(mirror_tb(shapes[0]))
print("------------")

#print_shape(shapes[0])
#print_shape(shapes[1])