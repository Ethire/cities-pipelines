import networkx as nx
import matplotlib.pyplot as plt

config = 15     
# entre 1 et 16

G = nx.path_graph(20)

if config == 1:
    G = nx.complete_bipartite_graph(3, 3)
    pos = nx.bipartite_layout(G)

elif config == 2:
    pos = nx.circular_layout(G)

elif config == 3:
    pos = nx.forceatlas2_layout(G)  # bizarre

elif config == 4:
    pos = nx.kamada_kawai_layout(G) 

elif config == 5:
    pos = nx.random_layout(G)

elif config == 6:
    pos = nx.rescale_layout(G)  # pour recentrer les noeuds ?

elif config == 7:
    pos = nx.rescale_layout_dict(G) 

elif config == 8:
    pos = nx.shell_layout(G)  # forme circulaire

elif config == 9:
    pos = nx.spring_layout(G)  # bizarre

elif config == 10:
    pos = nx.spectral_layout(G)  # forme de parabole

elif config == 11:
    pos = nx.planar_layout(G)   # forme bizarre, fait des liens super longs

elif config == 12:
    pos = nx.fruchterman_reingold_layout(G)     # forme bizarre

elif config == 13:
    pos = nx.spiral_layout(G)       # spirale

elif config == 14:
    pos = nx.multipartite_layout(G)

elif config == 15:
    pos = nx.bfs_layout(G)  # breadth-first search

elif config == 16:
    pos = nx.arf_layout(G)  # attractive and repulsive forces


nx.draw(G, pos, with_labels=True)
plt.show()