class DisjointSet:
    def __init__(self):
        self.parent = {}
        self.rank = {}
        self.count = 0   # number of disjoint sets (always initialized)

    def make_set(self, x):
        """Create a new set with element x."""
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
            self.count += 1

    def find(self, x):
        """Find representative with path compression."""
        if x not in self.parent:
            raise KeyError(f"{x} is not present. Call make_set(x) first.")
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        """Union by rank; returns True if merged, False if already same set."""
        # If user passes unknown elements, raise — keeps behavior explicit.
        rootX = self.find(x)
        rootY = self.find(y)

        if rootX == rootY:
            return False

        if self.rank[rootX] < self.rank[rootY]:
            self.parent[rootX] = rootY
        elif self.rank[rootX] > self.rank[rootY]:
            self.parent[rootY] = rootX
        else:
            self.parent[rootY] = rootX
            self.rank[rootX] += 1

        self.count -= 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)

    def num_sets(self):
        """Return the number of disjoint sets (fast, O(1))."""
        return self.count

    def get_sets(self):
        """Return all disjoint sets as a list of lists."""
        groups = {}

        # Ensure path compression first (optional but makes groups cleaner)
        for x in self.parent:
            root = self.find(x)
            groups.setdefault(root, []).append(x)

        return list(groups.values())