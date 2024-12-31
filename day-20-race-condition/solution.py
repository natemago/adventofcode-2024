def read_input(fn):
    with open(fn) as f:
        return [line.strip() for line in f if line.strip()]


def find_start_end(maze):
    start, end = None, None
    for y, row in enumerate(maze):
        for x, c in enumerate(row):
            if c == 'S':
                start = (x, y)
            elif c == 'E':
                end = (x, y)
    return start, end


def find_shortest_bfs(maze, start, end):
    # No cheats
    q = [(start, 0)]
    seen = set()

    while len(q):
        curr, steps = q[0]
        q = q[1:]
        if curr in seen:
            continue
        seen.add(curr)
        if curr == end:
            return steps
        
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            x, y = curr
            xx, yy = x+dx, y+dy
            if maze[yy][xx] == '#':
                continue
            q.append(((xx, yy), steps+1))


def cheat_end_positions(delta, exact):
    deltas = []
    for y in range(-delta, delta+1):
        for x in range(-delta, delta+1):
            if exact:
                if (x, y) != (0, 0) and (abs(x) + abs(y)) == delta:
                    deltas.append((x, y))
            else:
                if (x, y) != (0, 0) and (abs(x) + abs(y)) <= delta:
                    deltas.append((x, y))
    return deltas


def all_distances_bfs(a, maze):
    visited = {}
    q = [(a, 0)]

    while len(q):
        curr, steps = q[0]
        q = q[1:]
        if curr in visited:
            continue
        visited[curr] = steps
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            x, y = curr
            xx, yy = x+dx, y+dy
            if maze[yy][xx] == '#':
                continue
            if (xx, yy) in visited:
                continue
            q.append(((xx, yy), steps+1))
    visited[a] = 0
    return visited


def part1(maze):
    start, end = find_start_end(maze)
    shortest_path = find_shortest_bfs(maze, start, end)
    distances_start_end = all_distances_bfs(start, maze)
    distances_end_start = all_distances_bfs(end, maze)

    total = 0
    seen = set()
    for pos, steps in distances_start_end.items():
        for dx, dy in cheat_end_positions(2, exact=True):
            x, y = pos
            xx, yy = dx+x, dy+y
            if (xx, yy) in distances_end_start:
                if (xx, yy) in distances_start_end:
                    if distances_start_end[(xx, yy)] - steps <= 2:
                        continue
                if shortest_path - (steps + distances_end_start[(xx, yy)] + 1) < 100:
                    continue
                total += 1
    return total


def part2(maze):
    start, end = find_start_end(maze)
    shortest_path = find_shortest_bfs(maze, start, end)
    distances_start_end = all_distances_bfs(start, maze)
    distances_end_start = all_distances_bfs(end, maze)

    total = 0
    seen = set()
    for pos, steps in distances_start_end.items():
        for dx, dy in cheat_end_positions(20, exact=False):
            x, y = pos
            xx, yy = dx+x, dy+y
            if (xx, yy) in distances_end_start:
                if (xx, yy) in distances_start_end:
                    if distances_start_end[(xx, yy)] - steps <= (abs(x-xx) + abs(y-yy)):
                        continue
                if shortest_path - (steps + distances_end_start[(xx, yy)] + (abs(x-xx) + abs(y-yy)) - 1) < 100:
                    continue
                total += 1
    return total


print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))
