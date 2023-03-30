# %%
import gzip
import json
import networkx as nx
import itertools
# import scipy
import matplotlib.pyplot as plt
import math
import numpy as np
import collections

activated = set()
beta = 0.5

test_G = nx.Graph()
nodelist = range(1, 10)
edgelist = [[1, 2], [1, 4], [1, 3], [3, 6],
            [3, 5], [6, 9], [5, 8], [5, 7], [4, 6]]


test_G.add_nodes_from(nodelist)
test_G.add_edges_from(edgelist)

degs = {n: test_G.degree(n) for n in test_G.nodes()}

def activation(u, v, d, neighbors):
    # d is cascade depth NOT distance between u and v
    l = 1/d
    print(u, v, d, neighbors & activated)
    m = len(neighbors & activated)
    p = 1 - (1 - beta) ** (1 + (m/(degs[u]-1)))
    return p * l

def CI_TLS_rec(G, n):
    activated.add(n)

    sigmas = {n: 0}  # activation probabilities

    # def sigma(v):
    #     if v in sigmas:
    #         return sigmas[v]
    #     # return 1 - np.prod([1 - ])

    ######################### Calculate RELEVANT nodes ######################### 
    relevant_nodes = collections.defaultdict(set)
    q = collections.deque()
    depth_set = [set([n])]
    visited = set([n])

    q.append(n)
    for d in range(4):
        depth_set.append(set())
        for _ in range(len(q)):
            cur = q.popleft()
            if d > 0:
                relevant_nodes[cur] = (set(G.neighbors(cur)) & depth_set[d-1])
            for neighbor in G.neighbors(cur):
                if neighbor not in visited:
                    visited.add(neighbor)
                    depth_set[d+1].add(neighbor)
                    q.append(neighbor)
    ############################## Compute sigmas ##############################
    q.clear()
    visited.clear()
    visited.add(n)
    for neighbor in G.neighbors(n):
        q.append(neighbor)
        visited.add(neighbor)
        sigmas[neighbor] = beta

    for d in range(1, 4):
        for _ in range(len(q)):
            v = q.popleft()
            if v not in sigmas:
                # print(d,v,sigmas)
                product = 1
                for r in relevant_nodes[v]:
                    product *= (1 - sigmas[r] * activation(r, v, d, set(G.neighbors(r))))
                sigmas[v] = 1 - product
            for neighbor in G.neighbors(v):
                if neighbor not in visited:
                    visited.add(neighbor)
                    q.append(neighbor)
        for node in depth_set[d]:
            # print(node)
            activated.add(node)

    for k, v in sigmas.items():
        print(k, v)

print(CI_TLS_rec(test_G, 9))
