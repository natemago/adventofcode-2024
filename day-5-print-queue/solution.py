from functools import cmp_to_key

def read_input(fn):
    rules = []
    rules_map = {}
    updates = []

    with open(fn) as f:
        for line in f:
            line = line.strip()
            if line == '':
                continue
            if '|' in line:
                x,y = line.split('|')
                x,y = int(x), int(y)
                rules.append((x, y))
                rules_map[x] = rules_map.get(x, []) + [y]
            else:
                updates.append([int(n.strip()) for n in line.split(',')])
    return rules, updates, rules_map


def comparator(rules_map):
    
    def _compare(a, b):
        if a == b:
            return 0
        if a not in rules_map and b not in rules_map:
            raise Exception('Both not in rules map')
        if a not in rules_map:
            return 1
        if b not in rules_map:
            return -1
        if b in rules_map[a]:
            return -1
        if a in rules_map[b]:
            return 1

    return _compare


def part1(rules, updates, rules_map):
    compare = comparator(rules_map)
    total = 0
    for u in updates:

        s = sorted(u, key=cmp_to_key(compare))
        if s == u:
            total += u[len(u)//2]
    return total


def part2(rules, updates, rules_map):
    compare = comparator(rules_map)
    total = 0
    for u in updates:

        s = sorted(u, key=cmp_to_key(compare))
        if s != u:
            total += s[len(s)//2]
    return total


print('Part 1:', part1(*read_input('input')))
print('Part 2:', part2(*read_input('input')))