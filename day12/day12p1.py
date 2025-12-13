# AOC 2025 - Day 12

# idea: keep track of legal placements for all shapes with variants. when placing a shape re-evaluate the legal placements. 
# if one of the shapes that are left to place have no legal place left we reach a contradiction

def parse_region(line):
    dims_raw, quantities_raw = line.split(":")
    dims = tuple(map(int, dims_raw.split("x")))
    quantities = list(map(int,quantities_raw.split()))
    return dims, quantities

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

def flip(grid):
    return grid[::-1]    

# def mirror_lr(grid):
#     return [row[::-1] for row in grid]    
    
# def mirror_tb(grid):
#     return grid[::-1]    


def print_shape(grid):    
    for j in range(len(grid)):
        print(grid[j])

class Board:
    def __init__(self, width, height, num_shapes, shape_dim = 3):
        self.width = width
        self.height = height
        all_shapes = [ 
            (shapeindex, rotation, variant) 
                for shapeindex in range(num_shapes)
                    for rotation in range(4)
                        for variant in range(2)            
            ]
        # in the beginning all shapes are candidates for all positions        
        self.candidates = [ [ all_shapes for _ in range(width-shape_dim+1)] for _ in range(height-shape_dim+1) ] 
        max_candidates = (width-shape_dim+1) * (height-shape_dim+1) * num_shapes * 4 * 2
        self.num_candidates = dict([ (shapeindex, max_candidates) for shapeindex in range(num_shapes) ])

    def get_candidates_for_shape(self, shapes_to_place):
        return sorted(shapes_to_place, key=lambda shapeindex: self.num_candidates[shapeindex])[0]
                
class PresentsToPlace:
    def __init__(self, shape_counters):
        self.shape_counters = shape_counters

    def shapes(self):
        return [ shapeindex for shapeindex in self.shape_counters if self.shape_counters[shapeindex] > 0 ]
    
    def add(self, shapeindex):
        self.shape_counters[shapeindex] += 1

    def subtract(self, shapeindex):
        self.shape_counters[shapeindex] -= 1


def search(board, presents_to_place):

    shapes_to_place = presents_to_place.shapes()
    if len(shapes_to_place) == 0:
        return True # nothing more to place, we were successful

    for shape_to_attempt_to_place in shapes_to_place:
        presents_to_place.subract(shape_to_attempt_to_place)
        candidates = board.get_candidates_for_shape(shape_to_attempt_to_place)
        for candidate in candidates:
            undo = board.place_candidate(candidate)  # TODO: we can detect if this placement causes contraditions here and move on with searching further
            result = search(board, presents_to_place)  # this does not work
            if result == True:
                return True   # success
            presents_to_place.add()
            board.undo(undo)
        presents_to_place.add(shape_to_attempt_to_place)

    return False # no candidate was successful


with open('example.txt','r') as f:
    lines = f.read().splitlines()

shapes, puzzles = parse(lines)
# TODO: we want to create a dictionary (shapeindex, rotation, variant) -> shape as a "global" static data block
num_shapes = len(shapes)
num_unsolved = 0
for (width, height), quantities in puzzles:    
    board = Board(width, height, num_shapes)
    presents_to_place = PresentsToPlace(quantities)
    result = search(board, presents_to_place) 
    if not result:
        num_unsolved += 1


