# %%
import matplotlib.pyplot as plt
from random import uniform, seed
import numpy as np
import pandas as pd
import time
import networkx as nx
import random
from collections import Counter


# %%
# adapted from hautahi to work with networkx and have different probabilities per node
def get_RRS(G, p_func):
    """
    Args:
      G:  Networkx Graph with activation probabilities associated with each edge
      p_func: A function that takes in the network and source node, and returns
        the network with activation probabilities associated with each edge.
        (can also modify the original graph edges if desired)
    Returns:
      A random reverse reachable set expressed as a list of nodes.
    """

    # Step 1. Select random source node
    source = random.choice(list(G.edges()))[0]

    # get activation probabilities
    df = nx.to_pandas_edgelist(p_func(G, source))

    # Step 2. Sample edges
    df = df.loc[np.random.uniform(0, 1, df.shape[0]) < df["p"]]

    # Step 3. Construct reverse reachable set of the random source node
    new_nodes, RRS0 = [source], [source]
    while new_nodes:
        # Limit to edges that flow into the source node
        temp = df.loc[df["target"].isin(new_nodes)]

        # Extract the nodes flowing into the source node
        temp = temp["source"].tolist()

        # Add new set of in-neighbors to the RRS
        RRS = list(set(RRS0 + temp))

        # Find what new nodes were added
        new_nodes = list(set(RRS) - set(RRS0))

        # Reset loop variables
        RRS0 = RRS[:]

    return RRS


# %%
# adapted from hautahi to work with networkx and have different probabilities per node
def ris(G, k, p_func, mc=1000):
    """
    Args:
      G:  Networkx graph
      k:  Size of seed set
      p_func: A function that takes in the network and source node, and returns
        the network with activation probabilities associated with each edge.
        (can also modify the original graph edges if desired)
      mc: Number of RRSs to generate
    Returns:
      A seed set of nodes as an approximate solution to the IM problem
    """

    # Step 1. Generate the collection of random RRSs
    start_time = time.time()
    R = [get_RRS(G, p_func) for _ in range(mc)]

    # Step 2. Choose nodes that appear most often (maximum coverage greedy algorithm)
    SEED, timelapse = [], []
    for _ in range(k):
        # Find node that occurs most often in R and add to seed set
        flat_list = [item for sublist in R for item in sublist]
        seed = Counter(flat_list).most_common()[0][0]
        SEED.append(seed)

        # Remove RRSs containing last chosen seed
        R = [rrs for rrs in R if seed not in rrs]

        # Record Time
        timelapse.append(time.time() - start_time)

    return (sorted(SEED), timelapse)


# %% some example p_funcs:


def IC_uniform(p):
    def func(G):
        for e in list(G.edges):
            G.edges[e]["p"] = p
        return G

    return lambda G, s: func(G)


def IC_random(rand_func=None):
    def func(G, s):
        for e in list(G.edges):
            G.edges[e]["p"] = np.random.rand() if rand_func is None else rand_func()
        return G

    return lambda G, s: func(G, s)


def TSSCM(beta):
    def func(G, s):
        ## get degrees
        degrees = G.in_degree()

        ## get nodes within radius of 3 from s
        G = nx.ego_graph(G.copy(), s, 3)

        ## remove edges that point back to s
        for u, v in list(G.edges()):
            if v == s:
                G.remove_edge(u, v)

        ## get distances
        distances = nx.shortest_path_length(G, source=s)

        activated = set()
        visited = set()
        depth = 1

        ## iterate through target nodes
        for v in list(distances)[1:]:
            ## new cascade depth: mark all previously visited as activated
            if distances[v] > depth:
                depth += 1
                activated = activated | visited

            ## iterate through nodes which have an edge point to v
            for u in G.predecessors(v):
                m = len(activated & set(G.neighbors(u)))
                p = 1 - (1 - beta) ** (1 + (m / (degrees[u] + 1)))
                G.edges[(u, v)]["p"] = p / distances[v]
            visited.add(v)
        return G

    return lambda G, s: func(G, s)


# %%
# create an example directed network
G = nx.random_k_out_graph(15, 2, 1, False, 0)

# no multigraphs
G = nx.DiGraph(G)

seeds, times = ris(G, 3, TSSCM(0.5), 1000)
print(seeds)
print(times)

# draw
pos = nx.spring_layout(G, seed=0, scale=100)
nx.draw(G, pos, with_labels=True)
plt.show()
