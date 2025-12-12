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

def search(shapes_to_place):
    shape_to_place = shapes_to_place.select_by_min_available_cancidates()
    if shape_to_place is None:
        return True # no more shapes to place, we were successful
    
    candidates = get_candidates_for_shape(shape_to_place)
    if len(candidates) == 0:
        return False # no avaialbe position

    for candidate in candidates:
        place(candidate)
        result = search(...)
        if result == True:
            return True   # success
        unplace(candidate)

    return False # no candidate was successful

# contradictions: min num horizontal/vertical bits to place less than available horitzontal/vertical bits left
# idea: keep track of legal placements for all shapes with variants. when placing a shape re-evaluate the legal placement. if one of the shapes that are left to place have no legal place left we reach a contradiction

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