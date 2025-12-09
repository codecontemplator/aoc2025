with open('input.txt', 'r') as file:
    rows = list(map(lambda x: tuple(map(int,x.split(','))),file.read().splitlines()))

corners = [(rows[i],rows[j]) for i in range(len(rows)-1) for j in range(i+1,len(rows))]

def area(corner):
    return (1+abs(corner[1][0]-corner[0][0]))*(1+abs(corner[1][1]-corner[0][1]))

mc = max(corners, key=area)
print(area(mc))
