def read_input(fn):
    l1, l2 = [], []
    with open(fn) as f:
        for line in f:
            n1, n2 = line.strip().split()
            l1.append(int(n1))
            l2.append(int(n2))
    return l1, l2


def part1(l1, l2):
    l1 = list(sorted(l1))
    l2 = list(sorted(l2))
    assert len(l1) == len(l2)
    return sum([abs(l1[i] - v) for i,v in enumerate(l2)])


def part2(l1, l2):
    d2 = {}
    for i in l2:
        d2[i] = d2.get(i, 0) + 1
    return sum([i*d2.get(i, 0) for i in l1])

print('Part 1:', part1(*read_input('input')))
print('Part 2:', part2(*read_input('input')))
