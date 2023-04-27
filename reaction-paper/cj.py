# %%
import gzip
import json
import networkx as nx
import itertools
import scipy
import matplotlib.pyplot as plt
import math
import numpy as np
import collections


def CI_TLS_rec(G, n):
    activated.add(n)

    sigmas = {n: 0}  # activation probabilities

    def sigma(v):
        if v in sigmas:
            return sigmas[v]
        # return 1 - np.prod([1 - ])

    relevant_nodes = collections.defaultdict(set)
    current = set()

    def dfs(i, depth):
        if depth <= 2:
            current.add(i)
            for neighbor in G.neighbors(i):
                if neighbor not in current:
                    relevant_nodes[neighbor] |= current
                    dfs(neighbor, depth + 1)
            current.remove(i)

    # construct depth-set first, do dfs here
    dfs(n, 0)
    print(relevant_nodes)


test_G = nx.Graph()
nodelist = range(1, 10)
edgelist = [[1, 2], [1, 4], [1, 3], [3, 6],
            [3, 5], [6, 9], [5, 8], [5, 7], [4, 6]]


test_G.add_nodes_from(nodelist)
test_G.add_edges_from(edgelist)

CI_TLS_rec(test_G, 1)
