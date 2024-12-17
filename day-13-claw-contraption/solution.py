import re

def read_input(fn):
    machines = []
    with open(fn) as f:
        b1 = None
        b2 = None
        prize = None
        for line in f:
            if (m := re.match(r'Button A: X\+(\d+), Y\+(\d+)', line)):
                b1 = (int(m.group(1)), int(m.group(2)))
            elif (m := re.match(r'Button B: X\+(\d+), Y\+(\d+)', line)):
                b2 = (int(m.group(1)), int(m.group(2)))
            elif (m := re.match(r'Prize: X=(\d+), Y=(\d+)', line)):
                prize = (int(m.group(1)), int(m.group(2)))
                machines.append((b1, b2, prize))
            else:
                if line.strip():
                    print('Not matched:', line)
                    raise Exception('not matched')
    return machines


def reach(ba, bb, prize):
    x1,y1 = ba
    x2,y2 = bb
    px, py = prize


    reachable = []
    for i in range(px//x1 + 1):
        for j in range(px//x2 + 1):
            if x1*i + x2*j == px and y1*i + y2*j == py:
                reachable.append((i, j))
    return reachable


def part1(machines):
    '''
    '''
    total = 0
    for ba, bb, prize in machines:
        reachable = reach(ba, bb, prize)
        tokens_spent = []
        for presses_a, presses_b in reachable:
            tokens_spent.append(3*presses_a + presses_b)
        if len(tokens_spent):
            total += min(tokens_spent)
        
    
    return total


def part2(machines):
    '''
    m*x1 + n*x2 = px
    m*y1 + n*y2 = py
    -----------------

    m + n*(x2/x1) = px/x1
    m + n*(y2/y1) = py/y1
    ----------------------
    n(x2/x1) - n(y2/y1) = px/x1 - py/y1
    n(x2/x1 - y2/y1) = px/x1 - py/y1

    n = (px/x1 - py/y1)/(x2/x1 - y2/y1)
    
           px*y1 - py*x1
          -----------------------
              x1*y1
    n = ------------------------------
           x2*y1 - x1*y2
          ----------------------
              x1*y1
    
        px*y1 - py*x1
    n = ---------------
        x2*y1 - x1*y2


    m = (px - n*x2)/x1
    '''

    total = 0
    for ba, bb, prize in machines:
        x1, y1 = ba
        x2, y2 = bb
        px, py = prize
        px, py = px+10000000000000, py+10000000000000

        if x2*y1 - x1*y2 == 0 or x1 == 0:
            # multiple solutions are possible
            raise Exception('OH NO')
        if (px*y1 - py*x1) % (x2*y1 - x1*y2) != 0:
            # cannot reach the prize
            continue
        
        n = (px*y1 - py*x1) // (x2*y1 - x1*y2)
        if (px - n*x2) % x1 != 0:
            # cannot reach the prize
            continue

        # there is only a single solution
        m = (px - n*x2) // x1

        total += 3*m + n
    
    return total


print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))
