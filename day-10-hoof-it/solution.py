def read_input(fn):
    with open(fn) as f:
        return [[int(v) for v in line.strip()] for line in f if line.strip()]


def reach(x, y, topo_map):
    reached = {}
    q = [(x, y)]

    while len(q):
        x, y = q[0]
        q = q[1:]

        if topo_map[y][x] == 9:
            reached[(x, y)] = reached.get((x, y), 0) + 1
            continue

        current = topo_map[y][x]

        for xx, yy in ((x, y-1), (x-1, y), (x, y+1), (x+1, y)):
            if xx < 0 or xx >= len(topo_map[0]) or yy < 0 or yy >= len(topo_map):
                continue
            if topo_map[yy][xx] - current == 1:
                q.append((xx, yy))
    
    return reached


def find_trail_heads(topo_map):
    trail_heads = []
    for y, row in enumerate(topo_map):
        for x, c in enumerate(row):
            if c == 0:
                trail_heads.append((x, y))
    return trail_heads


def part1(topo_map):
    total = 0
    for x, y in find_trail_heads(topo_map):
        reached = reach(x, y, topo_map)
        total += len(reached)
    return total


def part2(topo_map):
    total = 0
    for x, y in find_trail_heads(topo_map):
        reached = reach(x, y, topo_map)
        total += sum(reached.values())
    return total


print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))
