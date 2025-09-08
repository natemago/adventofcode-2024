import re

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
    

def get_z_bit(b, ast):
    for n in ast.keys():
        if n.startswith('z'):
            if int(n[1:].lstrip('0') or 0) == b:
                return n

def test_bit(b, ast):
    for x, y, expected_bits in ((0, 0, [0]), (0, 1, [1]), (1, 0, [1]), (1, 1, [0, 1])):
        result, _ = run_with(x*(2**b), y*(2**b), ast)
        #print('Test: x=', x*(2**b), '; y=', y*(2**b), '; result=', result)
        zb = get_z_bit(b, ast)
        if result & (2**b) != expected_bits[0]*(2**b):
            #print(' - fail [1]')
            return False
        if len(expected_bits) > 1:
            zb = get_z_bit(b+1, ast)
            if zb is not None and result & (2**(b+1)) != expected_bits[1]*(2**(b+1)):
                # print(' - fail [2]')
                # print(zb)
                # print(result & (2**(b+1)))
                return False
    return True


def swap_and_test(bit, a, b, ast):
    a = {}
    a.update(ast)

    t = a[b]
    a[b] = a[a]
    a[a] = t
    try:
        return test_bit(bit, a)
    except:
        return False
# --------
class V:

    def __init__(self, id_, label, type_, value=None):
        self.id = id_
        self.label = label
        self.type = type_
        self.in_edges = []
        self.out_edges = []
        self.value = value
    
    def __str__(self):
        return 'V({})'.format(self.id)
    
    def __repr__(self):
        return self.__str__()

class E:

    def __init__(self, id_, label, v1, v2):
        self.id = id_
        self.label = label
        self.v1 = v1
        self.v2 = v2

class G:

    def __init__(self):
        self.vertices = {}
        self.edges = {}
    
    def add_vertex(self, v):
        if v.id in self.vertices:
            raise Exception('Vertex already in graph')
        self.vertices[v.id] = v
    
    def add_edge(self, v1, v2, id_, label):
        if (v1.id, v2.id) in self.edges:
            raise Exception('Edge already in graph')
        edge = E(id_, label, v1, v2)
        
        if v1.id not in self.vertices:
            raise Exception('Vertex {} not in graph'.format(v1.id))
        if v2.id not in self.vertices:
            raise Exception('Vertex {} not in graph'.format(v2.id))

        v1.out_edges.append(edge)
        v2.in_edges.append(edge)
        self.edges[(v1.id, v2.id)] = edge
    
    def to_dot_file(self, fn):
        with open(fn, mode='w') as f:
            f.write('digraph G {\n')

            for vx in self.vertices.values():
                f.write('{} [label="{}"];\n'.format(vx.id, vx.label))

            for eg in self.edges.values():
                f.write('{} -> {} [label="{}"];\n'.format(eg.v1.id, eg.v2.id, eg.label))

            f.write('}\n')
    
    def get_input_vertices(self, iop):
        vertices = []
        for vn, v in self.vertices.items():
            if re.match(r'^{}\d+_input$'.format(iop), vn):
                vertices.append(v)
        return vertices

    def get_output_vertices(self):
        vertices = []
        for vn, v in self.vertices.items():
            if re.match(r'^z\d+_output$', vn):
                vertices.append(v)
        return vertices
    
    def calculate(self, x=None, y=None):
        values = {}

        def calculate_for(node):
            if node in values:
                return values[node]
            child_node_values = []
            for edg in node.in_edges:
                v = calculate_for(edg.v1)
                child_node_values.append(v)
            if len(child_node_values) == 1:
                values[node] = child_node_values[0]
                return child_node_values[0]
            elif len(child_node_values) != 2:
                print(child_node_values)
                print(node.id)
                raise Exception('more than two in_edges to: {}'.format(node))
            a, b = child_node_values
            result = None
            if node.value == 'AND':
                result = 1 if a and b else 0
            elif node.value == 'OR':
                result = 1 if a or b else 0
            elif node.value == 'XOR':
                result = 1 if a != b else 0
            else:
                raise Exception('unknown op: {}'.format(node.value))

            values[node] = result
            return result
        
        for i, n in enumerate(self.get_input_vertices('x')):
            values[n] = n.value if x is None else (1 if (x & (2**i)) else 0)
        
        for i, n in enumerate(self.get_input_vertices('y')):
            values[n] = n.value if y is None else (1 if (y & (2**i)) else 0)

        outputs = sorted(self.get_output_vertices(), key=lambda n: n.id)
        result = 0
        for i,n in enumerate(outputs):
            result += (2**i) * calculate_for(n)
        return result
    
    def get_reachable_inv(self, n):
        q = [n]
        reachable = set()

        while len(q):
            n = q[0]
            q = q[1:]
            if n in reachable:
                continue
            reachable.add(n)
            for e in n.in_edges:
                if e.v1 in reachable:
                    continue
                q.append(e.v1)
        
        return reachable
    
    def swap(self, a, b):
        a_out_edges = a.out_edges
        a.out_edges = b.out_edges
        b.out_edges = a_out_edges

        for e in a.out_edges:
            e.v1 = a
        for e in b.out_edges:
            e.v1 = b




def get_io(ast, t):
    result = []
    for key, v in ast.items():
        if key[0] == t:
                result.append(key)
    return sorted(result)


def to_graph(ast):
    xinputs = get_io(ast, 'x')
    yinputs = get_io(ast, 'y')
    zouts = get_io(ast, 'z')

    g = G()


    def _get_vx(k):
        if k in xinputs + yinputs:
            return g.vertices['{}_input'.format(k)]
        if k in zouts:
            return g.vertices['{}_output'.format(k)]
        return g.vertices[k]

    for i in xinputs + yinputs:
        v = V('{}_input'.format(i), i, 'input', value=ast[i][1])
        g.add_vertex(v)
    
    for i in zouts:
        v = V('{}_output'.format(i), i, 'output')
        g.add_vertex(v)
    
    for key, v in ast.items():
        if v[0] == 'value':
            continue
        _, a, op, b = v
        vx = V(key, op, 'gate', value=op)
        g.add_vertex(vx)
    
    for key, v in ast.items():
        if v[0] == 'value':
            continue
        _, a, op, b = v
        gate_vx = g.vertices[key]
        a_vx = _get_vx(a)
        b_vx = _get_vx(b)
        g.add_edge(a_vx, gate_vx, (a, key), '{}->{}'.format(a, key))
        g.add_edge(b_vx, gate_vx, (b, key), '{}->{}'.format(b, key))
        if key in zouts:
            z_vx = _get_vx(key)
            g.add_edge(gate_vx, z_vx, (key, key), key)

    return g


# --------

def part2(ast):
    reached = {}
    for n in ast.keys():
        
        if n[0] == 'z':
            reached[n] = get_reachable(n, ast)
    g = to_graph(ast)
    print(g.calculate())

    # Sanity checks
    # inputs should connect to two gates - one XOR and one AND gate
    for n in g.get_input_vertices('x') + g.get_input_vertices('y'):
        assert len(n.out_edges) == 2

    wrong_wires = []

    # Inputs must connect to exactly one XOR and exactly one AND gate
    for n in g.get_input_vertices('x') + g.get_input_vertices('y'):
        wire1, wire2 = n.out_edges
        w1, w2 = wire1.v2, wire2.v2

        if w1.type != 'gate':
            wrong_wires.append(wire1)
            continue
        if w2.type != 'gate':
            wrong_wires.append(wire2)
            continue
        
        gates_types_ok = True
        if w1.value not in ('XOR', 'AND'):
            wrong_wires.append(wire1)
            gates_types_ok = False
        if w2.value not in ('XOR', 'AND'):
            wrong_wires.append(wire2)
            gates_types_ok = False
        if gates_types_ok and w1.value == w2.value:
            gates_types_ok = False
            if w1.value == 'XOR':
                wrong_wires.append(wire2)
            else:
                wrong_wires.append(wire1)
        xor_gate = w1 if w1.value == 'XOR' else (w2 if w2.value == 'XOR' else None)
        if xor_gate:
            # must connect to exactly two inputs
            if len(xor_gate.in_edges) == 2:
                in1, in2 = xor_gate.in_edges
                if not in1.v1.id.endswith('_input'):
                    wrong_wires.append(in1)
                if not in2.v1.id.endswith('_input'):
                    wrong_wires.append(in2)
                if in1.v1 == in2.v1:
                    print('CANNOT INP FROM SAME INPUT!')
                    wrong_wires.append(in1)
                    wrong_wires.append(in2)
            else:
                print('WRONG NUMBER OF IN TO XOR')
        and_gate = w1 if w1.value == 'AND' else (w2 if w2.value == 'AND' else None)

        if and_gate:
            # must connect to exactly two inputs
            if len(xor_gate.in_edges) == 2:
                in1, in2 = xor_gate.in_edges
                if not in1.v1.id.endswith('_input'):
                    wrong_wires.append(in1)
                if not in2.v1.id.endswith('_input'):
                    wrong_wires.append(in2)
                if in1.v1 == in2.v1:
                    print('CANNOT INP FROM SAME INPUT!')
                    wrong_wires.append(in1)
                    wrong_wires.append(in2)
            else:
                print('WRONG NUMBER OF IN TO AND')
        
    
    print('wrong wires:', wrong_wires)
    g.to_dot_file('circuit.dot')

    def _check_addition_at_bit(n):
        for x in [0, 2**n]:
            for y in [0, 2**n]:
                try:
                    z = g.calculate(x, y)
                    exp = x+y
                    if exp != z:
                        print('Failure at bit {} - expected {}, but got {}'.format(n, exp, z))
                        return False
                except RecursionError:
                    # circular circuit
                    return False
        return True

    

    outs = g.get_output_vertices()
    swapped = set()
    def ordp(a, b):
        return (a, b) if a < b else (b, a)

    while True:
        print('----')
        failure_on_bits = []

        for i in range(len(g.get_input_vertices('x'))):
            print('checking addition for bit:', i)
            if not _check_addition_at_bit(i):
                failure_on_bits.append(i)
        print('Failure on bits:', failure_on_bits)
        if not len(failure_on_bits):
            break

        successful = {}
        for i in failure_on_bits:
            print('Failure on:', outs[i])
            potentials = [n for n in g.get_reachable_inv(outs[i]).union(g.get_reachable_inv(outs[i+1])).union(g.get_reachable_inv(outs[i-1])).difference(g.get_reachable_inv(outs[i-2])) if n.type == 'gate']
            print('  - potential:',len(potentials),  potentials)
            
            from itertools import combinations

            for (a, b) in combinations(potentials, 2):
                g.swap(a, b)

                if _check_addition_at_bit(i):
                    print('  - success with:', (a, b))
                    successful[i] = successful.get(i, [])
                    successful[i].append((a, b))
                g.swap(a, b) # swap back, check with other pair

        print('Success:', successful)
        print(len(successful))
        print('success at bits:', successful.keys())
        input()

        from itertools import product

        def in_group(pair, group):
            a, b = pair
            for pp in group:
                if a in pp or b in pp:
                    return True
            return False


        for possible in product(*list(successful.values())):
            # merge
            pairs_groups = []
            print(" ** possible:", possible)
            for p in possible:
                added = False
                for group in pairs_groups:
                    if in_group(p, group):
                        group.append(p)
                        added = True
                        break

                # not in any group - append in new group
                if not added:
                    pairs_groups.append([p])
            print(pairs_groups)
            #input('...')
            # if len(pairs_groups) != 4:
            #     continue # not a solution
            for pairs in product(*pairs_groups):
                print('Pairs to test:', pairs)
                g = to_graph(ast)
                for p in pairs:
                    a, b = p
                    g.swap(a, b)
                
                # test all bits if it works:
                is_solution = True
                for i in range(len(g.get_input_vertices('x'))):
                    if not _check_addition_at_bit(i):
                        is_solution = False
                        break
                
                if is_solution:
                    print('Solution! Yay!')
                    print(pairs)
                    result = []
                    for a, b in pairs:
                        result.append(a.id)
                        result.append(b.id)
                    
                    # do a final check
                    print(' -- Final check --')
                    g = to_graph(ast)
                    for a, b in pairs:
                        g.swap(a, b)
                        print(' - swapped: ', a, '<->', b)
                    print(' * checking with powers of 2')
                    xinps = g.get_input_vertices('x')
                    for i in range(len(xinps)):
                        for xx, yy in product((0,1), (0,1)):
                            x = xx*(2**i)
                            y = yy*(2**i)
                            r = g.calculate(x, y)
                            print(x, '+', y, '=', r, '; correct=', x+y)
                            assert r == (x+y)
                    


                    return ','.join(sorted(result))
                # swap back
                for p in pairs:
                    a, b = p
                    g.swap(a, b)
        return

    
    # sketch of solution approach:
    '''
    def check_at_bit(i):
        # all bits before i are set correctly
        ok_gates = graph.gates(i-1)
        
        curr_bit = i
        while not ok:
            curr_gates = graph.gates(curr_bit) - ok_gates
            # try swapping a pair in the gates
            for pair in choose_2_of_gates(curr_gates):
                graph.swap(pair)
                
                test graph at bit i
                if correct:
                    return pair
                graph.swap(pair) # swap back
                # conitnue with the next pair
            # if here, no pair was found so expand search to next bit gates
            curr_bit += 1
            if curr_bit > length of output wires:
                raise Exception('we cannot fix the bit at', i)
    
    # start at bit 0, then try to fix all bits one by one
    bit = 0
    swapped = []
    while bit <= leght of output bits:
        pair = check_at_bit(bit)
        swapped.append(pair)
    return swapped
    '''
    
    result = []
    for (a, b) in swapped:
        result.append(a.id)
        result.append(b.id)
    
    return ','.join(sorted(result))

#print('Part 1:', part1(read_input('input')))
#print('Part 2:', part2(read_input('input')))
#part2(read_input('day-24-crossed-wires/input'))
print('Part 2:', part2(read_input('input')))
