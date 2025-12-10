with open('input.txt', 'r') as f:
    rows = f.read().splitlines()

def parse_btn(s):
    return  list(map(int,s.strip("()").split(",")))

def parse_goal(s):
    goal = 0
    for i in range(len(s)):
        if s[i] == '#':
            goal += 2**i
    return goal

def parse_row(s):
    i1 = s.index("]") + 1
    i2 = s.index("{") - 1
    p1 = s[1:i1-1]
    p2 = s[i1+1:i2]
    p3 = s[i2+2:-1]
    p1f = parse_goal(p1)
    p2f = list(map(parse_btn, p2.split(" ")))
    p3f = list(map(int,p3.split(",")))
    return (p2f, p3f )  # btns, goal

def update(btn, cur):
    next = list(cur)
    for i in btn:
        next[i] += 1
    return next

def search(goal, btns, cur, pressed):
    from collections import deque
    
    queue = deque([(cur, pressed, 0)])
    visited = {(tuple(cur), tuple(sorted(pressed.items())))}
    
    while queue:
        cur, pressed, cnt = queue.popleft()
        print(cnt)
        
        if cur == goal:
            return (cnt, pressed)
        
        for i, btn in enumerate(btns):
            pressed2 = pressed | {i: pressed[i] + 1}
            next = update(btn, cur)
            state = (tuple(next), tuple(sorted(pressed2.items())))
            
            if state not in visited:
                visited.add(state)
                queue.append((next, pressed2, cnt + 1))
    
    return (None, None)

parsed_rows = [ parse_row(row) for row in rows ]
total_cnt = 0
for btns, goal in parsed_rows:
    start = [ 0 for i in range(len(goal))]
    no_pressed = dict([(i,0) for i in range(len(btns))])
    cnt, _ = search(goal, btns, start, no_pressed)
    print(cnt)
    total_cnt += cnt

print("=", total_cnt)    