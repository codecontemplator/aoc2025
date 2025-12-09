with open('example.txt', 'r') as file:
    corners = list(map(lambda x: tuple(map(int,x.split(','))),file.read().splitlines()))

corners.append(corners[0])  # Close the loop

# corner_pairs = list(zip(corners[::2], corners[1::2]))
corner_pairs = list(zip(corners, corners[1:]))

intervals = {}
for c1,c2 in corner_pairs:
    x1, y1 = c1
    x2, y2 = c2
    if x1 == x2:  # Vertical line
        ymin, ymax = sorted([y1, y2])
        for y in range(ymin, ymax + 1):
            if y not in intervals:
                intervals[y] = (x1, x1)
            else:
                (xmin, xmax) = intervals[y]
                intervals[y] = (min(xmin, x1), max(xmax, x1))
    elif y1 == y2:  # Horizontal line
        y = y1
        xmin, xmax = sorted([x1, x2])
        if y not in intervals:
            intervals[y] = (xmin, xmax)
        else:
            (cur_xmin, cur_xmax) = intervals[y]
            intervals[y] = (min(cur_xmin, xmin), max(cur_xmax, xmax))
    else:
        raise ValueError("Only horizontal or vertical lines are supported")
    
for y in range(9):
    tmp = 14 * '.'
    if y in intervals:
        (xmin, xmax) = intervals[y]
        tmp = list(tmp)
        for x in range(xmin, xmax + 1):
            tmp[x] = '#'
        tmp = ''.join(tmp)
    print(tmp)
