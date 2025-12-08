import math
import djset

with open('input.txt', 'r') as file:
    rows = list(map(lambda x: tuple(map(int,x.split(','))), file.read().splitlines()))

def dist2(a, b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2

nNodes = len(rows)
nodes = []
for i in range(nNodes-1):
    for j in range(i+1,nNodes):        
        nodes.append( (dist2(rows[i],rows[j]), i, j) )

nodes = sorted(nodes, key=lambda x: x[0])

ds = djset.DisjointSet()
for i in range(nNodes):
    ds.make_set(i)

count = 0
for (d, i, j) in nodes:
    count += 1
    if not ds.connected(i,j):
        print(f"{count}: {i} <--> {j}")
#        print(f"{count}: {rows[i]} <--> {rows[j]}")
        ds.union(i,j)
        print(sorted(ds.get_sets(), key=lambda x: len(x), reverse=True))
    if count == 1000:
        break

print("--------------------------")
print(sorted(ds.get_sets(), key=lambda x: len(x), reverse=True))
print(math.prod(map(len, sorted(ds.get_sets(), key=lambda x: len(x), reverse=True)[:3])))
    

        #print(f"union {i} {j} with dist {d}")
# [ {i} for i in range(nNodes) ] 

# for (d, i, j) in nodes:
#     if ! connected(i,j):


# stopAt = 500
# for i in range(stopAt+1):
#     print(f"---- {i}")
#     #print(i, connected)
#     gmind = float('inf')
#     s1_sel = -1
#     s2_sel = -1
#     for s1 in range(len(connected)-1):
#         for s2 in range(s1+1, len(connected)):
#             # find closest points between s1 and s2
#             mind = float('inf')
#             for n1 in connected[s1]:
#                 for n2 in connected[s2]:
#                     d = dm[n1][n2]
#                     if d < mind:
#                         mind = d
#             if mind < gmind:
#                 gmind = mind
#                 s1_sel = s1
#                 s2_sel = s2
#     # union s1_sel and s2_sel
#     new_connected = [ connected[ii] for ii in range(len(connected)) if ii != s1_sel if ii != s2_sel ]
#     new_connected.append( connected[s1_sel] | connected[s2_sel] )
#     connected = new_connected
#     print(list(sorted(connected, reverse=True, key=len)[:3]))
#     print(math.prod(len(c) for c in sorted(connected, reverse=True, key=len)[:3]))


# print("--------------------------")
# connectedSorted = sorted(connected, reverse=True, key=len)[:3]
# result = math.prod(len(c) for c in connectedSorted)
# print(result)