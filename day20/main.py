import networkx as nx


def get_point(grid, p):
    x, y = p
    return grid[x][y]


def get_opposite_neighbor(p, n):
    x, y = p
    x1, y1 = n
    if x == x1:
        if y1 > y:
            return x, y - 1
        return x, y + 1
    else:
        if x1 > x:
            return x - 1, y
    return x + 1, y


def check_outer(p, grid):
    row, col = p
    max_width = max(map(len, grid))
    if row == 1 or col == 1 or col == max_width - 2 or row == len(grid) - 2:
        return True
    return False


level = 100


def get_neighbors(grid, r, c):
    neighbors = []
    if r > 0 and len(grid[r - 1]) > c:
        neighbors.append((r - 1, c))
    if c > 0:
        neighbors.append((r, c - 1))
    if r < len(grid) - 1 and len(grid[r + 1]) > c:
        neighbors.append((r + 1, c))
    if c < len(grid[r]) - 1:
        neighbors.append((r, c + 1))
    return set(neighbors)


def handle_letter(grid, r, c, g: nx.Graph):
    letter = grid[r][c]
    neighbors = get_neighbors(grid, r, c)
    if not any(map(lambda x: grid[x[0]][x[1]] == '.', neighbors)):
        return
    else:
        for n in neighbors:
            if get_point(grid, n) == '.':
                other_letter = get_point(grid, get_opposite_neighbor((r, c), n))
                letter += other_letter
                for i in range(level):
                    if (n[0], n[1], i) not in g:
                        g.add_node((n[0], n[1], i))
                if (letter, 0) in G:
                    letter = letter[::-1]
                for i in range(level):
                    g.add_node((letter, i), outer=check_outer((r, c), grid))
                    g.add_edge((letter, i), (n[0], n[1], i), weight=0)


def construct_graph():
    with open('input') as f:
        maze = [[c for c in s if c != '\n'] for s in f.readlines()]
        graph = nx.Graph()
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if maze[i][j] == '.':
                    p = i, j
                    graph.add_node((i, j))
                    neighbors = get_neighbors(maze, i, j)
                    for n in neighbors:
                        row, col = n
                        if maze[row][col] == '.':
                            for lev in range(level):
                                if n not in graph:
                                    graph.add_node((n[0], n[1], lev))
                                graph.add_edge((n[0], n[1], lev), (p[0], p[1], lev), weight=1)
                        elif maze[row][col] != '#' and maze[row][col] != '#':
                            handle_letter(maze, row, col, graph)
        for n in graph.nodes:
            if isinstance(n[0], str) and n[0] != 'AA' and n[0] != 'ZZ':
                assert graph.nodes.data()[n]['outer'] != graph.nodes.data()[(n[0][::-1], n[1])]['outer']

        for n in graph.nodes:
            if isinstance(n[0], str) and n[0] != 'AA' and n[0] != 'ZZ':
                outer = graph.nodes.data()[n]['outer']
                label, lev = n
                if outer and lev > 0:
                    graph.add_edge(n, (label[::-1], lev - 1), weight=1)
                if (not outer) and lev < level - 1:
                    graph.add_edge(n, (label[::-1], lev + 1), weight=1)
        return graph


G = construct_graph()

total, path = nx.single_source_dijkstra(G, source=('AA', 0), target=('ZZ', 0), weight='weight')
