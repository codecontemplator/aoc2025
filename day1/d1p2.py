from itertools import accumulate

with open("day1/input.txt", "r") as f:
    lines = f.read().splitlines() 

steps = [(line[0], int(line[1:])) for line in lines]

zero_count = 0
pos = 50
for step in steps:
    print(step)
    direction, value = step    
    zero_add = 0
    zero_add += value // 100
    sign = 1 if direction == "R" else -1
    new_pos = (pos + sign * value) % 100
    if new_pos == 0 and pos != 0:
        zero_add += 1
        print("hit zero exactly")
    elif sign == 1 and new_pos < pos and pos != 0:
        zero_add += 1
        print("passed zero going right")
    elif sign == -1 and new_pos > pos and pos != 0:
        zero_add += 1
        print("passed zero going left")
    print("step:", step, "from", pos, "to", new_pos, "zero_count:", zero_add)
    pos = new_pos 
    zero_count += zero_add

print(zero_count)
