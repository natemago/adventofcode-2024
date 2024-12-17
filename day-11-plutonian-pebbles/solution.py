def read_input(fn):
    with open(fn) as f:
        return [int(c) for c in f.read().strip().split()]


def blink(pebbles, times):
    for i in range(times):
        np = []
        for p in pebbles:
            if p == 0:
                np.append(1)
            elif len(str(p)) % 2 == 0:
                p = str(p)
                np.append(int(p[0:len(p)//2]))
                np.append(int(p[len(p)//2:]))
            else:
                np.append(p * 2024)
        pebbles = np
    
    return pebbles


def part1(pebbles):
    pebbles = blink(pebbles, 25)
    return len(pebbles)


def part2(pebbles):
    values = {p: 1 for p in pebbles}
    for i in range(75):
        for p, count in list(values.items()):
            if p == 0:
                if values.get(0) is not None:
                    values[0] -= count
                    if values[0] <= 0:
                        del values[0]
                values[1] = values.get(1, 0) + count
            elif len(str(p)) % 2 == 0:
                p = str(p)
                v1 = int(p[0:len(p)//2])
                v2 = int(p[len(p)//2:])
                p = int(p)
                if values.get(p) is not None:
                    values[p] -= count
                    if values[p] <= 0:
                        del values[p]
                values[v1] = values.get(v1, 0) + count
                values[v2] = values.get(v2, 0) + count
            else:
                if values.get(p) is not None:
                    values[p] -= count
                    if values[p] <= 0:
                        del values[p]
                values[p*2024] = values.get(p*2024, 0) + count
    return sum(values.values())

print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))
