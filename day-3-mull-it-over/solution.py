import re

def read_input(fn):
    mem_lines = []
    with open(fn) as f:
        for line in f:
            if line.strip() != '':
                mem_lines.append(line.strip())
    return ''.join(mem_lines)


def read_input2(fn):
    mem_lines = []
    with open(fn) as f:
        for line in f:
            if line.strip() != '':
                mem_lines.append(line.strip())
    return mem_lines

def mul_string(s):
    total = 0
    for m in re.finditer(r'mul\((?P<X>\d+),(?P<Y>\d+)\)', s):
        x = int(m.group('X'))
        y = int(m.group('Y'))
        total += x*y
    return total


def part1(program):
    return mul_string(program)


def get_instructions(s):
    return re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", s)

def part2(programs):
    instructions = []
    for program in programs:
        instructions += get_instructions(program)
    
    result = 0
    on = True
    for i, instr in enumerate(instructions):
        if instr == 'do()':
            on = True
        elif instr == "don't()":
            on = False
        else:
            m = re.match(r'mul\((\d+),(\d+)\)', instr)
            if not m:
                raise Exception('Invalid instruction:' + instr)
            x = int(m.group(1))
            y = int(m.group(2))
            if on:
                result += x*y
    return result

print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input2('input')))
