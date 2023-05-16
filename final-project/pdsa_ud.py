
#%%
from collections import defaultdict
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng()

#%%
def pdsa_ud(G, mc):
    score = defaultdict(int)
    for _ in range(mc):
        G_temp = G.copy()
        for (u, v) in list(G_temp.edges()):
            if (rng.uniform(0, 1) > G.edges[(u, v)]["p"]):
                G_temp.remove_edge(u, v)    

        CCS = nx.connected_components(G_temp)
        for cc in CCS:
            for node in cc:
                score[node] += len(cc)

    score = {n:score[n]/mc for n in score}
    return sorted(score, key = lambda x: -score[x])
# %%
def ECE(G, node_rank, k):
    topk_list = []
    removed_list = set()
    not_considered_list = []
    for node in node_rank:
        if node not in removed_list:
            topk_list.append((node, node_rank[node]))
            removed_list |= set(G.neighbors(node))
        else:
            not_considered_list.append((node,node_rank[node]))    
        if len(topk_list) == k:
            return topk_list
    topk_list |= not_considered_list[0:k-len(topk_list)]
    return sorted(topk_list, key=lambda x: x[1])

#%%
G = nx.random_k_out_graph(20, 2, 1, False, 0)

# no multigraphs
G = nx.Graph(G)

#add probabilities
for e in list(G.edges()):
    G.edges[e]["p"] = 0.1

scores = pdsa_ud(G, 10000)
print(scores)

print(ECE(G, scores, 4))

# draw
pos = nx.spring_layout(G, seed=0, scale=100)
nx.draw(G, pos, with_labels=True)
plt.show()
# %%
