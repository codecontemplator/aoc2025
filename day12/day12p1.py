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

def rotatecw(grid, count):
    for _ in range(count):
        grid = rotate90cw(grid)
    return grid

def flip(grid):
    return grid[::-1]    

def to_binary(list):
    return sum([ 2**i for i, ch in enumerate(list) if ch == '#' ])

def print_shape(grid):    
    for j in range(len(grid)):
        print(grid[j])

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
            bits = shape[h] >> i
            gridrow = self.grid[h+j]
            if bits & gridrow > 0:
                return False
        return True

    def place_candidate(self, candidate):
        # precondition: enusre that it can be placed (we are placing a candidate so it should be possible)
        assert(self.can_place_candidate(candidate))
        # place!
        (i,j), (shapeindex, variant) = candidate
        shape = self.shape_cache.get(shapeindex, variant)
        for h in range(self.shape_dim):
            bits = shape[h] >> i
            self.grid[h+j] |= bits
        undo_candidates = {}
        # remove invalidated candidates, check all overlapping tiles        
        for h in range(self.shape_dim):
            for w in range(self.shape_dim):
                jj = j - h
                ii = i - w
                if jj < 0 or ii < 0:
                    continue
                original_candidates = self.candidates[jj][ii]
                pos = (ii,jj)
                new_candidates = [ candidate for candidate in original_candidates if self.can_place_candidate((pos,candidate)) ]
                self.candidates[jj][ii] = new_candidates
                undo_candidates[pos] = original_candidates
        # return undo info
        return (candidate, undo_candidates)



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
        presents_to_place.subtract(shape_to_attempt_to_place)
        candidates = board.get_candidates_for_shape(shape_to_attempt_to_place)
        for candidate in candidates:
            board.place_candidate(candidate)  # TODO: we can detect if this placement causes contraditions here and move on with searching further
            result = search(board, presents_to_place)
            if result == True:
                return True   # success
            board.unplace_candidate(candidate)
        presents_to_place.add(shape_to_attempt_to_place)

    return False # no candidate was successful


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
for (width, height), quantities in [puzzles[0]]:    
    print(f"puzzle: {width}x{height} {quantities}")
    board = Board(width, height, num_shapes, shapeCache)
    presents_to_place = PresentsToPlace(quantities)
    result = search(board, presents_to_place) 
    if not result:
        num_unsolved += 1


print(num_unsolved)