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

def part1(maze):
    start, end = find_start_end(maze)

    q = [(start, 0, (-1, 0), None), (start, 0, (1, 0), None), (start, 0, (0, -1), None), (start, 0, (0, 1), None)]
    seen = set()

    while len(q):
        pos, steps, direction, cheat = q[0]
        #print(pos, steps, direction)
        q = q[1:]

        if (pos, direction, ) in seen:
            continue
        seen.add((pos, direction, cheat))

        if pos == end:
            print(steps, ' steps with cheat:', cheat)
            continue
        
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            x,y = pos
            xx, yy = x+dx, y+dy
            if maze[yy][xx] == '#':
                if cheat is not None:
                    if (xx, yy) in cheat:
                        q.append(((xx, yy), steps + 1, (dx, dy), cheat))
                    else:
                        continue
                else:
                    cxx, cyy = xx+dx, yy+dy
                    if cxx < 0 or cxx >= len(maze[0]) or cyy < 0 or cyy >= len(maze):
                        continue
                    if maze[cyy][cxx] == '#':
                        continue
                    c = ((xx, yy), (cxx, cyy))
                    print('cheat at:', c)
                    q.append(((xx, yy), steps + 1, (dx, dy), c))
                    continue

            q.append(((xx, yy), steps + 1, (dx, dy), cheat))



print('Part 1:', part1(read_input('input')))