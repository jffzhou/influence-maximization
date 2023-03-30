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

# %%
activated = set()
beta = 0.5

test_G = nx.Graph()
nodelist = range(1, 10)
edgelist = [[1, 2], [1, 4], [1, 3], [3, 6],
            [3, 5], [6, 9], [5, 8], [5, 7], [4, 6]]


test_G.add_nodes_from(nodelist)
test_G.add_edges_from(edgelist)

degs = {n: test_G.degree(n) for n in test_G.nodes()}

# %%


def activation(u, v, d, neighbors):
    # d is cascade depth NOT distance between u and v
    l = 1/d
    m = len(neighbors & activated)
    p = 1 - (1 - beta) ** (1 + (m/(degs[u]-1)))
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
                    product *= (1 - sigmas[r] * activation(r,
                                v, d, set(G.neighbors(r))))
                sigmas[v] = 1 - product
            for neighbor in G.neighbors(v):
                if neighbor not in visited:
                    visited.add(neighbor)
                    q.append(neighbor)
        for node in depth_set[d]:
            # print(node)
            activated.add(node)

    return np.sum(list(sigmas.values())), list(sigmas.keys())


for i in range(1, 10):
    print(f"{i}: {CI_TLS_rec(test_G, i)}")


# %% influence maximization algorithm
def ci_tls_im(G, k):
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

        # remove nodes within 3 edges of i
        for n in local_nodes[np.argmax(ci_tls_scores)]:
            G_copy.remove_node(n)

    return S


# %%
MONTH = 0
with open("CryptoCurrency.json") as fp:
    month_nets = json.load(fp)

G = nx.DiGraph()

for u in month_nets[MONTH]:
    for v in month_nets[MONTH][u]:
        if u != v:
            G.add_edge(u, v)

USE_DIRECTED = False
degs = {}
if USE_DIRECTED:
    degs = {n: G.indegree(n) for n in G.nodes()}
else:
    G = G.to_undirected(reciprocal=False)
    degs = {n: G.degree(n) for n in G.nodes()}

# %%
activated = set()
beta = 0.05
k = 20
seed = ci_tls_im(G, k)
print(seed)

color = ["red" if n in seed else "grey" for n in G.nodes()]
nx.draw(G, node_size=10, node_color=color)
plt.show()

# %% HITS algorithm
h, a = nx.hits(G)
h = dict(sorted(h.items(), key=lambda item: -item[1]))
a = dict(sorted(a.items(), key=lambda item: -item[1]))

top_hubs = list(h.keys())[:k]
top_auth = list(a.keys())[:k]
print(f"{k} highest hub scores:")
for u in top_hubs:
    print(f"{u}: {h[u]}")

print(f"\n{k} highest authority scores:")
for u in top_auth:
    print(f"{u}: {a[u]}")

# %%
for n in seed:
    print(f"{n} hub ranking: {list(h.keys()).index(n)}")
    print(f"\thub score: {h[n]}")
    print(f"{n} auth ranking: {list(a.keys()).index(n)}")
    print(f"\tauth score: {a[n]}")
