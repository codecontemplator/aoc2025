with open('input.txt', 'r') as f:
    rows = f.read().splitlines()

def parse_btn(s):
    return  list(map(int,s.strip("()").split(",")))
    #return sum([ 2**i for i in bits])

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
    return (p1f, p2f, p3f)

#goal, btns_orig, _ = parse_row("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}");
#btns = list(map(lambda x: sum([ 2**i for i in x]), btns_orig))

def search(goal, btns, lights, pressed, cnt, g_min_cnt):
    from collections import deque
    
    queue = deque([(lights, pressed, cnt)])
    visited = {(lights, tuple(sorted(pressed.items())))}
    
    while queue:
        lights, pressed, cnt = queue.popleft()
        
        if lights == goal:
            return (cnt, pressed)
        
        if g_min_cnt is not None and cnt >= g_min_cnt:
            continue
        
        for i, btn in enumerate(btns):
            if pressed[i] < 2:
                pressed2 = pressed | {i: pressed[i] + 1}
                new_lights = lights ^ btn
                state = (new_lights, tuple(sorted(pressed2.items())))
                
                if state not in visited:
                    visited.add(state)
                    queue.append((new_lights, pressed2, cnt + 1))
    
    return (None, None)


# (cnt,pressed) = search(0, dict([(i,0) for i in range(len(btns))]), 0, None)
# print(pressed)
# for i,cnt in pressed.items():
#     if cnt > 0:
#         print(f"{btns_orig[i]} * {cnt}")

parsed_rows = [ parse_row(row) for row in rows ]
total_cnt = 0
for goal, btns_orig, _ in parsed_rows:
    btns = [ sum([ 2**i for i in btn]) for btn in btns_orig]
    no_lights = 0
    no_pressed = dict([(i,0) for i in range(len(btns))])
    cnt, _ = search(goal, btns, no_lights, no_pressed, 0, None)
    print(cnt)
    total_cnt += cnt

print("=", total_cnt)    