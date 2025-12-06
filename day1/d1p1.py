from itertools import accumulate

def next(current_pos, step):
    direction, value = step
    sign = 1 if direction == "R" else -1
    return (current_pos + sign * value) % 100

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

steps = [(line[0], int(line[1:])) for line in lines]
positions = accumulate(steps, func=next, initial=50)
zero_count = sum(1 for pos in positions if pos == 0)

print(zero_count)
