with open('input.txt', 'r') as file:
    rows = file.read().splitlines()

nodes = {}
for row in rows:
    x, xs = row.split(':')
    xs = xs.strip().split(' ')
    nodes[x] = xs

cached_nodes={}

def traverse_all_paths(start, end, path=[]):
    ind = sum([1 for p in path if p == 'dac' or p == 'fft'])
    key = (start, ind)
    if key in cached_nodes:
        return cached_nodes[key]
    path = path + [start]    
    if start == end:        
        if 'dac' in path and 'fft' in path:
            return 1    
        else:
            return 0
    if start not in nodes:
        raise ValueError(f"Node {start} not in nodes")
    paths = 0
    for node in nodes[start]:
        if node in path:
            print("already visited", node)
            continue
        new_paths = traverse_all_paths(node, end, path)
        paths += new_paths
        cached_nodes[key] = paths
    return paths

start = 'svr'
end = 'out'
count = traverse_all_paths( start, end)
print("Total paths from", start, "to", end, ":", count)
