#with open('example.txt', 'r') as f:
#    rows = f.read().splitlines()

def parse_btn(s):
    return list(map(int,s.strip("()").split(",")))

def parse_goal(s):
    goal = set()
    for i in range(len(s)):
        if s[i] == '#':
            goal.add(i)
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

goal, btns, _ = parse_row("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}");

def update_lights(lights, btn):
    new_lights = set(lights)
    for i in btn:
        if i in lights:
            new_lights.remove(i)
        else:
            new_lights.add(i)
    return new_lights

def press_btn(pressed, i):
    pressed2 = dict(pressed)
    pressed2[i] += 1
    return pressed2

def search(lights, btn_state, g_min_cnt):
    #print(lights, btn_state)
    if lights == goal:
        return btn_state
        
    (cnt,pressed) = btn_state
    if g_min_cnt is not None and cnt >= g_min_cnt:
        return (None, None)
    
    min_cnt = None
    final_result = None
    for i in range(len(btns)):
        if pressed[i] < 2:
            cnt_result, pressed_result = search(update_lights(lights, btns[i]), (cnt+1, press_btn(pressed, i)), min_cnt)
            if cnt_result is None:
                continue
            if min_cnt is None or cnt_result < min_cnt:
                min_cnt = cnt_result
                final_result = pressed_result
    return (min_cnt, final_result)

# lights = set()
# print(lights)
# lights = update_lights(lights, btns[0])
# print(lights)
# lights = update_lights(lights, btns[0])
# print(lights)
# lights = update_lights(lights, btns[1])
# print(lights)
# lights = update_lights(lights, btns[0])
# print(lights)
 
pressed = search(set(), (0, dict([(i,0) for i in range(len(btns))])), None)
print(pressed)
