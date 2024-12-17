def read_input(fn):
    with open(fn) as f:
        return [line.strip() for line in f if line.strip()]


def get_regions(garden):
    tiles_map = {}
    regions = {}
    region_number = 0

    for gy, row in enumerate(garden):
        for gx, c in enumerate(row):
            if (gx, gy) in tiles_map:
                continue
            
            # Flood fill this region
            region_number += 1
            q = [(gx, gy)]
            visited = set()
            while len(q):
                x, y = q[0]
                q = q[1:]
                if (x, y) in visited:
                    continue
                visited.add((x, y))
                for xx, yy in ((x, y-1), (x-1, y), (x, y+1), (x+1, y)):
                    if xx < 0 or xx >= len(row) or yy < 0 or yy >= len(garden):
                        continue
                    if garden[yy][xx] != c:
                        continue
                    q.append((xx, yy))
            regions[region_number] = visited
            for (x, y) in visited:
                tiles_map[(x, y)] = region_number
    return regions


def part1(garden):
    regions = get_regions(garden)
    perimeters = {}
    for reg_id, region in regions.items():
        perimeter = 0
        for (x, y) in region:
            perimeter += 4
            for xx, yy in ((x, y-1), (x-1, y), (x, y+1), (x+1, y)):
                if (xx, yy) in region:
                    perimeter -= 1
        perimeters[reg_id] = perimeter

    total = 0
    for reg_id, perimeter in perimeters.items():
        area = len(regions[reg_id])
        total += perimeter*area
    return total


def part2(garden):
    total = 0
    regions = get_regions(garden)
    for reg_id, region in regions.items():
        convex_corners = 0
        for x, y in region:
            if (x-1, y) not in region and (x, y-1) not in region:
                convex_corners += 1
            if (x+1, y) not in region and (x, y-1) not in region:
                convex_corners += 1
            if (x-1, y) not in region and (x, y+1) not in region:
                convex_corners += 1
            if (x+1, y) not in region and (x, y+1) not in region:
                convex_corners += 1

        concave_corners = set()
        for x, y in region:
            if (x-1, y) not in region and (x-1, y-1) in region and (x, y-1) in region:
                concave_corners.add((x-1, y, 'up-right'))
            if (x-1, y) not in region and (x-1, y+1) in region and (x, y+1) in region:
                concave_corners.add((x-1, y, 'down-right'))
            if (x+1, y) not in region and (x+1, y-1) in region and (x, y-1) in region:
                concave_corners.add((x+1, y, 'up-left'))
            if (x+1, y) not in region and (x+1, y+1) in region and (x, y+1) in region:
                concave_corners.add((x+1, y, 'down-left'))
        
        total += (convex_corners + len(concave_corners)) * len(region)
    return total


print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))
          