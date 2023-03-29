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

# %%
h, a = nx.hits(G)
h = dict(sorted(h.items(), key=lambda item: -item[1]))
a = dict(sorted(a.items(), key=lambda item: -item[1]))

n = 5
print(f"{n} highest Hub scores:")
for u in list(h.keys())[:n]:
    print(f"{u}: {h[u]}")

print(f"\n{n} highest Hub scores:")
for u in list(a.keys())[:n]:
    print(f"{u}: {a[u]}")
