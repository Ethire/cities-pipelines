import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np

# Code en cours d'écriture pour créer le réseau RURAL

order = 6   # profondeur max
nb_chateau = 3

G = nx.Graph()

G = nx.binomial_tree(order)  # sorte d'arbre, d'ordre n, soit 2**n noeuds, forme un peu aléatoire
pos = nx.spring_layout(G, k=0.3, iterations=300, seed=30)   # permet d'avoir une forme où les noeuds se croisent le moins possible 



# Pour ajouter les chateaux d'eau
if nb_chateau >= 1:
    G.add_node("C1", type="chateau")
    G.add_edge("C1", 0)
    pos["C1"] = np.array([pos[0][0] + 0.2*random.uniform(-1, 1), pos[0][1] + 0.2*random.uniform(-1, 1)])   

if nb_chateau >= 2:
    node_degree2 = [node for node in G.nodes() if G.degree(node) == 2]
    for i in range(2, nb_chateau+1):
        if i <= len(node_degree2):
            node = node_degree2[i-1]
        else: 
            node = random.choice(list(G.nodes()))

        G.add_node(f"C{i}", type="chateau")
        G.add_edge(f"C{i}", node)
        pos[f"C{i}"] = np.array([pos[node][0] + 0.2*random.uniform(-1, 1), pos[node][1] + 0.2*random.uniform(-1, 1)])   


pos = nx.spring_layout(G, k=0.3, iterations=500, seed=30)   # permet d'avoir une forme où les noeuds se croisent le moins possible, avant d'ajouter les maisons


# Pour rajouter une maison (un noeud) à chaque noeud deja existant, sauf le noeud 0, permet d'ajouter la maison à angle droit avec le tuyau
for i in range(1, len(pos)-nb_chateau):
    neighbors = list(G.neighbors(i))
    if neighbors:
        parent = neighbors[0]
        edge_vector = np.array(pos[i]) - np.array(pos[parent])
        perp_vector = np.array([-edge_vector[1], edge_vector[0]]) * random.choice([-1, 1])  # on multiplie par 1 ou -1 pour avoir les maisons aléatoirement à droite ou à gauche de la rue
        perp_vector = perp_vector / np.linalg.norm(perp_vector) * 0.05   # à modifier si envie, c'est la distance du tuyau jusqu'à la maison
        G.add_node(f"M{i}")
        G.add_edge(i, f"M{i}")
        pos[f"M{i}"] = np.array(pos[i]) + perp_vector

    

# Affichage
nx.draw(G, pos, with_labels=True)
plt.show()


# finir la fonction "_build_graph(self, params):" par "return G"


# print(G.nodes)  # permet d'afficher le nom des noeuds

