def read_input(fn):
    the_map = []
    with open(fn) as f:
        for line in f:
            if not line.strip():
                continue
            the_map.append(line.strip())
    return the_map

def find_guard_position(m):
    for y, row in enumerate(m):
        for x, c in enumerate(row):
            if c in '<>^V':
                return (x, y)
    raise Exception('no guard on the map')

DIRECTIONS = {
    '>': (1, 0),
    '<': (-1, 0),
    '^': (0, -1),
    'V': (0, 1),
}

def rotate(direction):
    return {
        (1, 0): (0, 1),
        (-1, 0): (0, -1),
        (0, -1): (1, 0),
        (0, 1): (-1, 0),
    }[direction]

def print_area(area, gp, visited):
    xx, yy = gp

    for y, row in enumerate(area):
        for x, c in enumerate(row):
            if (x, y) == gp:
                print('G', end='')
            elif (x, y) in visited:
                print('X', end='')
            else:
                print(c, end='')
        print()


def part1(the_map):
    x,y = find_guard_position(the_map)
    direction = DIRECTIONS[the_map[y][x]]
    visited = set()

    while True:
        visited.add((x, y))
        dx, dy = direction
        xx, yy = x+dx, y+dy

        if xx < 0 or yy < 0 or xx >= len(the_map[0]) or yy >= len(the_map):
            break # outside of area
        if the_map[yy][xx] == '#':
            # wall, must rotate
            direction = rotate(direction)
            continue
        
        x, y = xx, yy

    return len(visited)


def has_infinite_loop(area):
    x,y = find_guard_position(area)
    direction = DIRECTIONS[area[y][x]]
    visited = set()

    while True:
        if (x, y, direction) in visited:
            return True # we have entered an infinite loop
        visited.add((x, y, direction))

        dx, dy = direction
        xx, yy = x+dx, y+dy

        if xx < 0 or yy < 0 or xx >= len(area[0]) or yy >= len(area):
            return False
        if area[yy][xx] == '#':
            # wall, turn right
            direction = rotate(direction)
            continue
        x, y = xx, yy


def part2(area):
    total = 0
    gp = find_guard_position(area)
    for y in range(len(area)):
        for x in range(len(area[y])):
            if (x, y) == gp or area[y][x] == '#':
                continue

            test_area = [[c for c in row] for row in area]
            test_area[y][x] = '#'
            if has_infinite_loop(test_area):
                total += 1
    return total


print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))