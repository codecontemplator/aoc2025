import re

with open('input.txt', 'r') as f:
    text = f.read()

ranges = [ tuple(map(int, range.split('-'))) for range in text.split(',') ]

def is_silly(number):
    numberstr = str(number)
    substrings = [numberstr[:i+1] for i in range(len(numberstr) // 2)]
    for substring in substrings:
        pattern = f"^({substring})+$"
        if re.match(pattern, numberstr):
            return True
    return False

def silly_in_range( start, end):
    return [ number for number in range(start, end + 1) if is_silly(number) ]

all = []
for start, end in ranges:
    all.extend(silly_in_range(start, end))
print(sum(all))
