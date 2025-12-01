from functools import reduce


def fold_step(acc, step):
    pos, zeros = acc
    direction, value = step
    new_pos = (pos + value) % 100 if direction == "R" else (pos - value) % 100
    new_zeros = zeros + (1 if new_pos == 0 else 0)
    return (new_pos, new_zeros)


with open("input.txt", "r") as f:
    lines = f.read().splitlines() 

steps = [(line[0], int(line[1:])) for line in lines]
start = (50, 0)
final_pos, zero_count = reduce(fold_step, steps, start)
print(final_pos, zero_count)
