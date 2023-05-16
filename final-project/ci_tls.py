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
from copy import deepcopy
import pylab
from matplotlib.lines import Line2D


USE_DIRECTED = True


# %% influence maximization algorithm
def ci_tls_im(G, k, beta, remove=True):
    degs = {}
    if USE_DIRECTED:
        degs = {n: G.in_degree(n) for n in G.nodes()}
    else:
        G = G.to_undirected(reciprocal=False)
        degs = {n: G.degree(n) for n in G.nodes()}

    def activation(u, v, d, neighbors):
        # d is cascade depth NOT distance between u and v
        l = 1 / d
        m = len(neighbors & activated)
        p = 1 - (1 - beta) ** (1 + (m / (degs[u] - 1)))
        return p * l

    def CI_TLS_rec(G, n):
        activated.add(n)

        sigmas = {n: 0}  # activation probabilities

        ######################### Calculate RELEVANT nodes #########################
        relevant_nodes = {}
        q = collections.deque()
        depth_set = [{n}]
        visited = {n}

        q.append(n)
        for d in range(4):
            depth_set.append(set())
            for _ in range(len(q)):
                cur = q.popleft()
                if d > 0:
                    relevant_nodes[cur] = set(G.neighbors(cur)) & depth_set[d - 1]
                for neighbor in G.neighbors(cur):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        depth_set[d + 1].add(neighbor)
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
                        product *= 1 - sigmas[r] * activation(
                            r, v, d, set(G.neighbors(r))
                        )
                    sigmas[v] = 1 - product
                for neighbor in G.neighbors(v):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        q.append(neighbor)
            for node in depth_set[d]:
                # print(node)
                activated.add(node)

        return np.sum(list(sigmas.values())), list(sigmas.keys())

    activated = set()
    S = set()
    G_copy = deepcopy(G)
    while len(S) < k and len(G_copy.nodes()) > 0:
        # calculate scores
        ci_tls_scores = []
        local_nodes = []
        for n in G_copy.nodes():
            score, local = CI_TLS_rec(G_copy, n)
            ci_tls_scores.append(score)
            local_nodes.append(local)

        # add node with highest score
        i = list(G_copy.nodes())[np.argmax(ci_tls_scores)]
        S.add(i)

        # remove nodes
        if remove:
            for n in local_nodes[np.argmax(ci_tls_scores)]:
                G_copy.remove_node(n)
        else:
            G_copy.remove_node(i)

    return S
