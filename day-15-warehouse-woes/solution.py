def read_input(fn):
    with open(fn) as f:
        warehouse = []
        instructions = ''
        for line in f:
            if not line.strip():
                continue
            if line.strip()[0] in '><v^':
                instructions += line.strip()
            else:
                warehouse.append(line.strip())
        return warehouse, instructions


def to_warehouse_map(warehouse):
    wm = {}
    robot_position = None
    for y, row in enumerate(warehouse):
        for x, c in enumerate(row):
            if c == '@':
                if robot_position is not None:
                    raise Exception('multiple robots?')
                robot_position = (x, y)
            elif c in '#O[]':
                wm[(x, y)] = c
    return wm, robot_position


DIRECTIONS = {
    '>': (1, 0),
    '<': (-1, 0),
    '^': (0, -1),
    'v': (0, 1),
}


def peek_ahead(pos, direction, wm):
    x, y = pos
    dx, dy = direction
    xx, yy = x+dx, y+dy
    if (xx, yy) not in wm:
        return True, []
    if wm[(xx, yy)] == 'O':
        boxes = []
        while (xx, yy) in wm:
            if wm[(xx, yy)] == 'O':
                boxes.append((xx, yy))
            elif wm[(xx, yy)] == '#':
                return False, []
            xx, yy = xx+dx, yy+dy
        return True, boxes
    return False, []

def part1(warehouse, instructions):
    wm, robot_position = to_warehouse_map(warehouse)

    for instr in instructions:
        can_move, boxes = peek_ahead(robot_position, DIRECTIONS[instr], wm)
        if can_move:
            # move the boxes in the same direction
            moved_boxes = []
            dx, dy = DIRECTIONS[instr]
            for x,y in boxes:
                moved_boxes.append((x+dx, y+dy))
                del wm[(x, y)]
            for x,y in moved_boxes:
                wm[(x, y)] = 'O'
            robot_position = (robot_position[0] + dx, robot_position[1] + dy)
    
    total = 0
    for (x, y), c in wm.items():
        if c == 'O':
            total += 100*y + x

    return total


def widen_warehouse(warehouse):
    wide = []
    for row in warehouse:
        wide_row = ''
        for c in row:
            if c == '#':
                wide_row += '##'
            elif c == '@':
                wide_row += '@.'
            elif c == 'O':
                wide_row += '[]'
            elif c == '.':
                wide_row += '..'
        wide.append(wide_row)
    return wide


def peek_ahead_wide(pos, direction, wm):
    x, y = pos
    dx, dy = direction
    xx, yy = x+dx, y+dy

    if (xx, yy) not in wm:
        return True, []
    if direction in (DIRECTIONS['<'], DIRECTIONS['>']):
        # just as part 1, just move all boxes on the same line
        if wm[(xx, yy)] in '[]':
            boxes = []
            while (xx, yy) in wm:
                if wm[(xx, yy)] in '[]':
                    boxes.append((xx, yy))
                elif wm[(xx, yy)] == '#':
                    return False, []
                xx, yy = xx+dx, yy+dy
            return True, boxes
        else:
            return False, []
    else:
        if wm[(xx, yy)] == '#':
            return False, []
        boxes = []
        topmost_boxes = [(xx, yy)]
        if wm[(xx, yy)] == '[':
            topmost_boxes.append((xx+1, yy))
        else:
            topmost_boxes.append((xx-1, yy))
        boxes += topmost_boxes
        while len(topmost_boxes):
            new_topmost_boxes = []
            for x, y in topmost_boxes:
                xx, yy = x+dx, y+dy
                if (xx, yy) not in wm:
                    continue
                if wm.get((xx, yy)) == '#':
                    return False, []
                if wm[(xx, yy)] == '[':
                    new_topmost_boxes.append((xx, yy))
                    new_topmost_boxes.append((xx+1, yy))
                else:
                    new_topmost_boxes.append((xx, yy))
                    new_topmost_boxes.append((xx-1, yy))
            for b in new_topmost_boxes:
                boxes.append(b)
            topmost_boxes = new_topmost_boxes

        return True, boxes


def print_warehouse_map(wm, width, height, p):
    for y in range(height):
        for x in range(width):
            if (x, y) == p:
                print('@', end='')
            elif (x, y) not in wm:
                print('.', end='')
            else:
                print(wm[(x, y)], end='')
        print()

def part2(warehouse, instructions):
    warehouse = widen_warehouse(warehouse)
    wm, robot_position = to_warehouse_map(warehouse)
    width = len(warehouse[0])
    height = len(warehouse)
    
    for instr in instructions:
        can_move, boxes = peek_ahead_wide(robot_position, DIRECTIONS[instr], wm)
        if can_move:
            # move the boxes in the same direction
            moved_boxes = []
            dx, dy = DIRECTIONS[instr]
            for x,y in boxes:
                if (x, y) in wm:
                    moved_boxes.append((x+dx, y+dy, wm[(x, y)]))
                    del wm[(x, y)]
            for x,y, c in moved_boxes:
                wm[(x, y)] = c
            robot_position = (robot_position[0] + dx, robot_position[1] + dy)
    
    # print('FINAL:')
    # print_warehouse_map(wm, width, height, robot_position)

    total = 0
    for (x, y), c in wm.items():
        if c == '[':
            total += 100*y + x

    return total


print('Part 1:', part1(*read_input('input')))
print('Part 2:', part2(*read_input('input')))
