def read_input(fn):
    reports = []
    with open(fn) as f:
        for line in f:
            reports.append([int(v) for v in line.strip().split()])
    return reports


def is_safe(report):
    safe = True
    p = report[0]
    increasing = None
    for n in report[1:]:
        if increasing == None:
            increasing = (n-p) > 0
        if abs(n-p) == 0 or abs(n-p) > 3:
            safe = False
            break
        if increasing:
            if (n-p) < 0:
                safe = False
                break
        else:
            if (n-p) > 0:
                safe = False
                break
        p = n
    return safe


def part1(reports):
    safe_reports = 0
    for report in reports:
        if is_safe(report):
            safe_reports += 1
    return safe_reports


def part2(reports):
    safe_reports = 0
    for report in reports:
        if is_safe(report):
            safe_reports += 1
            continue
        any_safe = False
        for i in range(len(report)):
            if is_safe(report[0:i] + report[i+1:]):
                any_safe = True
                break
        if any_safe:
            safe_reports += 1

    return safe_reports


print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))
        