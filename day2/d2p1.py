import re

with open('input.txt', 'r') as f:
    text = f.read()

ranges = [ tuple(map(int, range.split('-'))) for range in text.split(',') ]

def is_silly(number):
    numberstr = str(number)
    halfstring = numberstr[:len(numberstr)//2]
    return halfstring * 2 == numberstr
    # substrings = [numberstr[:i+1] for i in range(len(numberstr) // 2)]
    # for substring in substrings:
    #     pattern = f"^({substring}){2}$"
    #     if re.match(pattern, numberstr):
    #         return True
    # return False

def silly_in_range( start, end):
    return [ number for number in range(start, end + 1) if is_silly(number) ]

#print(ranges)    

# x = re.search("^(123)+$", "123123")  # Example match
# print(x)

# x = re.search("^(123)+$", "1223123")  # Example match
# print(x)


# print(is_silly(123123))
# print(is_silly(123456))
# print(is_silly(111111))

all = []
for start, end in ranges:
    all.extend(silly_in_range(start, end))
print(sum(all))

