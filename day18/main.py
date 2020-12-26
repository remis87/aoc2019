from typing import Set, Tuple

import networkx as nx
import itertools
import functools
import multiprocessing

pool = multiprocessing.Pool()


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
    pos = []
    graph = nx.Graph()
    with open('input') as f:
        grid = [[c for c in s.strip()] for s in f.readlines()]
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                tile = grid[y][x]
                if tile == '@':
                    pos.append((x, y))
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
    return graph, tuple(pos), set(doors.values()), set(keys.values())


def can_reach(target, source, obtained_keys):
    global keys_needed_on_path
    global shortest_paths
    key_needed = keys_needed_on_path[source][target]
    if 'unreachable' not in key_needed:
        return key_needed.issubset(obtained_keys)
    return False


def get_reachable_keys(pos, obtained_keys, apsp):
    global keys
    return {k for k in keys if can_reach(k, pos, obtained_keys, apsp)}.difference(obtained_keys)


def get_distance_to_keys(pos, obtained_keys, apsp):
    return {k: len(apsp[pos][k]) - 1 for k in keys.difference(obtained_keys) if can_reach(k, pos, obtained_keys) and len(apsp[pos][k]) > 0}


def get_reachable_for_several_pos(positions, obtained_keys):
    reachable = {}
    for i, pos in enumerate(positions):
        reachable[i] = get_distance_to_keys(pos, obtained_keys, shortest_paths)
    return reachable
seen = {}


def play_game(positions, obtained_keys):
    global shortest_paths
    global keys
    global doors
    obtained_str = ''.join(sorted(obtained_keys))
    if obtained_keys == keys:
        seen[(positions, obtained_str)] = 0
        return 0
    if (positions, obtained_str) in seen:
        return seen[(positions, obtained_str)]
    reachable = get_reachable_for_several_pos(positions, obtained_keys)
    next_args = []
    for i in reachable.keys():
        for key in reachable[i].keys():
            new_pos = [x for x in positions]
            new_pos[i] = key
            next_args.append((i, tuple(new_pos), obtained_keys.union(key)))
    possibilities = []
    for a in next_args:
        idx = a[0]
        new_pos = a[1][a[0]]
        distance = reachable[idx][new_pos]
        possibilities.append(distance + play_game(a[1], a[2]))
    ret = min(possibilities)

    seen[(positions, obtained_str)] = ret
    return min(possibilities)


g, pos, doors, keys = parse_input()
relevant_nodes = {v for v in doors}.union(v for v in keys).union(set(pos))
shortest_paths = dict()
keys_needed_on_path = dict()
for t in list(itertools.product(list(relevant_nodes), list(relevant_nodes))):
    u, v = t
    if u not in shortest_paths:
        shortest_paths[u] = dict()
        keys_needed_on_path[u] = dict()
    try:
        shortest_paths[u][v] = set(nx.shortest_path(g, u, v))
        keys_needed_on_path[u][v] = set(map(lambda x: x.lower(), shortest_paths[u][v].intersection(doors)))
    except nx.NetworkXNoPath:
        shortest_paths[u][v] = set()
        keys_needed_on_path[u][v] = set('unreachable')
print(play_game(pos, set()))
