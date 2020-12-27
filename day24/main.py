def get_neighbor(r, c, d):
    neighbors = {(r - 1, c, d), (r + 1, c, d), (r, c - 1, d), (r, c + 1, d)}
    neighbors = set(filter(lambda x: 0 <= x[0] < len(grid) and 0 <= x[1] < len(grid[r]), neighbors))
    if (2, 2, d) in neighbors:
        neighbors.remove((2, 2, d))
    if r == 0:
        neighbors.add((1, 2, d - 1))
    if c == 0:
        neighbors.add((2, 1, d - 1))
    if r == 4:
        neighbors.add((3, 2, d - 1))
    if c == 4:
        neighbors.add((2, 3, d - 1))
    if r == 1 and c == 2:
        for i in range(5):
            neighbors.add((0, i, d + 1))
    if r == 3 and c == 2:
        for i in range(5):
            neighbors.add((4, i, d + 1))
    if r == 2 and c == 1:
        for i in range(5):
            neighbors.add((i, 0, d + 1))
    if r == 2 and c == 3:
        for i in range(5):
            neighbors.add((i, 4, d + 1))
    return neighbors


def print_bug_set(d):
    level_bugs = [(x, y) for (x, y, z) in bugs if z == d]
    for i in range(len(grid)):
        r = ''
        for j in range(len(grid[i])):
            if (i, j) in level_bugs:
                r += '#'
            elif (i, j) != (2, 2):
                r += '.'
            else:
                r += '?'
        print(r)


with open('input') as f:
    grid = [[x for x in s.strip()] for s in f.readlines()]


def get_score(row, col, d):
    n = row * len(grid[0]) + col
    return pow(2, n)


bugs = set()
empty = set()
for row in range(len(grid)):
    for col in range(len(grid[row])):
        if grid[row][col] == '#':
            bugs.add((row, col, 0))
        else:
            empty.add((row, col, 0))

print(print_bug_set(0))
for _ in range(200):
    all_neighbors = set()
    for bug in bugs:
        all_neighbors.update(get_neighbor(*bug))
        all_neighbors.add(bug)
    bugs_to_visit = all_neighbors.intersection(bugs)
    tiles_to_visit = all_neighbors.difference(bugs)
    dead_bugs = set()
    newly_infested = set()
    for bug in bugs_to_visit:
        nx = get_neighbor(*bug)
        if len(nx.intersection(bugs)) != 1:
            dead_bugs.add(bug)
    for tile in tiles_to_visit:
        nx = get_neighbor(*tile)
        inf_n = nx.intersection(bugs)
        if len(inf_n) == 1 or len(inf_n) == 2:
            newly_infested.add(tile)
    bugs.difference_update(dead_bugs)
    bugs.update(newly_infested)
print(bugs)
print(len(bugs))
print(print_bug_set(0))