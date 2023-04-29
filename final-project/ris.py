#%%
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
def get_RRS(G):   
    """
    Inputs: G:  Networkx Graph
    Return: A random reverse reachable set expressed as a list of nodes
    """
    #convert to pandas dataframe
    df = nx.to_pandas_edgelist(G)

    # Step 1. Select random source node
    source = random.choice(np.unique(df['source']))
    
    # Step 2. Sample edges  
    df = df.loc[np.random.uniform(0,1,df.shape[0]) < df['p']]

    # Step 3. Construct reverse reachable set of the random source node
    new_nodes, RRS0 = [source], [source]   
    while new_nodes:
        
        # Limit to edges that flow into the source node
        temp = df.loc[df['target'].isin(new_nodes)]

        # Extract the nodes flowing into the source node
        temp = temp['source'].tolist()

        # Add new set of in-neighbors to the RRS
        RRS = list(set(RRS0 + temp))

        # Find what new nodes were added
        new_nodes = list(set(RRS) - set(RRS0))

        # Reset loop variables
        RRS0 = RRS[:]

    return(RRS)

#%%
# adapted from hautahi to work with networkx and have different probabilities per node
def ris(G,k,mc=1000):    
    """
    Inputs: G:  Networkx graph
            k:  Size of seed set
            mc: Number of RRSs to generate
    Return: A seed set of nodes as an approximate solution to the IM problem
    """
    
    # Step 1. Generate the collection of random RRSs
    start_time = time.time()
    R = [get_RRS(G) for _ in range(mc)]

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
    
    return(sorted(SEED),timelapse)

#%%
# create an example directed network
G = nx.random_k_out_graph(15, 2, 1, False, 0)

# no multigraphs
G = nx.DiGraph(G)

#add probabilities to each edge 
np.random.seed(0)
for e in list(G.edges):
    G.edges[e]["p"] = round(np.random.rand() * 100)/100

#draw
pos = nx.spring_layout(G, seed=0, scale=100)
nx.draw(G, pos, with_labels=True)
nx.draw_networkx_edge_labels(
    G, pos, font_size=7,
    edge_labels={(u, v): G[u][v]['p'] for (u, v) in G.edges()}
)
plt.show()