def read_input(fn):
    with open(fn) as f:
        return [int(c) for c in f.read().strip()]


def to_disk(disk_map):
    m = []

    i = 0
    id = 0
    while i < len(disk_map):
        used = disk_map[i]
        free = 0
        if i+1 < len(disk_map):
            free = disk_map[i+1]
        i += 2
        for j in range(used):
            m.append(id)
        for j in range(free):
            m.append(-1)
        id += 1

    return m


def part1(disk_map):
    disk = to_disk(disk_map)

    c = 0
    p = len(disk) - 1
    while c < p:
        if disk[c] >= 0:
            c += 1
            continue
        while disk[p] < 0 and p >= 0:
            p -= 1
        if c >= p:
            break
        if disk[c] < 0 and disk[p] >= 0:
            # swap
            disk[c] = disk[p]
            disk[p] = -1
            p -= 1
        # goto next
        c += 1

    checksum = 0
    for i, v in enumerate(disk):
        if v < 0:
            break
        checksum += i*v
    return checksum


def files(disk):
    f = []

    file_id = None
    idx = None
    size = 0
    for i, c in enumerate(disk):
        if c >= 0:
            if file_id is None:
                file_id = c
                idx = i
            else:
                if file_id != c:
                    f.append((file_id, idx, size))
                    file_id = c
                    idx = i
                    size = 0
            size += 1
        else:
            if file_id is not None:
                f.append((file_id, idx, size))
                size = 0
                file_id = None
                idx = None
    
    if file_id is not None and idx is not None:
        f.append((file_id, idx, size))


    return f

def part2(disk_map):
    disk = to_disk(disk_map)
    fs = files(disk)

    def next_free_space(start, end):
        i = start
        at_idx = None
        size = 0
        while i < end:
            if disk[i] >= 0:
                i += 1
                continue
            at_idx = i
            while disk[i] < 0 and i < end:
                i += 1
                size += 1
            break
        return (at_idx, size)

    for file_id, f_idx, f_size in reversed(fs):
        start_idx = 0
        while True:
            free_idx, free_size = next_free_space(start_idx, f_idx)
            
            if free_idx is None:
                break # end of disk, doesn't fit
            if free_size >= f_size:
                # move file here
                for i in range(f_size):
                    disk[free_idx + i] = file_id
                    disk[f_idx + i] = -1
                break
            start_idx = free_idx + free_size

    checksum = 0
    for i, c in enumerate(disk):
        if c > 0:
            checksum += i*c

    return checksum
    
print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))