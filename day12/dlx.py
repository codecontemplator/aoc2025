"""
Dancing Links Algorithm (DLX) - Donald Knuth's Algorithm X implementation
for solving exact cover problems.
"""


class Node:
    """Represents a cell in the dancing links matrix."""
    
    def __init__(self):
        self.left = self
        self.right = self
        self.up = self
        self.down = self
        self.col = None  # Reference to column header
        self.row_id = None  # Optional: identifier for the row


class Column:
    """Column header node with additional metadata."""
    
    def __init__(self, name=None, primary=True):
        self.node = Node()
        self.node.col = self
        self.name = name
        self.size = 0  # Number of nodes in this column
        self.primary = primary  # True: must be covered exactly once, False: may be covered 0 or 1 times


class DLX:
    """Dancing Links solver for exact cover problems."""
    
    def __init__(self):
        self.header = Column("header")
        self.header.node.col = self.header
        self.columns = []
        self.solutions = []
        self.current_partial = []
    
    def add_column(self, name=None, primary=True):
        """
        Add a new column to the matrix.
        
        Args:
            name: Optional name for the column
            primary: True if column must be covered exactly once (default),
                    False if column may be covered 0 or 1 times
        """
        col = Column(name, primary=primary)
        # Insert after header (before header.node.right)
        col.node.right = self.header.node.right
        col.node.left = self.header.node
        self.header.node.right.left = col.node
        self.header.node.right = col.node
        self.columns.append(col)
        return col
    
    def add_row(self, col_indices, row_id=None):
        """
        Add a row to the matrix.
        
        Args:
            col_indices: List of column indices that have 1s in this row
            row_id: Optional identifier for this row
        """
        if not col_indices:
            return
        
        nodes = []
        for col_idx in col_indices:
            col = self.columns[col_idx]
            
            # Create new node
            node = Node()
            node.col = col
            node.row_id = row_id
            
            # Link horizontally within the row
            if nodes:
                node.right = nodes[0]
                node.left = nodes[-1]
                nodes[-1].right = node
                nodes[0].left = node
            else:
                node.left = node
                node.right = node
            
            nodes.append(node)
            
            # Link vertically in the column
            node.down = col.node
            node.up = col.node.up
            col.node.up.down = node
            col.node.up = node
            col.size += 1
    
    def choose_column(self):
        """
        Choose a primary column with minimum size (heuristic for Algorithm X).
        Only considers primary columns (those that must be covered).
        Returns the primary column with fewest 1s, or None if no primary columns remain.
        """
        min_col = None
        min_size = float('inf')
        
        col_node = self.header.node.right
        while col_node != self.header.node:
            col = col_node.col
            # Only consider primary columns
            if col.primary and col.size < min_size:
                min_size = col.size
                min_col = col
            col_node = col_node.right
        
        return min_col
    
    def cover(self, col):
        """Cover a column (remove it and all rows that intersect it)."""
        # Remove column header from column list
        col.node.right.left = col.node.left
        col.node.left.right = col.node.right
        
        # For each row in this column
        node = col.node.down
        while node != col.node:
            # For each column in this row
            other_node = node.right
            while other_node != node:
                # Remove this node from its column
                other_node.down.up = other_node.up
                other_node.up.down = other_node.down
                other_node.col.size -= 1
                other_node = other_node.right
            node = node.down
    
    def uncover(self, col):
        """Uncover a column (undo a cover operation)."""
        # Restore rows in reverse order
        node = col.node.up
        while node != col.node:
            # For each column in this row (in reverse order)
            other_node = node.left
            while other_node != node:
                # Restore this node to its column
                other_node.col.size += 1
                other_node.down.up = other_node
                other_node.up.down = other_node
                other_node = other_node.left
            node = node.up
        
        # Restore column header to column list
        col.node.right.left = col.node
        col.node.left.right = col.node
    
    def solve(self, max_solutions=None):
        """
        Solve the exact cover problem using Algorithm X.
        
        Args:
            max_solutions: Stop after finding this many solutions (None = find all)
        
        Returns:
            List of solutions, where each solution is a list of row_ids
        """
        self.solutions = []
        self.current_partial = []
        self._search(max_solutions)
        return self.solutions
    
    def _search(self, max_solutions):
        """Recursive search function for Algorithm X."""
        if max_solutions and len(self.solutions) >= max_solutions:
            return
        
        # Choose a primary column with minimum size
        col = self.choose_column()
        
        # If no primary columns remain, we have a solution
        # (all primary columns have been covered exactly once)
        if col is None:
            self.solutions.append(list(self.current_partial))
            return
        
        if col.size == 0:
            # No solution in this branch (primary column has no options)
            return
        
        # Cover the column
        self.cover(col)
        
        # Try each row in the column
        node = col.node.down
        while node != col.node:
            if max_solutions and len(self.solutions) >= max_solutions:
                break
            
            # Select this row
            self.current_partial.append(node.row_id)
            
            # Cover other columns in this row
            other_node = node.right
            while other_node != node:
                self.cover(other_node.col)
                other_node = other_node.right
            
            # Recursively search
            self._search(max_solutions)
            
            # Uncover other columns in this row (backtrack)
            other_node = node.left
            while other_node != node:
                self.uncover(other_node.col)
                other_node = other_node.left
            
            # Remove this row from partial solution
            self.current_partial.pop()
            
            node = node.down
        
        # Uncover the column
        self.uncover(col)
    
    # (removed _get_current_solution method - no longer needed)


# Example usage:
if __name__ == "__main__":
    # Example 1: Classic exact cover problem (all primary columns)
    print("Example 1: All primary columns")
    print("-" * 40)
    
    dlx = DLX()
    
    # Create columns for elements 1-7 (all primary)
    cols = [dlx.add_column(f"col{i}", primary=True) for i in range(7)]
    
    # Add rows representing sets
    dlx.add_row([1, 3, 5], row_id="A")
    dlx.add_row([2, 3, 6], row_id="B")
    dlx.add_row([1, 4], row_id="C")
    dlx.add_row([2, 5], row_id="D")
    dlx.add_row([3, 6], row_id="E")
    dlx.add_row([2, 4], row_id="F")
    dlx.add_row([0], row_id="G")
    
    solutions = dlx.solve()
    print(f"Found {len(solutions)} solution(s):")
    for sol in solutions:
        print(f"  {sol}")
    
    # Example 2: Mixed primary and secondary columns
    print("\nExample 2: Mixed primary and secondary columns")
    print("-" * 40)
    
    dlx2 = DLX()
    
    # Create 3 primary columns and 2 secondary columns
    primary = [dlx2.add_column(f"P{i}", primary=True) for i in range(3)]
    secondary = [dlx2.add_column(f"S{i}", primary=False) for i in range(2)]
    
    # Add rows
    dlx2.add_row([0, 3], row_id="Row1")     # covers P0, S0
    dlx2.add_row([1], row_id="Row2")        # covers P1
    dlx2.add_row([2, 4], row_id="Row3")     # covers P2, S1
    
    solutions2 = dlx2.solve()
    print(f"Found {len(solutions2)} solution(s):")
    for sol in solutions2:
        print(f"  {sol}")
