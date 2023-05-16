# %%
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import scipy

# %% ZACHARY'S KARATE CLUB

# Mr. Hi (instructor) is 0, John A. (administrator) is 33
G = nx.karate_club_graph()

# color the nodes by faction
color = ['C0' if G.nodes.data()[i]['club'] ==
         "Mr. Hi" else 'C1' for i in range(len(G.nodes()))]

fig, ax = plt.subplots(figsize=(10, 10))
plt.axis("equal")
nx.draw_circular(G, with_labels=True, node_color=color, ax=ax,
                 font_color="white", node_size=1000)
ax.set_title("Zachary's Karate Club\nCircular Network Plot", fontsize=20)

# legend
john_a_legend = Line2D([], [], markerfacecolor="C1", markeredgecolor='C1',
                       marker='o', linestyle='None', markersize=10)

mr_hi_legend = Line2D([], [], markerfacecolor="C0", markeredgecolor='C0',
                      marker='o', linestyle='None', markersize=10)

ax.legend([mr_hi_legend, john_a_legend],
          ["Mr. Hi", "John A."],
          loc='upper left', bbox_to_anchor=(1, 1), title="Faction")
plt.show()


nx.draw(G, with_labels=True, node_color=[
        'C0' if i < 17 else 'C1' for i in G.nodes()])
plt.legend([mr_hi_legend, john_a_legend],
           ["Mr. Hi", "John A."],
           loc='upper left', bbox_to_anchor=(1, 1), title="Faction")
plt.show()

# %%
hubs, authorities = nx.hits(G)

# sort by values
hubs = dict(sorted(hubs.items(), key=lambda item: item[1]))
authorities = dict(sorted(authorities.items(), key=lambda item: item[1]))
print(hubs)
print(authorities)
