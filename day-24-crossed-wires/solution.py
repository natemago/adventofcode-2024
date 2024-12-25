def read_input(fn):
    with open(fn) as f:
        ast = {}
        for line in f:
            if line.strip():
                if '->' in line:
                    p1, res = line.split('->')
                    a, op, b = p1.strip().split()
                    ast[res.strip()] = ('expr', a, op, b)
                elif ':' in line:
                    wire, value = line.split(':')
                    ast[wire.strip()] = ('value', int(value.strip()))
                else:
                    raise Exception(line)
        return ast


def solve_for(wire, ast):
    val = ast[wire]
    if val[0] == 'value':
        return val[1]
    _, a, op, b = val
    a = solve_for(a, ast)
    b = solve_for(b, ast)
    if op == 'AND':
        return 1 if a == 1 and b == 1 else 0
    elif op == 'OR':
        return 1 if a == 1 or b == 1 else 0
    elif op == 'XOR':
        return 1 if a !=  b else 0
    raise Exception('Invalid operation: ' + op)

def part1(ast):
    result = []
    for key in ast.keys():
        if key.startswith('z'):
            result.append((key, solve_for(key, ast)))
    
    result = sorted(result)
    total = 0
    for i, (_, v) in enumerate(result):
        total += v*(2**i)
    return total

def part2(ast):
    c = 0
    for key in ast.keys():
        if key[0] in 'xyz':
            pass
        else:
            c+=1
    return c

#print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))
