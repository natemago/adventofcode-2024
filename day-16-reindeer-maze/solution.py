from heapq import heappush, heappop, heapify
from functools import cmp_to_key
import math


def read_input(fn):
    with open(fn) as f:
        return [line.strip() for line in f if line.strip()]


def get_positions(maze):
    start, stop = None, None
    for y, row in enumerate(maze):
        for x, c in enumerate(row):
            if c == 'S':
                start = (x, y)
            elif c == 'E':
                stop = (x, y)
    return start, stop


def print_maze(maze, path):
    for y, row in enumerate(maze):
        for x, c in enumerate(row):
            if (x, y) in path:
                print(path[(x, y)], end='')
            else:
                print(c, end='')
        print()


P = {
    (0, 1): 'v',
    (0, -1): '^',
    (1, 0): '>',
    (-1, 0): '<',
}


def part1(maze):
    start, stop = get_positions(maze)

    q = [(0, start, (1, 0))]

    distances = {
        start: 0,
    }
    path = {}
    path[start] = ('>', None,)
    seen = set()

    while len(q):
        cost, pos, direction = heappop(q)
        if (pos, direction) in seen:
            continue

        seen.add((pos, direction))

        for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            x, y = pos
            xx, yy = x+dx, y+dy
            if direction == (-dx, -dy) and ((xx, yy), (-dx, -dy)) in seen:
                continue
            if maze[yy][xx] == '#':
                continue
            additional_cost = 1
            if (dx, dy) != direction:
                additional_cost += 1000
            alt = distances[(x, y)] + additional_cost
            if alt < distances.get((xx, yy), math.inf):
                distances[(xx, yy)] = alt
                heappush(q, (alt, (xx, yy), (dx, dy)))
                path[(xx, yy)] = (P[(dx, dy)], (x, y))


    final_path = {}
    p = stop
    while p in path:
        d, f = path[p]
        final_path[p] = d
        p = f 
    
    # print('----------')
    # print_maze(maze, final_path)

    return distances[stop]
        

def part2(maze):
    start, stop = get_positions(maze)
    best_cost = part1(maze)

    q = [(start, (1, 0), 0, set())]
    seen = {}
    best = None
    all_tiles = set()
    while len(q):
        pos, direction, cost, path = q[0]
        q = q[1:]

        if (pos, direction) in seen:
            if seen[(pos, direction)] < cost:
                continue
        seen[(pos, direction)] = cost

        if pos == stop:
            if cost == best_cost:
                all_tiles = all_tiles.union(path).union({stop})
                continue

        for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            x, y = pos
            xx, yy = x+dx, y+dy

            if direction == (-dx, -dy) and ((xx, yy), (-dx, -dy)) in seen:
                continue
            if maze[yy][xx] == '#':
                continue
            additional_cost = 1
            if (dx, dy) != direction:
                additional_cost += 1000
            if cost + additional_cost > best_cost:
                continue
            q.append(((xx, yy), (dx, dy), cost + additional_cost, path.union({(x, y)})))


    return len(all_tiles)


print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))