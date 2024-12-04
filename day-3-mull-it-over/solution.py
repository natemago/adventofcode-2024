import re

def read_input(fn):
    mem_lines = []
    with open(fn) as f:
        for line in f:
            if line.strip() != '':
                mem_lines.append(line.strip())
    return ''.join(mem_lines)


def mul_string(s):
    total = 0
    for m in re.finditer(r'mul\((?P<X>\d+),(?P<Y>\d+)\)', s):
        x = int(m.group('X'))
        y = int(m.group('Y'))
        total += x*y
    return total

def part1(program):
    return mul_string(program)

def tokenize(s):
    tokens = []

    buff = ''
    i = 0
    tkn_type = 'exec'
    while i < len(s):
        if s[i:].startswith('do()'):
            if buff != '':
                tokens.append((buff, tkn_type))
                buff = ''
            tkn_type = 'do'
            i += 4
        elif s[i:].startswith("don't()"):
            if buff != '':
                tokens.append((buff, tkn_type))
                buff = ''
            tkn_type = 'skip'
            i+= 7
        else:
            buff += s[i]
            i += 1
    if buff != '':
        tokens.append((buff, tkn_type))
    return tokens

def part2(program):
    programs = []
    with open('input') as f:
        for line in f:
            if line.strip() != '':
                programs.append(line.strip())
    on = True
    executable = []
    for program in programs:
        #print('Line:', program)
        tokens = tokenize(program)
        #print(tokens)
        for i, (tkn, tp) in enumerate(tokens):
            if tp == 'exec' and on:
                executable.append(tkn)
            elif tp == 'do':
                if i < len(tokens) - 1:
                    # check if next token is also 'do'
                    if tokens[i+1][1] == 'do':
                        # skip this one
                        continue
                    else:
                        on = True
                        executable.append(tkn)
                        continue
                on = True
                executable.append(tkn)
            elif tp == "skip":
                if i < len(tokens) - 1:
                    # check if next token is also 'skip'
                    if tokens[i+1][1] == 'skip':
                        if on:
                            # we can execute this one...
                            executable.append(tkn)
                        continue
                    else:
                        on = False
                        continue
                on = False

        return sum([mul_string(exec_str) for exec_str in executable])



print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))
