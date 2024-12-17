import re
from math import ceil


def read_input(fn):
    with open(fn) as f:
        robots = []
        for line in f:
            m = re.match(r'p=(-{0,1}\d+),(-{0,1}\d+) v=(-{0,1}\d+),(-{0,1}\d+)', line)
            if m:
                robots.append(((
                    int(m.group(1)),
                    int(m.group(2)),
                ),(
                    int(m.group(3)),
                    int(m.group(4)),
                )))
        return robots


def print_robots(robots, width, height):
    rm = {}
    for r in robots:
        rm[r[0]] = rm.get(r[0], 0) + 1

    for y in range(height):
        for x in range(width):
            if (x, y) in rm:
                print(rm[(x,y)], end='')
            else:
                print('.', end='')
        print()



def part1(robots, width, height):
    for i in range(100):
        next_robots = []
        for robot in robots:
            (x, y), (dx, dy) = robot
            next_robots.append(((
                (x+dx) % width,
                (y+dy) % height,
            ),(dx, dy)))
        robots = next_robots

    mid_x = width//2
    mid_y = height//2

    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0
    for robot in robots:
        (x, y), _ = robot
        if x < mid_x and y < mid_y:
            q1 += 1
        elif x < mid_x and y > mid_y:
            q4 += 1
        elif x > mid_x and y < mid_y:
            q3 += 1
        elif x > mid_x and y > mid_y:
            q2 += 1
    
    return q1*q2*q3*q4


def find_clusters(robots):
    cid = 0
    clusters = {}

    seen = set()

    rpos = set()
    for (x, y), _ in robots:
        rpos.add((x, y))

    for (rx, ry),_ in robots:
        if (rx, ry) in seen:
            continue
        cid += 1
        clusters[cid] = set()

        q = [(rx, ry)]

        while len(q):
            x, y = q[0]
            q = q[1:]
            if (x, y) in seen:
                continue
            seen.add((x, y))
            clusters[cid].add((x, y))
            for xx, yy in ((x+0, y+1), (x+0, y-1), (x+1, y+0), (x-1, y+0)):
                if (xx, yy) in rpos:
                    q.append((xx, yy))
    return clusters


def part2(robots, width, height):
    i = 0
    min_clusters = None
    while True:
        next_robots = []
        for robot in robots:
            (x, y), (dx, dy) = robot
            next_robots.append(((
                (x+dx) % width,
                (y+dy) % height,
            ),(dx, dy)))
        i += 1
        robots = next_robots
        clusters = find_clusters(robots)
        for _, cr in clusters.items():
            if len(cr) >= len(robots)/5:
                print_robots(robots, width, height)
                print(i)
                if len(cr) >= len(robots)/3:
                    cont = input('Possible solution here. Type c and hit enter to continue searching or just enter if found...')
                    if cont.strip() == 'c':
                        continue
                    else:
                        return i


print('Part 1:', part1(read_input('input'), 101, 103))
print('Part 2:', part2(read_input('input'), 101, 103))
