# %%
import matplotlib.pyplot as plt
from random import uniform, seed
import numpy as np
import pandas as pd
import time
import networkx as nx
import random
from collections import Counter
import json
from ris import *
from ci_tls import *

# %%
MONTH = 1
with open("../data/cscareerquestions.json") as fp:
    month_nets = json.load(fp)

G = nx.DiGraph()

for u in month_nets[MONTH]:
    for v in month_nets[MONTH][u]:
        if u != v:
            G.add_edge(u, v)


def draw_seeds(G, seeds, rs=None):
    color = ["red" if n in seeds else "grey" for n in G.nodes()]
    pos = nx.spring_layout(G, seed=rs)
    nx.draw(G, node_size=10, node_color=color, pos=pos)
    nx.draw(G, node_size=40, nodelist=seeds, node_color="red", pos=pos)


# %%
ris_seeds, times = ris(G, 20, TSSCM(0.5), 1000)
print(ris_seeds)
draw_seeds(G, ris_seeds, 0)
plt.title("Seed set from RIS using TSSCM model")
plt.show()
# %%
ci_tls_seeds = ci_tls_im(G, 20, 0.5, True)
print(ci_tls_seeds)
draw_seeds(G, ci_tls_seeds, 0)
plt.title("Seed set from CI_TLS with removal")
plt.show()

# %%
ci_tls_no_removal_seeds = ci_tls_im(G, 20, 0.5, False)
print(ci_tls_no_removal_seeds)
draw_seeds(G, ci_tls_no_removal_seeds, 0)
plt.title("Seed set from CI_TLS without removal")
plt.show()

# %%
ris_seeds = set(ris_seeds)
print(len(ris_seeds & ci_tls_seeds))

# %%
print(f"RIS intersection with CI_TLS with removal: {len(ris_seeds & ci_tls_seeds)}")
print(
    f"RIS intersection with CI_TLS without removal: {len(ris_seeds & ci_tls_no_removal_seeds)}"
)

# %%
ris_cic_seeds, times = ris(G, 20, CIC(lambda x: nx.betweeness_centrality(x), 0.5), 1000)
print(ris_cic_seeds)
draw_seeds(G, ris_cic_seeds, 0)
plt.title("Seed set from RIS using CIC model with betweenness centrality")
plt.show()

# %% Tiny network for testing
G = nx.random_k_out_graph(30, 2, 1, False, 0)

# no multigraphs
G = nx.DiGraph(G)

seeds, times = ris(G, 3, CIC(lambda x: nx.eigenvector_centrality(x), 0.5), 10000)
print(seeds)
print(times)

# draw
pos = nx.spring_layout(G, seed=0, scale=100)
nx.draw(G, pos, with_labels=True)
plt.show()
