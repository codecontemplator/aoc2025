from itertools import accumulate

with open("input.txt", "r") as f:
    lines = f.read().splitlines() 

steps = [(line[0], int(line[1:])) for line in lines]

zero_count = 0
pos = 50
for step in steps:
    direction, value = step    
    sign = 1 if direction == "R" else -1    
    new_pos = (pos + sign * value) % 100
    if new_pos == 0:
        zero_count += 1
    pos = new_pos    

print(zero_count)
