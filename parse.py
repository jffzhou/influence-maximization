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

# %%
MONTH = 1
with open("CryptoCurrency.json") as fp:
    month_nets = json.load(fp)

G = nx.DiGraph()

for u in month_nets[MONTH]:
    for v in month_nets[MONTH][u]:
        if u != v:
            G.add_edge(u, v)

# %%
nx.draw(G, node_size=30)
plt.show()

# %% HITS algorithm
h, a = nx.hits(G)
h = dict(sorted(h.items(), key=lambda item: -item[1]))
a = dict(sorted(a.items(), key=lambda item: -item[1]))

n = 10
top_hubs = list(h.keys())[:n]
top_auth = list(a.keys())[:n]
print(f"{n} highest hub scores:")
for u in top_hubs:
    print(f"{u}: {h[u]}")

print(f"\n{n} highest authority scores:")
for u in top_auth:
    print(f"{u}: {a[u]}")

# %% graph of just top hubs and authorities
nodelist = set(top_hubs + top_auth)
edgelist = [e for e in G.edges() if e[0] in nodelist and e[1] in nodelist]
color = [("purple" if n in top_auth else "red") if n in top_hubs
         else "blue" if n in top_auth else "grey"
         for n in nodelist]
reduced_G = nx.DiGraph()
reduced_G.add_nodes_from(nodelist)
reduced_G.add_edges_from(edgelist)
nx.draw_circular(reduced_G, node_color=color)
plt.show()


# %%
undir_G = G.to_undirected()
beta = 0.01

# distance dictionary
dpath = {x[0]: x[1] for x in nx.all_pairs_shortest_path_length(undir_G)}

# degree dictionary
degs = {n: undir_G.degree(n) for n in undir_G.nodes()}

# activated nodes
activated = set()

# %%


def activation(u, v, d, neighbors):
    # d is cascade depth NOT distance between u and v
    l = 1/d
    m = len(neighbors & activated)
    p = 1 - (1 - beta) ** (1 + (m/(degs[u]-1)))
    return p * l


def final_activation(i, v, d):
    if v in undir_G.neighbors(i):
        return beta
    neighbors = []
    return 1 - np.prod([1 - final_activation(i, u)*activation(u, v, d+1) for u in neighbors])


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

# %%


def CI_TLS(G, n):
    activated.add(n)
    # do calculation
    sigmas = {n: 0}
    queue = []

    for neighbor in G.neighbors(n):
        sigmas[neighbor] = beta
        activated.add(neighbor)
        queue.append((neighbor, 2))

    while queue:
        u, d = queue.pop(0)
        for v in G.neighbors(u):
            if v not in sigmas and d < 4:
                print(v)
                previous = sigmas.keys() & G.neighbors(v)
                for u in previous:
                    print(f"({u}, {v})")
                    print(sigmas[u])
                    print(set(G.neighbors(u)))
                    print(activated)
                    print(activation(u, v, d, set(G.neighbors(u))))
                prod = [
                    1 - sigmas[u]*activation(u, v, d, set(G.neighbors(neighbor))) for u in previous]
                print(prod)
                sigmas[v] = 1 - np.prod(prod)
                activated.add(v)
                queue.append((v, d + 1))

    for u in sigmas:
        activated.remove(u)
    print(sigmas)
    return sum(sigmas.values())


def CI_TLS_IM(G, k):
    S = {}
    CI_TLS_scores = {n: CI_TLS(G, n) for n in G.nodes()}


CI_TLS(test_G, 1)
# %% Construct test graph

test_G = nx.Graph()
nodelist = range(1, 10)
edgelist = [[1, 2], [1, 4], [1, 3], [3, 6],
            [3, 5], [6, 9], [5, 8], [5, 7], [4, 6]]


test_G.add_nodes_from(nodelist)
test_G.add_edges_from(edgelist)

# distance dictionary
dpath = {x[0]: x[1] for x in nx.all_pairs_shortest_path_length(test_G)}

# degree dictionary
degs = {n: test_G.degree(n) for n in test_G.nodes()}

beta = 0.5

nx.draw(test_G, with_labels=True)
plt.show()

# %%
CI_TLS_rec(test_G, 1)
