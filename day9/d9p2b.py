def area(rectangle):
    return (1+abs(rectangle[1][0]-rectangle[0][0]))*(1+abs(rectangle[1][1]-rectangle[0][1]))

def make_intervals(corners):
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

    return intervals

def is_covered(rectangle, intervals):
    (c1, c2) = rectangle
    x1, y1 = c1
    x2, y2 = c2
    ymin, ymax = sorted([y1, y2])
    xmin, xmax = sorted([x1, x2])

    for y in range(ymin, ymax + 1):
        if y not in intervals:
            return False
        (int_xmin, int_xmax) = intervals[y]
        if int_xmin > xmin or int_xmax < xmax:
            return False

    return True

with open('input.txt', 'r') as file:
    corners = list(map(lambda x: tuple(map(int,x.split(','))),file.read().splitlines()))

corners.append(corners[0])  # Close the loop
intervals = make_intervals(corners)
rectangles = [(corners[i],corners[j]) for i in range(len(corners)-1) for j in range(i+1,len(corners))]

#covered_rectangles = [r for r in rectangles if is_covered(r, intervals)]    
covered_rectangles = []
i = 0
for r in rectangles:
    i += 1
    if i % 1000 == 0:
        print(f"{i} / {len(rectangles)}")
    if is_covered(r, intervals):
        covered_rectangles.append(r)

mr = max(covered_rectangles, key=area)
print(area(mr))

#1516172795