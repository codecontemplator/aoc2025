from collections import defaultdict
from itertools import combinations, product
import numbers
import dlx

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

def mk_shape_hash(shape):
    return "".join(["".join(row) for row in shape])

class ShapeCache:    
    def __init__(self, shapes):
        self.variants = defaultdict(list)
        for i, shape in enumerate(shapes):      
            unqiue_variants = set()  
            for r in range(4):
                for f in range(2):
                    variant = shape
                    if f == 1:
                        variant = flip(variant)
                    variant = rotatecw(variant, r)
                    variant_hash = mk_shape_hash(variant)
                    if variant_hash not in unqiue_variants:
                        self.variants[i].append(variant)
                        unqiue_variants.add(variant_hash)
            #print(f"shape {i} has {len(unqiue_variants)} variations")

    def get_variants(self, shape_index):
        return self.variants[shape_index]


class Solver:

    def __init__(self, shapes, board_width, board_height, quantities, shape_dim = 3):
        cache = ShapeCache(shapes)
        n_shapes = len(shapes)
        self.dlxsolver = dlx.DLX()
        board_columns = [ self.dlxsolver.add_column(f"cell{x}{y}", primary = False) for y in range(board_height) for x in range(board_width) ]
        shape_columns = [ self.dlxsolver.add_column(f"shape{i}", primary = True) for i in range(n_shapes) if quantities[i] > 0 ]

        row_count = 0
        shape_column = 0
        for shape_index in range(len(shapes)):
            variants = cache.get_variants(shape_index)
            quantity = quantities[shape_index]
            if quantity == 0:
                continue

            slots = [ (x, y) for y in range(board_height - shape_dim + 1) for x in range(board_width - shape_dim + 1) ]

            candidate_solutions = list(combinations(slots, quantity))
            for candidate_solution in candidate_solutions:
                if (len(candidate_solution) != quantity):
                    raise ValueError("invalid solution length")
                
                all_variant_assignments = list(product(range(len(variants)), repeat=len(candidate_solution)))                
                for variant_assignment in all_variant_assignments:
                    variant_pos_pair = list( zip(candidate_solution, variant_assignment) )  # [ ((x,y), variant_index), ... ]
                    row_board = [ 
                                (y + h) * board_width + (x + w) 
                                for (x,y), variant_index in variant_pos_pair
                                for h in range(shape_dim) 
                                for w in range(shape_dim) 
                                if variants[variant_index][h][w] == '#'
                    ]
                    row_board_no_duplicates = list(set(row_board)) 
                    if (len(row_board_no_duplicates) != len(row_board)):
                        continue  # overlapping shapes in this solution)

                    row = sorted(row_board + [ shape_column + len(board_columns) ])

                    self.dlxsolver.add_row(row, f"shape{shape_index}")  
                row_count += 1
            shape_column += 1


        print(f"DLX matrix: {len(board_columns) + len(shape_columns)} columns, {row_count} rows")

    def solve(self):
        solutions = self.dlxsolver.solve(max_solutions = 1)
        return len(solutions) > 0
    
with open('example.txt','r') as f:
    lines = f.read().splitlines()

shapes, puzzles = parse(lines)
num_unsolved = 0
for (width, height), quantities in puzzles:    
    print(f"puzzle: {width}x{height} {quantities}")
    solver = Solver(shapes, width, height, quantities)
    solution_found = solver.solve()
    if not solution_found:
        num_unsolved += 1
        print("  no solution found")
    else:
        print(f"  solution found")


print(num_unsolved)
