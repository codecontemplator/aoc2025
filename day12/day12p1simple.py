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

def part1(regions, present_areas):
    possible_count = 0

    for region in regions:
        region_area = region["width"] * region["height"]
        total_present_area = sum(count * present_areas[i] 
                                 for i, count in enumerate(region["presents"]))
        if total_present_area <= region_area:
            possible_count += 1

    return possible_count

with open('inputx.txt','r') as f:
    lines = f.read().splitlines()

shapes, puzzles = parse(lines)

shape_to_area = { i: sum([ row.count('#') for row in shape ]) for i, shape in enumerate(shapes) }

regions = [ {"width": w, "height": h, "presents": q} for (w,h), q in puzzles ]

# count = 0
# for (width, height), quantities in puzzles:    
#     max_area = width * height
#     total_shape_area = sum([ shape_to_area[i] * quantities[i] for i in range(len(shapes)) ])
#     print(max_area, total_shape_area)
#     if total_shape_area > max_area:
#         count += 1

# print(count)        

x = part1(regions, shape_to_area)
print(x)
