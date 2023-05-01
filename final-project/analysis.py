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

# %%
MONTH = 1
with open("../data/cscareerquestions.json") as fp:
    month_nets = json.load(fp)

G = nx.DiGraph()

for u in month_nets[MONTH]:
    for v in month_nets[MONTH][u]:
        if u != v:
            G.add_edge(u, v)

# %%
seed, times = ris(G, 20, TSSCM(0.5), 1000)

# %% draw
color = ["red" if n in seed else "grey" for n in G.nodes()]
pos = nx.spring_layout(G)
nx.draw(G, node_size=10, node_color=color, pos=pos)
nx.draw(G, node_size=40, nodelist=seed, node_color="red", pos=pos)
plt.show()
