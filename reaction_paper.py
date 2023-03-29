import itertools
import networkx as nx
import scipy
import matplotlib.pyplot as plt
import math
G = nx.Graph()
file = open('twitter_combined.txt', mode='r', encoding='utf-8-sig')
lines = file.readlines()
file.close()
# print((lines[0].split(" "))[0])
edge_list = []
for line in lines:
    edges = line.split(" ")
    node1 = int(edges[0])
    node2 = int(edges[1])
    edge_list.append((node1, node2))
G = nx.from_edgelist(edge_list)
h, a = nx.hits(G)
