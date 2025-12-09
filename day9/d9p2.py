def get_intervals(corners):
    ycs = sorted(corners, key=lambda x: x[1])

    pairs = list(zip(ycs[::2], ycs[1::2]))

    intervals = []
    for p in pairs: 
        (c1,c2) = p
        if c1[1] != c2[1]:
            raise ValueError("Unexpected y-coordinates")
        iv = min(c1[0],c2[0]), max(c1[0],c2[0])
        intervals.append((c1[1], iv))

    return intervals

def fill(intervals):
    (yc, (xmin, xmax))  = intervals.pop(0)

    result = [(yc, (xmin, xmax))]
    while True:
        if not intervals:
            break
        
        (y_next, (xmin_next, xmax_next)) = intervals.pop(0)
        for y in range(yc+1, y_next):
            result.append((y, (xmin, xmax)))
        yc = y_next
        if xmin_next < xmin:
            xmin = xmin_next
        else:
            
        xmin = min(xmin, xmin_next)
        xmax = max(xmax, xmax_next)
        result.append((yc, (xmin, xmax)))

    return result

with open('example.txt', 'r') as file:
    corners = list(map(lambda x: tuple(map(int,x.split(','))),file.read().splitlines()))

intervals = get_intervals(corners)
filled = fill(intervals)

for iv in filled:
    print(iv)


"""
print(yc)    

yranges = []

c1 = yc.pop(0)
c2 = yc.pop(0)
if c1[1] != c2[1]:
    raise ValueError("Unexpected y-coordinates")
y = 
(xmin,xmax) = (min(c1[0],c2[0]),max(c1[0],c2[0]))
for c in yc:
"""