def read_input(fn):
    with open(fn) as f:
        return [l.strip() for l in f.readlines() if l.strip()]

def get_in_8_directions(x, y, ws):
    forward = ''
    backward = ''
    up = ''
    down = ''
    nw = ''
    ne = ''
    sw = ''
    se = ''
    for i in range(4):
        if (x + i) < len(ws[y]):
            forward += ws[y][x+i]
        if (x - i) >= 0:
            backward += ws[y][x-i]
        if (y + i) < len(ws):
            down += ws[y+i][x]
        if (y - i) >= 0:
            up += ws[y-i][x]
        if (y-i) >= 0 and (x-i) >= 0:
            nw += ws[y-i][x-i]
        if (y-i) >= 0 and (x+i) < len(ws[y]):
            ne += ws[y-i][x+i]
        if (y+i) < len(ws) and (x-i) >= 0:
            sw += ws[y+i][x-i]
        if (y+i) < len(ws) and (x+i) < len(ws[y]):
            se += ws[y+i][x+i]
    return (
        up, nw, backward, sw, down, se, forward, ne
    )

def part1(ws):
    count = 0
    for y in range(len(ws)):
        for x in range(len(ws[y])):
            for direction in get_in_8_directions(x, y, ws):
                if direction == 'XMAS':
                    count += 1
    return count

def match_pattern(x, y, matrix, ws):
    for my in range(len(matrix)):
        for mx in range(len(matrix[my])):
            yy = y + my
            xx = x + mx
            if yy >= 0 and yy < len(ws) and xx >= 0 and xx < len(ws[0]):
                if matrix[my][mx] != '.' and ws[yy][xx] != matrix[my][mx]:
                    return False
            else:
                return False
    return True


def part2(ws):
    patterns = (
        (
            'M.M',
            '.A.',
            'S.S',
        ),
        (
            'S.M',
            '.A.',
            'S.M',
        ),
        (
            'S.S',
            '.A.',
            'M.M',
        ),
        (
            'M.S',
            '.A.',
            'M.S',
        ),
    )
    count = 0
    for y in range(len(ws)):
        for x in range(len(ws[y])):
            for pattern in patterns:
                if match_pattern(x, y, pattern, ws):
                    count += 1
    return count


print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))
