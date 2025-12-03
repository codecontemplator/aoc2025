with open("input.txt", "r") as file:
    rows = file.read().splitlines()

def process_row(row):
    l = len(row)
    max = None
    for i in range(l-1):
        for j in range(i+1, l):
            num = int(row[i] + row[j])
            if max is None or num > max:
                max = num
    return max

print(sum(map(process_row,rows)))
    
