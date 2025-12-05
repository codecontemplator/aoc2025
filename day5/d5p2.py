with open('input.txt', 'r') as file:
    content = file.read().splitlines()
    
sep = content.index('')    
intervals = [tuple(map(int, interval.split('-'))) for interval in content[:sep]]


intervals = sorted(intervals, key=lambda x: x[0]) 


result = []
startC, endC = intervals.pop(0)
    
for start, end in intervals:
    if start <= endC:
        endC = max(endC, end)
    else:
        result.append((startC, endC))
        startC, endC = start, end

result.append((startC, endC))

r = 0
for x in result:
    r += (x[1] - x[0]) + 1


print(r)


