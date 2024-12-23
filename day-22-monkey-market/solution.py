def read_input(fn):
    with open(fn) as f:
        return [int(line.strip()) for line in f if line.strip()]


def next_number(n):
    r = ((n*64) ^ n) % 16777216
    r = ((r//32) ^ r) % 16777216
    r = ((r*2048) ^ r) % 16777216
    return r


def part1(initial_numbers):
    total = 0
    for secret_number in initial_numbers:
        for i in range(2000):
            secret_number = next_number(secret_number)
        total += secret_number
    return total


def part2(initial_numbers):
    all_prices = []
    all_diffrences = []
    for secret_number in initial_numbers:
        player_prices = []
        player_diffrences = []
        prev = secret_number%10
        for i in range(2000):
            secret_number = next_number(secret_number)
            player_prices.append(secret_number%10)
            player_diffrences.append((secret_number%10) - prev)
            prev = secret_number%10


        all_prices.append(player_prices)
        all_diffrences.append(player_diffrences)

    
    all_sequences = {}

    for idx, diffrences in enumerate(all_diffrences):
        sequences = []
        for i in range(len(diffrences) - 3):
            seq = tuple(diffrences[i:i+4])
            price = all_prices[idx][i+3]
            sequences.append((price, seq))
            if seq not in all_sequences:
                all_sequences[seq] = {}
            if all_sequences[seq].get(idx) is None:
                all_sequences[seq][idx] = price
            
            
        
    most_bananas = None
    for _, sells in all_sequences.items():
        s = sum(sells.values())
        if most_bananas is None or s > most_bananas:
            most_bananas = s

    return most_bananas


print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))