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

fi = -1
fj = -1
for (d, i, j) in nodes:
    if not ds.connected(i,j):
        ds.union(i,j)
        if ds.num_sets() == 1:
            fi = i
            fj = j
            break

print(rows[fi][0] * rows[fj][0])



