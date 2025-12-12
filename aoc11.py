#!/usr/bin/env python3

from math import prod

import networkx as nx
from funcy import pairwise

from aoc_util import AOC, run_aoc


def create_graph(input):
    g = nx.DiGraph()
    for line in input.splitlines():
        node, *outputs = line.split()
        node = node[:-1]
        g.add_edges_from((node, o) for o in outputs)
    return (g,)


def aoc11(g: nx.DiGraph) -> AOC:
    def count_paths(g, s, t):
        if s in g and t in g:
            # note g is a DAG; enumerating simple_paths would be way too slow
            subg = g.subgraph(nx.descendants(g, s) & nx.ancestors(g, t) | {s, t})
            nodes = nx.topological_sort(subg)
            npaths = {next(nodes): 1}
            for node in nodes:
                npaths[node] = sum(npaths[p] for p in subg.predecessors(node))
            return npaths[t]
        else:
            return 0

    def count_paths_2_extra(g, *waypoints):
        if any(n not in g for n in waypoints):
            return 0
        else:
            # again g is a DAG, there can be only one order the middle nodes
            # are traversed
            if not nx.has_path(g, *waypoints[1:3]):
                waypoints[1:3] = waypoints[1:3][::-1]
            # and absent cycles, the legs are independent
            legs = (count_paths(g, n1, n2) for n1, n2 in pairwise(waypoints))
            return prod(legs)

    assert nx.is_directed_acyclic_graph(g), "not a DAG"
    yield count_paths(g, "you", "out")
    yield count_paths_2_extra(g, "svr", "fft", "dac", "out")


if __name__ == "__main__":
    run_aoc(aoc11, transform=create_graph)
