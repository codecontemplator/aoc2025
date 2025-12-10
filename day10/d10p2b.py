import numpy 
import sympy as sp

with open('input.txt', 'r') as f:
    rows = f.read().splitlines()

def parse_btn(s):
    return  list(map(int,s.strip("()").split(",")))

def parse_goal(s):
    goal = 0
    for i in range(len(s)):
        if s[i] == '#':
            goal += 2**i
    return goal

def parse_row(s):
    i1 = s.index("]") + 1
    i2 = s.index("{") - 1
    p1 = s[1:i1-1]
    p2 = s[i1+1:i2]
    p3 = s[i2+2:-1]
    p1f = parse_goal(p1)
    p2f = list(map(parse_btn, p2.split(" ")))
    p3f = list(map(int,p3.split(",")))
    return (p2f, p3f )  # btns, goal

def to_matrix(btns, dim):
    M = []
    for btn in btns:
        r = [ 0 for i in range(dim) ]
        for i in btn:
            r[i] = 1
        M.append(r)
    return M

parsed_rows = [ parse_row(row) for row in rows ]

total_sum = 0
rowcnt = 0
for (btns, goal) in parsed_rows:
    rowcnt += 1
   # if rowcnt < 157:
  #      continue;
    print(f"{rowcnt} / {len(parsed_rows)}")

    M = to_matrix(btns, len(goal))
    M2 = sp.Matrix(M).transpose()
    b2 = sp.Matrix(goal)
    sol_vec, params = M2.gauss_jordan_solve(b2)
    
    # Find the smallest solution by trying different parameter values
    if params:
        min_sum = float('inf')
        best_solution = None
        
        # Convert sympy solution to numpy for faster computation
        # Extract the particular solution and null space vectors
        n_params = len(params)
        n_vars = len(sol_vec)
        
        # Get particular solution (all params = 0)
        particular = numpy.array([float(val) for val in sol_vec.subs(dict(zip(params, [0]*n_params)))], dtype=float)
        
        # Get null space basis vectors (coefficient of each parameter)
        null_space = []
        for i, param in enumerate(params):
            param_vals = [1 if j == i else 0 for j in range(n_params)]
            vec = numpy.array([float(sol_vec[j].subs(dict(zip(params, param_vals)))) - particular[j] 
                              for j in range(n_vars)], dtype=float)
            null_space.append(vec)
        null_space = numpy.array(null_space).T  # Shape: (n_vars, n_params)
        
        # Use a limited search range to keep it fast, but increase if needed
        search_range = 5  # Start with small range
        max_search_range = 200  # Maximum range to try
        
        from itertools import product
        
        while best_solution is None and search_range <= max_search_range:
            param_ranges = [range(-search_range, search_range + 1) for _ in params]
            
            for param_values in product(*param_ranges):
                # Fast numpy computation: particular + null_space @ param_values
                concrete_sol = particular + null_space @ numpy.array(param_values, dtype=float)
                
                # Check if all values are non-negative integers (or close to integers)
                if numpy.all(numpy.abs(concrete_sol - numpy.round(concrete_sol)) < 0.001):
                    int_sol = numpy.round(concrete_sol).astype(int)
                    if numpy.all(int_sol >= 0):
                        sol_sum = int(numpy.sum(int_sol))
                        if sol_sum < min_sum:
                            min_sum = sol_sum
                            best_solution = int_sol.tolist()
            
            if best_solution is None:
                print(f"No solution found with range {search_range}, increasing to {search_range * 2}...")
                search_range *= 2
        
        if best_solution is not None:
            print(f"Best solution: {best_solution}, sum: {min_sum}")
            total_sum += min_sum
        else:
            print(f"WARNING: No valid solution found even with search range {max_search_range}!")
            # Could skip this row or handle differently
    else:
        # Unique solution
        print(f"Unique solution: {sol_vec}, sum: {sum(sol_vec)}")
        total_sum += sum(sol_vec)
    #a, residuals, rank, s = numpy.linalg.lstsq(MT, b, rcond=None)   
    

#print(parsed_rows)
#a, residuals, rank, s = numpy.linalg.lstsq(M, b, rcond=None)

print(total_sum)