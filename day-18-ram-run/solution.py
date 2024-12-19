def read_input(fn):
    with open(fn) as f:
        positions = []
        for line in f:
            if line.strip():
                pp = line.strip().split(',')
                positions.append((int(pp[0]), int(pp[1])))
        return positions

def print_space(width, height, positions, path):
    positions = set(positions)
    path = set(path)
    for y in range(height):
        for x in range(width):
            if (x, y) in path and (x, y) in positions:
                print('X', end='')
            elif (x, y) in path:
                print('O', end='')
            elif (x, y) in positions:
                print('#', end='')
            else:
                print('.', end='')
        print()
                

def part1(positions, width, height, first_n):
    start = (0, 0)
    end = (width-1, height-1)

    corrupted = set(positions[0:first_n])

    q = [(start, (1, 0), []), (start, (0, 1), [])]
    seen = set()

    found_path = None

    while len(q):
        pos, direction, path = q[0]
        q = q[1:]
        if (pos, direction) in seen:
            continue
        seen.add((pos, direction))

        if pos == end:
            pp = path + [(x, y)]
            if found_path is None or len(pp) < len(found_path):
                found_path = pp

        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            x, y = pos
            xx, yy = x+dx, y+dy
            if xx < 0 or xx >= width or yy < 0 or yy >= height:
                continue
            if (xx, yy) in corrupted:
                continue
            q.append(((xx, yy), (dx, dy), path + [(x, y)]))
    

    return len(found_path) - 1 # number of tiles in path minus 1


def part2(positions, width, height, first_n):
    start = (0, 0)
    end = (width-1, height-1)
    
    lower = first_n + 1
    upper = len(positions) - 1

    i = first_n + 1
    while i < len(positions):
        print('Checking byte:', i, ' of ', len(positions))
        corrupted = set(positions[0:i])
        #corrupted = set(positions)

        q = [(start, (1, 0), []), (start, (0, 1), [])]
        seen = set()

        found_path = None

        while len(q):
            pos, direction, path = q[0]
            #print(pos, direction)
            q = q[1:]
            if (pos, direction) in seen:
                continue
            seen.add((pos, direction))

            if pos == end:
                found_path = path

            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                x, y = pos
                xx, yy = x+dx, y+dy
                if xx < 0 or xx >= width or yy < 0 or yy >= height:
                    continue
                if (xx, yy) in corrupted:
                    continue
                q.append(((xx, yy), (dx, dy), path + [(x, y)]))
        
        if found_path is None:
            return ','.join([str(n) for n in positions[i-1]])
        i += 1


print('Part 1:', part1(read_input('input'), 71, 71, 1024))
#print('Part 1:', part1(read_input('test_input'), 7, 7, 12))
print('Part 2:', part2(read_input('input'), 71, 71, 1024))