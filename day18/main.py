from typing import Set, Tuple

import networkx as nx
import itertools
import functools

def add_all_neighbors(graph: nx.Graph, grid, p):
    x, y = p
    neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    graph.add_node(p, name=grid[y][x])
    for n in neighbors:
        a, b = n
        if grid[b][a] != '#':
            if n not in graph:
                graph.add_node(n, name=grid[b][a])
            graph.add_edge(p, n)


def parse_input():
    keys = {}
    doors = {}
    pos = None
    graph = nx.Graph()
    with open('input') as f:
        grid = [[c for c in s.strip()] for s in f.readlines()]
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                tile = grid[y][x]
                if tile == '@':
                    pos = (x, y)
                elif tile == '#':
                    continue
                else:
                    add_all_neighbors(graph, grid, (x, y))
                    if tile.islower():
                        keys[(x, y)] = tile
                    elif tile.isupper():
                        doors[(x, y)] = tile
    graph = nx.relabel_nodes(graph, doors)
    graph = nx.relabel_nodes(graph, keys)
    return graph, pos, set(doors.values()), set(keys.values())


def can_reach(target, source, obtained_keys, apsp):
    path = apsp[source][target]
    for n in path:
        if isinstance(n, str) and n.isupper():
            if not n.lower() in obtained_keys:
                return False
    return True


def get_reachable_keys(pos, keys, obtained_keys, apsp):
    return {k for k in keys if can_reach(k, pos, obtained_keys, apsp)}.difference(obtained_keys)

def get_distance_to_keys(pos, keys, obtained_keys, apsp):
    return {k: len(apsp[pos][k]) -1 for k in keys.difference(obtained_keys) if can_reach(k, pos, obtained_keys, apsp)}

def play_game(pos, obtained_keys: Set, keys: Set, apsp):
    print("Game: {} - {} - {}".format(pos, obtained_keys, keys.difference(obtained_keys)))
    if keys.issubset(obtained_keys):
        return 0
    reachable = get_distance_to_keys(pos, keys, obtained_keys, apsp)
    distances = map(lambda x: reachable[x] + play_game(x, obtained_keys.union(set(x)), keys, apsp), reachable.keys())
    return min(distances)



g, pos, doors, keys = parse_input()
relevant_nodes = {v for v in doors}.union(v for v in keys).union({pos})
apsp = dict()
for t in list(itertools.product(list(relevant_nodes),list(relevant_nodes))):
    u, v = t
    if u not in apsp:
        apsp[u] = dict()
    apsp[u][v] = nx.shortest_path(g, u, v)
print(play_game(pos, set(), keys, apsp))