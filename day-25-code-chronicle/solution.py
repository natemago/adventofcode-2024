def read_input(fn):
    keys = []
    locks = []
    with open(fn) as f:
        schematic = []
        for line in f:
            if not line.strip():
                if len(schematic):
                    if schematic[0].strip('#') == '':
                        locks.append(schematic)
                    elif schematic[-1].strip('#') == '':
                        keys.append(schematic)
                    else:
                        raise Exception('\n'.join(schematic))
                    schematic = []
            else:
                schematic.append(line.strip())
    if len(schematic):
        if schematic[0].strip('#') == '':
            locks.append(schematic)
        elif schematic[-1].strip('#') == '':
            keys.append(schematic)
        else:
            raise Exception('\n'.join(schematic))
    return locks, keys

def to_heights(schematic):
    if schematic[0].strip('#') == '':
        heights = []
        for i in range(len(schematic[0])):
            heights.append(0)
            for j in range(len(schematic)):
                if schematic[j][i] == '#':
                    heights[-1] += 1
        return (len(schematic), heights)
    else:
        heights = []
        for i in range(len(schematic[0])):
            heights.append(0)
            for j in range(len(schematic)-1, -1, -1):
                if schematic[j][i] == '#':
                    heights[-1] += 1
        return (len(schematic), heights)

def does_it_fit(lock, key):
    h1, l_numbers = lock
    h2, k_numbers = key
    if h1 != h2:
        return False
    if len(l_numbers) != len(k_numbers):
        return False
    
    for i in range(len(l_numbers)):
        if l_numbers[i] + k_numbers[i] > h1:
            return False
    return True

def part1(locks, keys):
    locks = [to_heights(l) for l in locks]
    keys = [to_heights(k) for k in keys]

    total = 0
    for lock in locks:
        for key in keys:
            if does_it_fit(lock, key):
                total += 1
    return total


print('Part 1:', part1(*read_input('input')))
