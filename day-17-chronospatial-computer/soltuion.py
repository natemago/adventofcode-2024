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
            #print('out>', get_combo_value(operand) % 8)
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


def compare(a, b):
    if len(a) > len(b):
        #print('True(1)')
        return 1
    if len(b) > len(a):
        #print('False(2)')
        return -1
    for i in range(len(a)):
        aa = a[len(a) - i - 1]
        bb = b[len(b) - i - 1]
        #print('compariring ', aa, ' with ', bb, ' at ', i, ' ', len(b) - i - 1)
        if aa != bb:
            if aa > bb:
                return 1
            else:
                return -1
    return 0


def part1(registers, program):
    out = run_program(registers, program)
    return ','.join([str(i) for i in out])



def part2(registers, program):
    start = 0
    end = int('9'*(len(program)-1))
    while True:
        
        i = (start + end) // 2
        
        regs = {}
        regs.update(registers)
        regs['A'] = i
        output = run_program(regs, program)
        
        if output == program:
            return start
        
        print(start, ' | ', i,  ' | ', end)
        print(output)
        print(program)
        print('output > program=', compare(output, program))


        if gt(output, program) >= 0:
            end = i
        else:
            start = i
        
        if abs(start - end) < 2:
            print('OK, stopping here...')
            break
        print(' - - - - - ')
    
    for i in range(start - 1000000, end + 1000000):
        regs = {}
        regs.update(registers)
        regs['A'] = i
        output = run_program(regs, program)
        if output == program:
            return i
        if i % 1000 == 0:
            print(i)
            print('o=', output)
            print('p=', program)
            print(' - - - ')

    #print(gt([3, 3, 3, 7, 3, 1, 1, 6, 0, 3, 2, 7, 3, 5, 2, 5], [2, 4, 1, 5, 7, 5, 1, 6, 0, 3, 4, 1, 5, 5, 3, 0]))

def to_dec(tri):
    r = 0
    for i in range(len(tri)):
        r += (8**i)*tri[i]
    return r


def part2(registers, program):
    coeff = []
    for i in range(to_dec(program) - 100000, to_dec(program) + 100000):
        output = run_program({
            'A': i+1,
            'B': 0,
            'C': 0,
        },program)
        #print(i+1, ': ', to_dec(output), '(', to_dec(program), ')')
        coeff.append(to_dec(output)/(i+1))
        #print(' >', coeff[-1])
    
    avg = sum(coeff)/len(coeff)
    variance = sum([(avg - v)**2 for v in coeff])/len(coeff)
    from math import sqrt
    std_dev = sqrt(variance)
    print('Avg coeff:', sum(coeff)/len(coeff))
    print('Variance:', variance)
    print('STD Dev:', std_dev)


    guess = int(to_dec(program)/avg)
    print('Guess:', guess)
    deviation = int(guess*std_dev)
    print('Offset:', deviation)
    for i in range(guess - deviation - 1000, guess + deviation + 1000):
        output = run_program({
            'A': i,
            'B': 0,
            'C': 0,
        },program)
        if to_dec(output) == to_dec(program):
            return i
        if i % 10000 == 0:
            print(' - - - - ')
            print(output)
            print(program)

# def part2(registers, program):
#     guess = [0 for i in range(len(program))]
#     d = 0
#     stack = [(d, 0)]
#     while len(stack):
#         d, i = stack[-1]
#         guess[-d-1] = i
#         output = run_program({
#             'A': to_dec(guess),
#             'B': 0,
#             'C': 0,
#         },program)
#         print(' - - - - ')
#         print('d:', d)
#         print('Guess:   ', guess)
#         print('Output:  ', output)
#         print('Program: ', program)
#         input()
#         if output[-d-1:] == program[-d-1:]:
#             if d < len(program)-1:
#                 stack.pop()
#                 stack.append((d+1, 0))
#                 print('Stack:', stack)
#                 continue
#         if i + 1 == 8:
#             if d < len(program)-1:
#                 stack.append((d+1, 0))
#         else:
#             stack.append((d, i+1))
#         print('Stack:', stack)
       
#     print(to_dec(guess))
#     return to_dec(guess)

def part2(registers, program):
    guess = [0 for i in range(len(program) + 5)]
    for i in range(500, 520):
        #guess[4] = i
        output = run_program({
            'A': i,
            'B': 0,
            'C': 0,
        }, program)
        #print('Guess:   ', guess)
        print(i)
        print('Output:  ', output)
        print('Program: ', program)
        input()

print('Part 1:', part1(*read_input('input')))
print('Part 2:', part2(*read_input('input')))