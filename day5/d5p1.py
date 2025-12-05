with open('input.txt', 'r') as file:
    content = file.read().splitlines()
    
sep = content.index('')    
intervals =  content[:sep]
indices = content[sep+1:]  

intervals = [tuple(map(int, interval.split('-'))) for interval in intervals]
indices = [int(index) for index in indices]

fresh = sum([ 1
         for index in indices
         if any(start <= index <= end for start, end in intervals)
])

print(fresh)