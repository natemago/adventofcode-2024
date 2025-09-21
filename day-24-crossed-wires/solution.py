from random import randint
from itertools import combinations

def read_input(fn):
    global id_seq
    id_seq = 0
    circuit = Circuit()
    inputs_read = False
    with open(fn) as f:
        for line in f:
            line = line.strip()
            if not line:
                if not inputs_read:
                    inputs_read = True
                continue
        
            if not inputs_read:
                # read inputs
                inp, value = line.split()
                w = InputWire(inp[:-1], int(value))
                if w.t == 'x':
                    circuit.inpx.append(w)
                else:
                    circuit.inpy.append(w)
                circuit.wires[w.name] = w
            else:
                p1, p2 = line.split('->')
                p1, p2 = p1.strip(), p2.strip()
                out_wire = circuit.wires[p2] if p2 in circuit.wires else InputWire(p2) if p2.startswith('z') else Wire(p2)
                in1_name, gate_op, in2_name = p1.split()
                in1_wire = circuit.wires[in1_name] if in1_name in circuit.wires else Wire(in1_name)
                in2_wire = circuit.wires[in2_name] if in2_name in circuit.wires else Wire(in2_name)
                gate = Gate(gate_op)
                in1_wire.gates.add(gate)
                in2_wire.gates.add(gate)
                out_wire.gates.add(gate)
                gate.in1 = in1_wire
                gate.in2 = in2_wire
                gate.out = out_wire

                if isinstance(out_wire, InputWire):
                    circuit.outz.append(out_wire)
                circuit.wires[in1_wire.name] = in1_wire
                circuit.wires[in2_wire.name] = in2_wire
                circuit.wires[out_wire.name] = out_wire
                circuit.gates.add(gate)

    circuit.inpx = sorted(circuit.inpx, key=lambda w: w.name)
    circuit.inpy = sorted(circuit.inpy, key=lambda w: w.name)
    circuit.outz = sorted(circuit.outz, key=lambda w: w.name)
    return circuit

OPS = {
    'AND': lambda a, b: a & b,
    'OR': lambda a, b: a | b,
    'XOR': lambda a, b: a ^ b,
}

class Wire:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value
        self.gates = set()
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.__str__()

class InputWire(Wire):

    def __init__(self, name, value=None):
        super(InputWire, self).__init__(name, value)
        self.bit = int(name[1:])
        self.t = name[0]


id_seq = 0


class Gate:

    def __init__(self, op):
        global id_seq
        self.id = id_seq
        id_seq += 1
        self.op = op
        self.in1 = None
        self.in2 = None
        self.out = None
    
    def __str__(self):
        return self.op + str(self.id)
    
    def __repr__(self):
        return self.__str__()
    
    def run(self):
        if self.in1.value is None:
            for gate in self.in1.gates:
                if self.in1.value is not None:
                    # already set
                    continue
                if gate == self:
                    continue
                if gate.out == self.in1:
                    self.in1.value = gate.run()
        if self.in2.value is None:
            for gate in self.in2.gates:
                if self.in2.value is not None:
                    # already set
                    continue
                if gate == self:
                    continue
                if gate.out == self.in2:
                    self.in2.value = gate.run()
        if self.in1.value is not None and self.in2.value is not None:
            v =  OPS[self.op](self.in1.value, self.in2.value)
            return v
        
        raise Exception('WOOPS')


class Circuit:
    def __init__(self):
        self.inpx = []
        self.inpy = []
        self.outz = []
        self.wires = dict()
        self.gates = set()
    
    def run(self, lbit=0, hbit=None):
        hbit = hbit if hbit is not None else len(self.outz) - 1
        for o in self.outz[lbit:hbit+1]:
            for gate in o.gates:
                if gate.out == o:
                    o.value = gate.run()
    
    def readout(self):
        return readout(self.outz)
    
    def reset(self):
        for w in self.wires.values():
            w.value = None
        for w in self.inpx:
            w.value = 0
        for w in self.inpy:
            w.value = 0
    
    def setx(self, n):
       setval(n, self.inpx)
    
    def sety(self, n):
       setval(n, self.inpy)
    

    def run_with(self, x, y, lbit=0, hbit=None):
        self.reset()
        self.setx(x)
        self.sety(y)
        self.run()
        return self.readout()
    
    def check_bit(self, bit):
        #print(':: checking bit:', bit)
        try:
            for x, y, r in ((0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 2)):
                n = self.run_with(x*(2**bit), y*(2**bit), lbit=bit, hbit=bit+1)
                # print('  ')
                # print('  :: (expected) {} + {} = {}'.format(x, y, r))
                # print('  :: actual: {} + {} = {}'.format(x*(2**bit), y*(2**bit), n))
                n = (n & (3<<bit))>>bit
                # print('  ::    after shift:', n)
                # print('  :: ', [str(i.value or 0) for i in self.inpx])
                # print('  :: ', [str(i.value or 0) for i in self.inpy])
                # print('  :: ', [str(i.value or 0) for i in self.outz])
                if n != r:
                    return False
            return True
        except Exception as e:
            #print('error:', e)
            return False
    
    def swap_gates(self, g1, g2):
        g1_out = g1.out
        g2_out = g2.out
        # fix back-refs
        g1_out.gates = g1_out.gates.difference({g1}).union({g2})
        g2_out.gates = g2_out.gates.difference({g2}).union({g1})
        # swap outputs
        g1.out = g2_out
        g2.out = g1_out
    
    def _gate_by_name(self, gid):
        for g in self.gates:
            if str(g) == gid:
                return g
        raise Exception('no gate ' + gid)

    def swap_gates_by_name(self, g1, g2):
        self.swap_gates(self._gate_by_name(g1), self._gate_by_name(g2))
    
    def gates_up_to(self, bit):
        gates = set()

        q = []
        for o in self.outz[0:bit+1]:
            for g in o.gates:
                if g not in q:
                    q.append(g)
        
        while len(q):
            gate = q[0]
            q = q[1:]
            if gate in gates:
                continue
            gates.add(gate)
            for wire in (gate.in1, gate.in2):
                for g in wire.gates:
                    if g in gates or g == gate:
                        continue
                    q.append(g)

        return gates
    
    def self_test(self):
        max_bits = len(self.inpx)
        print('Self test (max bits {})'.format(max_bits))
        for bit in range(max_bits):
            if not self.check_bit(bit):
                print(' - failed at bit:', bit)
                return False
        print('- per bit test passed')
        # Test with a couple of random numbers for good measure
        for i in range(50):
            x = randint(0, 2**max_bits)
            y = randint(0, 2**max_bits)
            expected = x+y
            result = self.run_with(x, y)
            if expected != result:
                print(' - failed test {} + {}: expected {} but got {}'.format(x, y, expected, result))
                return False
        print(' * Test passed.')
        return True
    
    def readout_raw(self):
        return '\n'.join([
            'X:  ' + ''.join(reversed([str(i.value or 0) for i in self.inpx])),
            'Y:  ' + ''.join(reversed([str(i.value or 0) for i in self.inpy])),
            'Z: ' + ''.join(reversed([str(i.value or 0) for i in self.outz])),
        ])
    
    def dot_file(self, fn, marked=None):
        with open(fn, mode='w') as f:
            f.write('digraph G {\n')
            # Write nodes

            # first, nodes for input and outputs
            for w in self.inpx:
                f.write('{} [label="{}", fillcolor=aquamarine, style=filled];\n'.format(w.name, w.name))
            for w in self.inpy:
                f.write('{} [label="{}", fillcolor=chartreuse, style=filled];\n'.format(w.name, w.name))
            for w in self.outz:
                f.write('{} [label="{}", fillcolor=darkgoldenrod1, style=filled];\n'.format(w.name, w.name))
            
            # Then all gates
            for g in self.gates:
                gk = str(g)
                color = {
                    'XOR': 'cadetblue1',
                    'AND': 'pink',
                    'OR': 'beige',
                    'marked': 'deeppink',
                }
                f.write('{} [label="{}", fillcolor={}, style=filled];\n'.format(gk, gk, color['marked'] if marked and gk in marked else color[g.op]))
            
            # write edges
            seen = set()
            for g in self.gates:
                for w in (g.in1, g.in2):
                    if isinstance(w, InputWire):
                        f.write('{} -> {} [label="{}"];\n'.format(w.name, str(g), w.name))
                    else:
                        for gg in w.gates:
                            if gg == g:
                                continue
                            # if (str(gg), str(g)) in seen:
                            #     continue
                            # seen.add((str(gg), str(g)))
                            if gg.out != w:
                                continue
                            f.write('{} -> {} [label="{}"];\n'.format(str(gg), str(g), w.name))
                if isinstance(g.out, InputWire):
                    f.write('{} -> {} [label="{}"];\n'.format(str(g), g.out.name, g.out.name))
            f.write('}\n')


def readout(wires):
    n = 0
    for i, w in enumerate(wires):
        n += (2**i)*(w.value or 0)
    return n


def setval(n, wires):
    mask = 1
    i = 0
    while n:
        if i >= len(wires):
            raise Exception('overflow')
        wires[i].value = n & mask
        i += 1
        n >>= 1


def part1(circuit):
    circuit.run()
    return circuit.readout()

def part2(circuit):
    '''
    x_i, y_i -> same XOR gate
        XOR gate -> XOR_2 gate -> z_i
            XOR_2 gate feeds from OR gate
            
    x_i, y_i -> xame AND gate
        AND gate goes to OR gate
            OR -> XOR -> z_(i+1)
    z outputs are output from XOR gate, except the last one (final overflow)
    '''
    # for bit in range(len(circuit.inpx)):
    #     ok = circuit.check_bit(bit)
    #     print('Check bit ', bit, " -> ", ok)
    #     if not ok:
    #         input('...')
    faulty_gates = set()

    # Rule: z outputs are output from XOR gate, except the last one (final overflow)
    for zw in circuit.outz[:-1]:
        if len(zw.gates) != 1:
            print(zw.name, 'has', len(sw.gates))
            raise Exception('error')
        gate = list(zw.gates)[0]
        if gate.op != 'XOR':
            faulty_gates.add(gate)

    # Rule: XOR gate is connected to either both input wires or OR and XOR gates
    for gate in circuit.gates:
        if gate.op == 'XOR':
            if isinstance(gate.out, InputWire) and gate.out.name[0] == 'z':
                continue # normal output to Z
            # It must output to exactly 1 AND and 1 XOR
            out_gates = [g for g in gate.out.gates if g != gate]
            if tuple(sorted([g.op for g in out_gates])) != ('AND', 'XOR'):
                faulty_gates.add(gate)
        elif gate.op == 'OR':
            # final OR gate just points to the last output wire
            if isinstance(gate.out, InputWire) and gate.out == circuit.outz[-1]:
                # OK, points to the last one
                continue
            
            # OR points to AND and XOR
            out_gates = [g for g in gate.out.gates if g != gate]
            if tuple(sorted([g.op for g in out_gates])) != ('AND', 'XOR'):
                faulty_gates.add(gate)
        elif gate.op == 'AND':
            # AND gates must output to OR gate
            out_gates = [g for g in gate.out.gates if g != gate]
            if len(out_gates) != 1:
                faulty_gates.add(gate)
                continue
            if out_gates[0].op != 'OR':
                faulty_gates.add(gate)
    
    print('Faulty gates:', faulty_gates)

    faulty_wires = set()
    for g in faulty_gates:
        faulty_wires.add(g.out)
    print('Faulty wires:', faulty_wires)

    circuit.dot_file('./circuit_orig.dot', marked=set([str(g) for g in faulty_gates]))
    # Sanity check
    assert len(faulty_gates) == 8
    assert len(faulty_wires) == 8

    def find_gate(gid):
        for g in circuit.gates:
            if str(g) == gid:
                return g
        raise Exception(gid)

    # Dirty check
    # faulty_wires = set()
    # for g1, g2 in (('XOR350', 'OR282'), ('AND382', 'XOR231'), ('XOR360', 'AND342'), ('XOR411', 'AND263')):
    #     circuit.swap_gates(find_gate(g1), find_gate(g2))
    #     faulty_wires.add(find_gate(g1).out)
    #     faulty_wires.add(find_gate(g2).out)


    # #circuit.dot_file('./circuit_swapped.dot', marked=set([str(g) for g in faulty_gates]))


    

    
    valid_configs = []
    q = [(0, [])]
    while len(q):
        bit, circuit_swaps = q[0]
        circuit = read_input('input')
        q = q[1:]
        for g1, g2 in circuit_swaps:
            circuit.swap_gates_by_name(g1, g2)
        if bit == len(circuit.inpx) - 1 or len(circuit_swaps) == 4:
            if len(circuit_swaps) == 4:
                print('Checking swaps:', circuit_swaps)
                if circuit.self_test():
                    print('Valid configuration:', circuit_swaps)
                    valid_configs.append(circuit_swaps)
            continue

        while bit < len(circuit.inpx) - 1 and circuit.check_bit(bit):
            bit += 1
        to_bit = bit
        while to_bit < len(circuit.inpx) - 1 and not circuit.check_bit(to_bit):
            to_bit += 1
        print('faulty bits:', bit, '->', to_bit, '; swaps->', circuit_swaps)
        while to_bit < len(circuit.inpx):
            ok_gates = circuit.gates_up_to(bit-1)
            to_check = circuit.gates_up_to(to_bit).difference(ok_gates)
            if to_bit - bit >= 3:
                print("Too much, bail")
                break
            for g1, g2 in combinations(to_check, 2):
                circuit.swap_gates_by_name(str(g1), str(g2))
                all_bits_ok = True
                for bb in range(0, to_bit+1):
                    if not circuit.check_bit(bb):
                        all_bits_ok = False
                        break
                if all_bits_ok:
                    print('Gate swap: ', g1, g2)
                    q.append([to_bit, circuit_swaps + [(str(g1), str(g2))]])
                # restore this swap
                circuit.swap_gates_by_name(str(g1), str(g2))
            to_bit += 1
            if to_bit >= len(circuit.inpx):
                print('Not found :(')
        # restore circuit for next check
        for g1, g2 in circuit_swaps:
            circuit.swap_gates_by_name(str(g1), str(g2))
    # faulty_wires = set()
    # for g1, g2 in (('XOR350', 'OR282'), ('AND382', 'XOR231'), ('XOR360', 'AND342'), ('XOR411', 'AND263')):
    #         circuit.swap_gates(find_gate(g1), find_gate(g2))
    #         faulty_wires.add(find_gate(g1).out)
    #         faulty_wires.add(find_gate(g2).out)
    # print('Self test:', circuit.self_test())
    solutions = set()
    for valid_config in valid_configs:
        circuit = read_input('input')
        print('Valid config:', valid_config)
        wires = []
        for g1, g2 in valid_config:
            wires.append(str(circuit._gate_by_name(g1).out))
            wires.append(str(circuit._gate_by_name(g2).out))
            circuit.swap_gates_by_name(g1, g2)
        test_pass = circuit.self_test()
        print('  * Self test:', test_pass)
        if test_pass:
            solution = ','.join(sorted(wires))
            print('  * Possible option:', solution)
            solutions.add(solution)
    if len(solutions) == 1:
        return solution
    print('There are {} possible solutions, check one of these:'.format(len(solutions)))
    for solution in solutions:
        print(solution)
    return ''

print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))