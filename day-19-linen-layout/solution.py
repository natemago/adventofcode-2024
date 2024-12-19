def read_input(fn):
    with open(fn) as f:
        lines = f.readlines()
        return [l.strip() for l in lines[0].strip().split(',')], [
            line.strip() for line in lines[2:] if line.strip()
        ]


def part1(towels_patterns, designs):
    available = towels_patterns

    cache = {}

    def can_arrange(design):
        if design in cache:
            return cache[design]
        can_it = False
        for a in available:
            if design.startswith(a):
                if design == a:
                    can_it = True
                    break
                if can_arrange(design[len(a):]):
                    can_it = True
                    break
        cache[design] = can_it
        return can_it
    
    total = 0
    for design in designs:
        if can_arrange(design):
            total += 1
    return total


def part2(towels_patterns, designs):
    available = towels_patterns

    cache = {}

    def count_arrangements(design):
        if design in cache:
            return cache[design]
        count = 0
        for a in available:
            if design.startswith(a):
                if design == a:
                    count += 1
                    continue
                count += count_arrangements(design[len(a):])
        cache[design] = count
        return count
    
    total = 0
    for design in designs:
        total += count_arrangements(design)
    return total


print('Part 1:', part1(*read_input('input')))
print('Part 2:', part2(*read_input('input')))