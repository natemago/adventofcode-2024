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

def get_reachable(n, ast):
    q = [n]
    reached = set()

    while len(q):
        n = q[0]
        q = q[1:]
        if n in reached:
            continue
        reached.add(n)
        if n not in ast:
            continue
        if ast[n][0] == 'expr':
            _, a, _, b = ast[n]
            q.append(a)
            q.append(b)
    return reached

def part2(ast):
    c = 0
    for key in ast.keys():
        if key[0] in 'xyz':
            pass
        else:
            c+=1
    return c

def run_with(x, y, ast):
    a = {}
    a.update(ast)
    for k in a.keys():
        if k[0] == 'x':
            bit = int(k[1:].lstrip('0') or 0)
            bit = x & (0x1<<bit)
            a[k] = ('value', bit)
        elif k[0] == 'y':
            bit = int(k[1:].lstrip('0') or 0)
            bit = y & (0x1<<bit)
            a[k] = ('value', bit)
    
    result = []
    for k in a.keys():
        if k[0] == 'z':
            result.append((k, solve_for(k, a)))
    result = sorted(result)
    r = 0
    for i, bit in enumerate(result):
        r += (2**i) * bit[1]
    return r, result
    
    

def part2(ast):
    reached = {}
    for n in ast.keys():
        
        if n[0] == 'z':
            reached[n] = get_reachable(n, ast)
    

    for z, wires in reached.items():
        input_wires = []
        for w in wires:
            if w[0] in 'xy':
                input_wires.append(w)
        input_wires = sorted(input_wires)
        z_bit = int(z[1:].lstrip('0') or 0)
        conn_error = ''
        x_count = 0
        y_count = 0
        for i in input_wires:
            if int(i[1:].lstrip('0') or 0) > z_bit:
                conn_error += '%s not properly connected to %s; ' % (i, z)
            if i[0] == 'x':
                x_count += 1
            else:
                y_count += 1
        if y_count != x_count:
            conn_error += 'mismatch count on x and y inputs; '
        if y_count != (z_bit + 1):
            conn_error += 'invalid conecctions to Y inputs; '
        if x_count != (z_bit + 1):
            conn_error += 'invalid conecctions to X inputs; '
        
        if conn_error:
            print('Output: ', z)
            print(z_bit, '; ', y_count, '; ', x_count)
            print(conn_error)
            print(input_wires)
        else:
            print('Output: ', z, ' OK')
    

    for i in range(45):
        for x, y in ((0, 0), (0, 1), (1, 0), (1, 1)):
            a = (2**i)*x
            b = (2**i)*y
            r, out = run_with(a, b, ast)
            if r != (a+b):
                print('FAILED at bit:', i)
                print('a=', a, '; b=', b, '; (a+b)=', a+b)
                print('but got:', r)
                print(out)
                wires = get_reachable(out[i][0], ast)
                wires1 = get_reachable(out[i+1][0], ast)
                print('wires involved:', wires.union(wires1))
                    
                gates = []
                for w in wires.union(wires1):
                    if ast[w][0] == 'expr':
                        gates.append(w)
                print('Gates:', gates)

                # Try swapping

                input()


#print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))
