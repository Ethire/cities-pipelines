import networkx as nx
import matplotlib.pyplot as plt
import random
from scipy.spatial import distance, Delaunay
import numpy as np

# Code en cours d'écriture pour créer le réseau RURAL

order = 5   # profondeur max
nb_chateau = 3

G = nx.Graph()

G = nx.binomial_tree(order)  # sorte d'arbre, d'ordre n, soit 2**n noeuds, forme un peu aléatoire
pos = nx.spring_layout(G, k=0.3, iterations=100, seed=30)   # permet d'avoir une forme où les noeuds se croisent le moins possible 

# Pour rajouter une maison (un noeud) à chaque noeud deja existant, sauf le noeud 0 
for i in range(1, len(pos)):
    G.add_edge(i, f"M{i}")
    pos[f"M{i}"] = np.array([pos[i][0] + 0.05*random.randint(-1, 1), pos[i][1] + 0.05*random.randint(-1, 1)])   # peut-être à modifier pour que la maison soit à angle droit avec le tuyau



# Ajout de pompe et chateau d'eau
# G.add_edge("P", 0)
# pos["P"] = pos[0]+0.05   # pos est un dictionnaire qui contient les coordonnées de chaque noeud, cette ligne permet d'ajouter la pompe à proximité du noeud 0
# G.add_edge("P", "C")
# pos["C"] = pos["P"]-0.3*random.random()

# Pour ajouter les chateaux
for i in range (1, nb_chateau+1):
    G.add_node(f"C{i}", type="chateau")
    j = random.randint(0, 2**order)
    G.add_edge(f"C{i}", j)
    pos[f"C{i}"] = np.array([pos[j][0] + 0.1*random.randint(-1, 1), pos[j][1] + 0.1*random.randint(-1, 1)]) 


# Affichage
nx.draw(G, pos, with_labels=True)
plt.show()



# finir la fonction "_build_graph(self, params):" par "return G"




# print(G.nodes)  # permet d'afficher le nom des noeuds

