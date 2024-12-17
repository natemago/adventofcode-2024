def read_input(fn):
    area = []
    antennae = {}

    with open(fn) as f:
        for line in f:
            if not line.strip():
                continue
            area.append(line.strip())
    
    for y, row in enumerate(area):
        for x, c in enumerate(row):
            if c == '.':
                continue
            antennae[c] = antennae.get(c, []) + [(x, y)]
    
    return area, antennae


def print_area(area, antennae, antipodes):
    am = {}
    for a, locations in antennae.items():
        for x, y in locations:
            am[(x, y)] = a
    overlaps = {}
    oc = 1
    for y, row in enumerate(area):
        for x, c in enumerate(row):
            if (x, y) in am and (x, y) in antipodes:
                print(oc, end='')
                overlaps[oc] = 'antena={}, antipode of={}'.format(am[(x, y)], antipodes[(x, y)])
                oc += 1
            elif (x, y) in am:
                print(am[(x, y)], end='')
            elif (x, y) in antipodes:
                print('#', end='')
            else:
                print(c, end='')
        print()


def part1(area, antennae):
    antipodes = {}
    for freq, ant in antennae.items():
        for i, a in enumerate(ant[0: -1]):
            for b in ant[i+1:]:
                dx, dy = b[0] - a[0], b[1] - a[1]
                x, y = b[0] + dx, b[1] + dy
                if x >= 0 and x < len(area[0]) and y >= 0 and y < len(area):
                    antipodes[(x, y)] = freq
                dx, dy = a[0] - b[0], a[1] - b[1]
                x, y = a[0] + dx, a[1] + dy
                if x >= 0 and x < len(area[0]) and y >= 0 and y < len(area):
                    antipodes[(x, y)] = freq

    #print_area(area, antennae, antipodes)
    return len(antipodes)


def part2(area, antennae):
    antipodes = {}
    for freq, ant in antennae.items():
        for i, a in enumerate(ant[0: -1]):
            for b in ant[i+1:]:
                dx, dy = b[0] - a[0], b[1] - a[1]
                sx, sy = b
                while True:
                    x, y = sx + dx, sy + dy
                    if x < 0 or x >= len(area[0]) or y < 0 or y >= len(area):
                        break
                    antipodes[(x, y)] = freq
                    sx, sy = x, y

                dx, dy = a[0] - b[0], a[1] - b[1]
                sx, sy = a
                while True:
                    x, y = sx + dx, sy + dy
                    if x < 0 or x >= len(area[0]) or y < 0 or y >= len(area):
                        break
                    antipodes[(x, y)] = freq
                    sx, sy = x, y
    
    for freq, locations in antennae.items():
        if len(locations) > 1:
            for l in locations:
                antipodes[l] = freq

    #print_area(area, antennae, antipodes)

    return len(antipodes)

print('Part 1:', part1(*read_input('input')))
print('Part 2:', part2(*read_input('input')))