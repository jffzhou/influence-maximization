# %%
import gzip
import json
import networkx as nx
import itertools
import scipy
import matplotlib.pyplot as plt
import math

# %%
MONTH = 0
with open("cscareerquestions.json") as fp:
    month_nets = json.load(fp)

G = nx.DiGraph()

edge_list = []
for u in month_nets[MONTH]:
    for v in month_nets[MONTH][u]:
        if u!=v:
            G.add_edge(u, v)

# %%
nx.draw(G, node_size = 30)
plt.show()
