# AOC 2025 - Day 12

# idea: keep track of legal placements for all shapes with variants. when placing a shape re-evaluate the legal placements. 
# if one of the shapes that are left to place have no legal place left we reach a contradiction

import numbers


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

def rotatecw(grid, count):
    for _ in range(count):
        grid = rotate90cw(grid)
    return grid

def flip(grid):
    return grid[::-1]    

def to_binary(x):
    return sum([ 2**i for i, ch in enumerate(x) if ch == '#' ])

def from_binary(x, w = 64):
    return [ '#' if 2**i & x > 0 else '.' for i in range(w) ]

def print_shape(grid):    
    for j in range(len(grid)):
        v = grid[j]
        if isinstance(v, numbers.Number):
            v = from_binary(v, 3)
        print("".join(v))

class Board:
    def __init__(self, width, height, num_shapes, shape_cache, shape_dim = 3):
        self.shape_cache = shape_cache
        self.grid = [ 0 for _ in range(height) ]
        self.shape_dim = shape_dim
        self.width = width
        self.height = height
        all_shapes = [ 
            (shapeindex, (rotation, flip)) 
                for shapeindex in range(num_shapes)
                    for rotation in range(4)
                        for flip in range(2)            
            ]
        # in the beginning all shapes are candidates for all positions        
        self.candidates = [ [ all_shapes for _ in range(width-shape_dim+1)] for _ in range(height-shape_dim+1) ] 
        max_candidates = (width-shape_dim+1) * (height-shape_dim+1) * num_shapes * 4 * 2
        self.num_candidates = dict([ (shapeindex, max_candidates) for shapeindex in range(num_shapes) ])

    def debug_print(self, title):
        print("--------------------------", title)
        for j in range(self.height):
            x = from_binary(self.grid[j], self.width)
            s = "".join(x)
            print(s)
        print("--------------------------")

    def get_candidates_for_shape(self, shapes_to_place):
        nrows = len(self.candidates)
        ncols = len(self.candidates[0])
        assert(nrows == self.height-self.shape_dim+1)
        assert(ncols == self.width-self.shape_dim+1)
        return [
            ((i,j), (shapeindex, variant))
             for j in range(nrows)
                for i in range(ncols)
                    for (shapeindex, variant) in self.candidates[j][i]
                        if shapeindex == shapes_to_place
        ]
    
    def can_place_candidate(self, candidate):
        (i,j), (shapeindex, variant) = candidate
        shape = self.shape_cache.get(shapeindex, variant)
        for h in range(self.shape_dim):
            bits = shape[h] << i
            assert(bits > 0)
            gridrow = self.grid[h+j]
            if bits & gridrow > 0:
                return False
        return True

    def place_candidate(self, candidate):
        # precondition: enusre that it can be placed (we are placing a candidate so it should be possible)
        assert(self.can_place_candidate(candidate))
        # place!
        (pi,pj), (shapeindex, variant) = candidate
        shape = self.shape_cache.get(shapeindex, variant)
        #print("placing candidate shape ")
        #print_shape(shape)
        for h in range(self.shape_dim):
            bits = shape[h] << pi
            assert(bits > 0)
            self.grid[h+pj] |= bits
        undo_candidates = {}
        # remove invalidated candidates, check all overlapping tiles        
        for j in range(max(0, pj-self.shape_dim), min(self.height-self.shape_dim+1, pj+self.shape_dim)):
            for i in range(max(0, pi-self.shape_dim), min(self.width-self.shape_dim+1, pi+self.shape_dim)):     
                pos = (i,j)
                original_candidates = self.candidates[j][i]
                new_candidates = [ candidate for candidate in original_candidates if self.can_place_candidate((pos,candidate)) ]
                self.candidates[j][i] = new_candidates
                undo_candidates[pos] = original_candidates
        # return undo info
        return (candidate, undo_candidates)


    def unplace_candidate(self, undo):
        candidate, undo_candidates = undo
        (pi,pj), (shapeindex, variant) = candidate
        shape = self.shape_cache.get(shapeindex, variant)
        for h in range(self.shape_dim):
            bits = shape[h] << pi
            self.grid[h+pj] &= ~bits
        
        # restore candidates
        for pos, original_candidates in undo_candidates.items():
            i, j = pos
            self.candidates[j][i] = original_candidates
    
class PresentsToPlace:
    def __init__(self, shape_counters):
        self.shape_counters = shape_counters

    def shapes(self):
        return [ index for index,count in enumerate(self.shape_counters) if count > 0 ]
    
    def add(self, shapeindex):
        self.shape_counters[shapeindex] += 1

    def subtract(self, shapeindex):
        self.shape_counters[shapeindex] -= 1


def search(board, presents_to_place):

    #print("--------- search")
    shapes_to_place = presents_to_place.shapes()
    #print(f"shapes to place", shapes_to_place)
    if len(shapes_to_place) == 0:
        return board # nothing more to place, we were successful
        
    for shape_to_attempt_to_place in shapes_to_place:
        #print(f"trying to place {shape_to_attempt_to_place}")
        presents_to_place.subtract(shape_to_attempt_to_place)
        candidates = board.get_candidates_for_shape(shape_to_attempt_to_place)
        for candidate in candidates:
            #board.debug_print("before")
            undo = board.place_candidate(candidate)  # TODO: we can detect if this placement causes contraditions here and move on with searching further
            #board.debug_print("after")
            result = search(board, presents_to_place)
            if result is not None:
                return result   # success
            board.unplace_candidate(undo)
        presents_to_place.add(shape_to_attempt_to_place)

    return None # no candidate was successful


class ShapeCache:    
    def __init__(self, shapes):
        self.cache = {}
        for i, shape in enumerate(shapes):
            for r in range(4):
                self.cache[(i,(r,0))] = list(map(to_binary, rotatecw(shape, r)))
            for r in range(4):
                self.cache[(i,(r,1))] = list(map(to_binary, rotatecw(flip(shape), r)))

    def get(self, shapeindex, variant):
        return self.cache[(shapeindex, variant)]

with open('example.txt','r') as f:
    lines = f.read().splitlines()

shapes, puzzles = parse(lines)
shapeCache = ShapeCache(shapes)
num_shapes = len(shapes)
num_unsolved = 0
for (width, height), quantities in [puzzles[1]]:    
    print(f"puzzle: {width}x{height} {quantities}")
    board = Board(width, height, num_shapes, shapeCache)
    presents_to_place = PresentsToPlace(quantities)
    result = search(board, presents_to_place) 
    if result is None:
        num_unsolved += 1
    else:
        result.debug_print("solution")


print(num_unsolved)