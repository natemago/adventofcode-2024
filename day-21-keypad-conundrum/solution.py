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


def find_all_shortest(a, b, keypad):
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
            result.append(''.join(p[1]) + 'A')

    return result

def get_sequences_num_keypad(keypad):
    sequences = {}
    for a in '0123456789A':
        for b in '0123456789A':
            sequences[(a, b)] = find_all_shortest(a, b, keypad)
    return sequences


def get_sequences_dir_keypad(keypad):
    sequences = {}
    for a in '<>^vA':
        for b in '<>^vA':
            sequences[(a, b)] = find_all_shortest(a, b, keypad)
    return sequences



def solve_for(codes, num_directional_keypads):
    # Disgusting recursive solution
    num_seq = get_sequences_num_keypad(num_keypad)
    dir_seq = get_sequences_dir_keypad(dir_keypad)
    total = 0

    cache = {}
    def sequence_length(code, depth):
        if (code, depth) in cache:
            return cache[(code, depth)]
        p = 'A'
        best_code_len = 0
        for c in code:
            per_move = []
            for s in dir_seq[(p, c)]:
                per_move.append((len(s), s))
            best_len = min(per_move, key=lambda n: n[0])[0]
            if depth > 0:
                best_for_next = []
                for next_s in per_move:
                    if next_s[0] == best_len:
                        best_for_next.append(sequence_length(next_s[1], depth - 1))
                best_code_len += min(best_for_next)
            else:
                best_code_len += best_len
            p = c
        cache[(code, depth)] = best_code_len

        return best_code_len
    
    for code in codes:
        p = 'A'
        code_length = 0
        for c in code:
            lengths = []
            for seq in num_seq[(p, c)]:
                lengths.append(sequence_length(seq, num_directional_keypads - 2)) # One keypad for the first transformation and one for me.
            p = c
            code_length += min(lengths)
        total += int(code[0:-1].lstrip('0')) * code_length

    return total

def part1(codes):
    return solve_for(codes, 3)


def part2(codes):
    return solve_for(codes, 26)


print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))