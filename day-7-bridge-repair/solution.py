from itertools import product


def read_input(fn):
    equations = []
    with open(fn) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            result, numbers = line.split(':')
            result = int(result)
            numbers = [int(n.strip()) for n in numbers.split() if n.strip()]
            equations.append((result, numbers))
    return equations


def part1(equations):
    total = 0
    for result, numbers in equations:
        for operations in product('*+', repeat=len(numbers) - 1):
            test_val = numbers[0]
            for i, operator in enumerate(operations):
                if operator == '+':
                    test_val += numbers[i+1]
                elif operator == '*':
                    test_val *= numbers[i+1]
                else:
                    raise Exception('unknown op:' + operator)
            if test_val == result:
                total += result
                break
    return total


def part2(equations):
    total = 0
    for result, numbers in equations:
        for operations in product('*+|', repeat=len(numbers) - 1):
            test_val = numbers[0]
            for i, operator in enumerate(operations):
                if operator == '+':
                    test_val += numbers[i+1]
                elif operator == '*':
                    test_val *= numbers[i+1]
                elif operator == '|':
                    test_val = int(str(test_val) + str(numbers[i+1]))
                else:
                    raise Exception('unknown op:' + operator)
            if test_val == result:
                total += result
                break
    return total


print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))