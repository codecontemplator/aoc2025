with open('input.txt', 'r') as file:
    rows = file.read().splitlines()

nodes = {}
for row in rows:
    x, xs = row.split(':')
    xs = xs.strip().split(' ')
    nodes[x] = xs

cached_nodes={}

def traverse_all_paths(start, end, path=[]):
    if start in cached_nodes:
        return cached_nodes[start]
    path = path + [start]    
    if start == end:        
        return 1    
    if start not in nodes:
        raise ValueError(f"Node {start} not in nodes")
    #paths = []
    paths = 0
    for node in nodes[start]:
        if node in path:
            print("already visited", node)
            continue

        #new_paths = traverse_all_paths(node, end, path)
        new_paths = traverse_all_paths(node, end, path)
        paths += new_paths
        cached_nodes[start] = paths
        #for new_path in new_paths:
        #    paths.append(new_path)
    return paths

start = 'you'
end = 'out'
count = traverse_all_paths( start, end)
print("Total paths from", start, "to", end, ":", count)
