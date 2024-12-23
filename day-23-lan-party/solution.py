def read_input(fn):
    with open(fn) as f:
        g = {}
        for line in f:
            line = line.strip()
            if not line:
                continue
            c1, c2 = line.split('-')
            if c1 not in g:
                g[c1] = []
            if c2 not in g:
                g[c2] = []
            g[c1].append(c2)
            g[c2].append(c1)
        return g

def part1(graph):
    triplets = set()
    for n1, nodes in graph.items():
        if n1[0] == 't':
            for n2 in nodes:
                for n3 in nodes:
                    if n2 != n3 and n2 in graph[n3]:
                        triplet = tuple(sorted([n1, n2, n3]))
                        triplets.add(triplet)
    return len(triplets)


def part2(graph):
    most = None
    best_tuple = None
    for n in graph.keys():
        q = [n]
        seen = set()
        while len(q):
            node = q[0]
            q = q[1:]
            if node in seen:
                continue
            can_add = True
            for s in seen:
                if node not in graph[s]:
                    can_add = False
                    break
            if not can_add:
                continue
            seen.add(node)

            for connection in graph[node]:
                all_connected = True
                for s in seen:
                    if connection not in graph[s]:
                        all_connected = False
                        break
                if not all_connected:
                    continue
                
                q.append(connection)
        
        if most is None or len(seen) > most:
            most = len(seen)
            best_tuple = seen

    return ','.join(sorted(best_tuple))



print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))
