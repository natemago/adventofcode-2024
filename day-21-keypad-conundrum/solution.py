def read_input(fn):
    with open(fn) as f:
        return [line.strip() for line in f if line.strip()]


num_keypad = [
    '#####',
    '#789#',
    '#456#',
    '#123#',
    '##0A#',
    '#####',
]

dir_keypad = [
    '#####',
    '##^A#',
    '#<v>#',
    '#####',
]


def find_button(bc, keypad):
    for y, row in enumerate(keypad):
        for x, c in enumerate(row):
            if c == bc:
                return (x, y)
    raise Exception('NOT FOUND')


def find_all_shortest(btn, keypad):
    btn_pos = find_button(btn, keypad)
    q = [(btn_pos, [])]
    seen = {}

    while len(q):
        (x, y), sequence = q[0]
        q = q[1:]
        if seen.get((x, y)) is not None:
            continue
        seen[(x, y)] = sequence
        for dx, dy, cc in ((-1, 0, '<'), (1, 0, '>'), (0, 1, 'v'), (0, -1, '^')):
            xx, yy = x+dx, y+dy
            if keypad[yy][xx] == '#':
                continue
            q.append(((xx, yy), sequence + [cc]))
    
    result = {}

    for pos, seq in seen.items():
        x, y = pos
        result[keypad[y][x]] = seq + ['A']

    return result


def find_all_shortest_1(a, b, keypad):
    a_pos = find_button(a, keypad)
    b_pos = find_button(b, keypad)
    q = [(a_pos, [], set())]

    paths = []

    while len(q):
        (x, y), sequence, seen = q[0]
        q = q[1:]
        if (x, y) in seen:
            continue
        #seen[(x, y)] = sequence
        if (x, y) == b_pos:
            paths.append((len(sequence), sequence))
            continue
        for dx, dy, cc in ((-1, 0, '<'), (1, 0, '>'), (0, 1, 'v'), (0, -1, '^')):
            xx, yy = x+dx, y+dy
            if keypad[yy][xx] == '#':
                continue
            q.append(((xx, yy), sequence + [cc], seen.union({(x, y)})))
    
    result = []

    best = min(paths)[0]

    for p in paths:
        if p[0] == best:
            result.append(p + ['A'])

    return result


def shortest_cross_prod(codes, keypad):
    shortest = {}
    for c in codes:
        shortest[c] = find_all_shortest_1(c, keypad)
    return shortest


def code_numerical_to_directional(code, num_keypad_shortest):
    pos = 'A'
    result = []
    for c in code:
        result += num_keypad_shortest[pos][c]
        pos = c
    return result

def code_numerical_to_directional(code, num_keypad_shortest):
    q = [('A', 0, [])]

    sequences = []

    while len(q):
        frm, i, sequence = q.pop()
        nxt = code[i]

        if i == len(code) - 1:
            sequences.append(sequence)
            continue

        for ss in num_keypad_shortest[frm][nxt]:
            q.append((ss, i+1, sequence + ss))
    
    return sequences


def code_directional_to_directional(code, dir_keypad_shortest):
    pos = 'A'
    result = []
    for c in code:
        result += dir_keypad_shortest[pos][c]
        pos = c
    return result

def part1(codes):
    # num_keypad_shortest = shortest_cross_prod('0123456789A', num_keypad)
    # dir_keypad_shortest = shortest_cross_prod('<>^vA', dir_keypad)

    # total = 0
    # for code in codes:
    #     r = code_numerical_to_directional(code, num_keypad_shortest)
    #     print('On num:', ''.join(r))
    #     r = code_directional_to_directional(r, dir_keypad_shortest)
    #     print('On d1:', ''.join(r))
    #     r = code_directional_to_directional(r, dir_keypad_shortest)
    #     print('Final:', ''.join(r))
    #     print(code,':', ''.join(r))
    #     a = int(code[:-1].lstrip('0'))
    #     l = len(r)
    #     print('a=', a, 'l=', l)
    #     break
    # return total
    r = find_all_shortest_1('1', '9', num_keypad)
    print(r)


print('Part 1:', part1(read_input('test_input')))