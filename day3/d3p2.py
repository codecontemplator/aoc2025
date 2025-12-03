with open("input.txt", "r") as file:
    rows = file.read().splitlines()

def process_row(rowin):
    row = list(map(int, list(rowin)))
    rowlen = len(row)
    startpos = 0
    result = []
    for i in range(12):
        endpos = rowlen - 11 + i
        selected = max(row[startpos:endpos])
        selected_index = row.index(selected, startpos, endpos)
        startpos = selected_index + 1
        result.append(selected)
    return int(''.join(map(str,result)))

print(sum(list(map(process_row, rows))))


