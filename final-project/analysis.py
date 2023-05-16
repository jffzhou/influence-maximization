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
