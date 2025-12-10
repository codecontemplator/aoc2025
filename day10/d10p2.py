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

# 196, 156
total_sum = 0
rowcnt = 0
for (btns, goal) in parsed_rows:
    rowcnt += 1
    #if rowcnt != 156 and rowcnt != 196:
    #    print("skipping")
    #    continue;
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
        
        # Smart approach: use linear programming to minimize sum
        # We want to minimize: sum(particular + null_space @ params)
        # Subject to: all elements of (particular + null_space @ params) >= 0
        # And all elements must be integers
        
        from scipy.optimize import linprog
        
        # Objective: minimize sum of all button presses
        # This is: minimize 1^T * (particular + null_space @ params)
        #        = minimize (1^T @ null_space) @ params  (constant term doesn't affect optimization)
        c = numpy.sum(null_space, axis=0)  # coefficients for minimization
        
        # Constraints: particular + null_space @ params >= 0
        # Rewritten as: -null_space @ params <= particular
        A_ub = -null_space
        b_ub = particular
        
        # Solve the LP relaxation first to get a good starting point
        result = linprog(c, A_ub=A_ub, b_ub=b_ub, method='highs')
        
        if result.success:
            # Now search around the LP solution for integer solutions
            lp_params = result.x
            
            # Try a small grid search around the LP solution
            from itertools import product
            search_radius = 10
            
            # Round LP solution and search around it
            base_params = numpy.round(lp_params).astype(int)
            
            for offsets in product(range(-search_radius, search_radius + 1), repeat=n_params):
                param_values = base_params + numpy.array(offsets)
                concrete_sol = particular + null_space @ param_values
                
                # Check if all values are non-negative integers (or close to integers)
                if numpy.all(numpy.abs(concrete_sol - numpy.round(concrete_sol)) < 0.001):
                    int_sol = numpy.round(concrete_sol).astype(int)
                    if numpy.all(int_sol >= 0):
                        sol_sum = int(numpy.sum(int_sol))
                        if sol_sum < min_sum:
                            min_sum = sol_sum
                            best_solution = int_sol.tolist()
        
        if best_solution is not None:
            print(f"Best solution: {best_solution}, sum: {min_sum}")
            total_sum += min_sum
        else:
            print(f"WARNING: No valid solution found with LP approach!")
            # Fallback to small brute force search
            from itertools import product
            for param_values in product(range(-5, 6), repeat=n_params):
                concrete_sol = particular + null_space @ numpy.array(param_values, dtype=float)
                if numpy.all(numpy.abs(concrete_sol - numpy.round(concrete_sol)) < 0.001):
                    int_sol = numpy.round(concrete_sol).astype(int)
                    if numpy.all(int_sol >= 0):
                        sol_sum = int(numpy.sum(int_sol))
                        if sol_sum < min_sum:
                            min_sum = sol_sum
                            best_solution = int_sol.tolist()
            
            if best_solution is not None:
                print(f"Fallback solution: {best_solution}, sum: {min_sum}")
                total_sum += min_sum
            else:
                print(f"ERROR: Could not find any valid solution!")
    else:
        # Unique solution
        print(f"Unique solution: {sol_vec}, sum: {sum(sol_vec)}")
        total_sum += sum(sol_vec)
    #a, residuals, rank, s = numpy.linalg.lstsq(MT, b, rcond=None)   
    

#print(parsed_rows)
#a, residuals, rank, s = numpy.linalg.lstsq(M, b, rcond=None)

print(total_sum)

# 20247  
# 164
# 337

# too high

# 20584
# too high