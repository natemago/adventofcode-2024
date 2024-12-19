def read_input(fn):
    registers, program = {}, []
    with open(fn) as f:
        for line in f:
            if line.startswith('Register A:'):
                registers['A'] = int(line.strip().split()[2])
            elif line.startswith('Register B:'):
                registers['B'] = int(line.strip().split()[2])
            elif line.startswith('Register C:'):
                registers['C'] = int(line.strip().split()[2])
            elif line.startswith('Program:'):
                program = [int(v.strip()) for v in line.strip().split()[1].split(',')]
    return registers, program


def run_program(registers, program, at_most_output=None):
    memory = program
    output = []

    def get_combo_value(operand):
        if operand < 4:
            return operand
        elif operand == 4:
            return registers['A']
        elif operand == 5:
            return registers['B']
        elif operand == 6:
            return registers['C']
        else:
            raise Exception('OPERAND 7')

    pc = 0
    while True:
        if pc < 0 or pc+1 >= len(memory):
            break # halt
        opcode = memory[pc]
        operand = memory[pc+1]
        if opcode == 0:
            registers['A'] = registers['A'] // (2**get_combo_value(operand))
            pc += 2
        elif opcode == 1:
            registers['B'] = registers['B'] ^ operand
            pc += 2
        elif opcode == 2:
            registers['B'] = get_combo_value(operand) % 8
            pc += 2
        elif opcode == 3:
            if registers['A'] != 0:
                pc = operand
            else:
                pc += 2
        elif opcode == 4:
            registers['B'] = registers['B'] ^ registers['C']
            pc += 2
        elif opcode == 5:
            output.append(get_combo_value(operand) % 8)
            pc += 2
            if at_most_output is not None and len(output) >= at_most_output:
                break
        elif opcode == 6:
            registers['B'] = registers['A'] // (2**get_combo_value(operand))
            pc += 2
        elif opcode == 7:
            registers['C'] = registers['A'] // (2**get_combo_value(operand))
            pc += 2
        else:
            raise Exception('INVALID OPCODE:' + str(opcode))

    return output


def part1(registers, program):
    out = run_program(registers, program)
    return ','.join([str(i) for i in out])


def part2(registers, program):
    # for i in range(100):
    #     output = run_program({
    #             'A': i,
    #             'B': 0,
    #             'C': 0,
    #         }, program)
    #     print('i=', i)
    #     print(output)
    #     print(program)
    #     print('---')
    '''
    Observations from the output:
        i= 0
        [3]
        [2, 4, 1, 5, 7, 5, 1, 6, 0, 3, 4, 1, 5, 5, 3, 0]
        ...
            i= 7
        [5]
        [2, 4, 1, 5, 7, 5, 1, 6, 0, 3, 4, 1, 5, 5, 3, 0]
        ---
        i= 8
        [3, 2] <- one more digit here...
        [2, 4, 1, 5, 7, 5, 1, 6, 0, 3, 4, 1, 5, 5, 3, 0]
        ---
        ...
        i= 63
        [3, 5]
        [2, 4, 1, 5, 7, 5, 1, 6, 0, 3, 4, 1, 5, 5, 3, 0]
        ---
        i= 64
        [1, 3, 2]
        [2, 4, 1, 5, 7, 5, 1, 6, 0, 3, 4, 1, 5, 5, 3, 0]
        ---
        ...

    1) The output seems to "jump" i.e get one more digit at exactly powers of 8 - so at 8**1 gets 2 digits, at 8^2 gets 3 digits etc.
       This would mean that our number should be at least 8^15 and at most 7*(8^15).
    2) The digit at location N (corresponds to 8^(N-1)) only changes for multiples of 8^(N-1) - in between it remains the same.
    3) From 1 and 2, we can tell that any number N such that (k-1)*(8^d) < N < k*(8^d) will not affect the digit at position d+1 - i.e 
       once we find a number for the (d+1) position, we can try with any number i in [0, 7] as i*(8^d) and the digit after it will not be affected.
       We can have more than one possible hit for i - for example we can have i=1 and i=5 to produce the same digit at the d-th position.

    So we can start by finding possible coefficients (i) for the last position first, then for each of those, we can try other numbers for the previous
    digit recursively. Note that the numbers at position d do NOT affect numbers at position > d, but DO affect numbers before it. 
    '''
    
    
    
    d = len(program) - 1
    q = []

    for i in range(8):
        output = run_program({
                'A': i*(8**d),
                'B': 0,
                'C': 0,
            }, program)
        # print(i)
        # print(output)
        # print(program)
        # print('---')
        if len(output) != len(program):
            continue
        if output[d] == program[d]:
            q.append((d, i, i*(8**d)))

    min_n = None

    while len(q):
        d, i, n = q.pop()
        if d == 0:
            if min_n is None or n < min_n:
                min_n = n
            continue
        for j in range(8):
            output = run_program({
                'A': n + int(j*(8**(d-1))),
                'B': 0,
                'C': 0,
            }, program)
            if len(output) != len(program):
                continue
            if output[(d-1)] == program[(d-1)]:
                q.append((d-1, j, n + int(j*(8**(d-1)))))
    

    # output = run_program({
    #     'A': min_n,
    #     'B': 0,
    #     'C': 0,
    # }, program)
    # print(output)
    # print(program)
    # print('---')
    return min_n


print('Part 1:', part1(*read_input('input')))
print('Part 2:', part2(*read_input('input')))