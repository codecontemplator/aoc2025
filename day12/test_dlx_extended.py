#!/usr/bin/env python3
"""Test the extended DLX implementation with primary and secondary columns."""

from dlx import DLX

print("=" * 50)
print("Testing Extended DLX Implementation")
print("=" * 50)

# Test 1: Simple exact cover with all primary columns
print("\nTest 1: All Primary Columns")
print("-" * 50)

dlx1 = DLX()
# Create 3 primary columns (must cover all)
for i in range(3):
    dlx1.add_column(f"P{i}", primary=True)

# Add solutions
dlx1.add_row([0, 1], row_id="Row_A")
dlx1.add_row([1, 2], row_id="Row_B")

solutions1 = dlx1.solve(max_solutions=5)
print(f"Found {len(solutions1)} solution(s):")
for sol in solutions1:
    print(f"  {sol}")

# Test 2: Mixed primary and secondary columns
print("\nTest 2: Mixed Primary and Secondary Columns")
print("-" * 50)

dlx2 = DLX()
# Create 2 primary columns (must cover both)
for i in range(2):
    dlx2.add_column(f"Primary{i}", primary=True)
# Create 1 secondary column (can cover 0 or 1 times)
dlx2.add_column("Secondary0", primary=False)

# Add rows
dlx2.add_row([0, 2], row_id="Row_X")  # covers P0 and S0
dlx2.add_row([1], row_id="Row_Y")     # covers P1

solutions2 = dlx2.solve(max_solutions=5)
print(f"Found {len(solutions2)} solution(s):")
for sol in solutions2:
    print(f"  {sol}")

# Test 3: Secondary column with multiple options
print("\nTest 3: Secondary Column with Options")
print("-" * 50)

dlx3 = DLX()
# Create 1 primary column
dlx3.add_column("Primary0", primary=True)
# Create 2 secondary columns
for i in range(2):
    dlx3.add_column(f"Secondary{i}", primary=False)

# Add rows - multiple ways to cover the primary column
dlx3.add_row([0, 1], row_id="Row_A")  # covers P0 and S0
dlx3.add_row([0, 2], row_id="Row_B")  # covers P0 and S1

solutions3 = dlx3.solve(max_solutions=5)
print(f"Found {len(solutions3)} solution(s):")
for sol in solutions3:
    print(f"  {sol}")

print("\n" + "=" * 50)
print("All tests completed!")
print("=" * 50)
