import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
import math

# Code en cours d'écriture pour créer le réseau RURAL

nb_maisons = 50
nb_chateau = 5


G = nx.Graph()

order = math.trunc(math.log(nb_maisons)/math.log(2)) # rajouter des maisons au hasard (difference entre puissance de 2 et nb voulu)
G = nx.binomial_tree(order)  # sorte d'arbre, d'ordre n, soit 2**n noeuds, forme un peu aléatoire
pos = nx.spring_layout(G, k=0.3, iterations=300, seed=30)   # permet d'avoir une forme où les noeuds se croisent le moins possible 


# Pour rajouter les maisons supplémentaires
if nb_maisons != 2**order:
    ajout = nb_maisons - 2**order
    noeuds_existants = list(G.nodes())
    
    for i in range (0, ajout):
        noeud_ajout = random.choice(noeuds_existants)
        nouv_noeud = 2**order + i
        G.add_node(nouv_noeud)
        G.add_edge(nouv_noeud, noeud_ajout)
        pos[nouv_noeud] = np.array([pos[noeud_ajout][0] + 0.2*random.uniform(-1, 1), pos[noeud_ajout][1] + 0.2*random.uniform(-1, 1)])   
        noeuds_existants.append(nouv_noeud)

pos = nx.spring_layout(G, k=0.3, iterations=300, seed=30)   # permet d'avoir une forme où les noeuds se croisent le moins possible 


# Pour ajouter les chateaux d'eau
noeuds_existants = list(G.nodes())
for i in range(1, nb_chateau+1):
    val_inf = round(((i-1)/nb_chateau)*len(noeuds_existants))
    val_sup = round((i/nb_chateau)*len(noeuds_existants))
    noeud_chateau = random.choice(noeuds_existants[val_inf:val_sup])
    chateau_node = f"C{i}"
    G.add_node(chateau_node, type="chateau")
    G.add_edge(chateau_node, noeud_chateau)
    pos[chateau_node] = np.array([pos[noeud_chateau][0] + 0.2 * random.uniform(-1, 1), pos[noeud_chateau][1] + 0.2 * random.uniform(-1, 1)])

pos = nx.spring_layout(G, k=0.3, iterations=500, seed=30)   # permet d'avoir une forme où les noeuds se croisent le moins possible, avant d'ajouter les maisons


# if nb_chateau >= 1:
#     G.add_node("C1", type="chateau")
#     G.add_edge("C1", 0)
#     pos["C1"] = np.array([pos[0][0] + 0.2*random.uniform(-1, 1), pos[0][1] + 0.2*random.uniform(-1, 1)])   

# if nb_chateau >= 2:
#     node_degree2 = [node for node in G.nodes() if G.degree(node) == 2]
#     for i in range(2, nb_chateau+1):
#         if i <= len(node_degree2):
#             node = node_degree2[i-1]
#         else: 
#             node = random.choice(list(G.nodes()))

#         G.add_node(f"C{i}", type="chateau")
#         G.add_edge(f"C{i}", node)
#         pos[f"C{i}"] = np.array([pos[node][0] + 0.2*random.uniform(-1, 1), pos[node][1] + 0.2*random.uniform(-1, 1)])   




# Pour rajouter une maison (un noeud) à chaque noeud deja existant, permet d'ajouter la maison à angle droit avec le tuyau
for i in list(G.nodes())[0:nb_maisons]:
    parent = next(G.neighbors(i))
    edge_vector = np.array(pos[i]) - np.array(pos[parent])
    perp_vector = np.array([-edge_vector[1], edge_vector[0]]) * random.choice([-1, 1])  # on multiplie par 1 ou -1 pour avoir les maisons aléatoirement à droite ou à gauche de la rue
    perp_vector = perp_vector / np.linalg.norm(perp_vector) * 0.05   # à modifier si envie, c'est la distance du tuyau jusqu'à la maison
    #perp_vector += np.array([random.uniform(0.05, 0.05), random.uniform(-0.05, 0.05)])
    nouv_maison = f"M{i}"
    G.add_node(nouv_maison, type="house")
    G.add_edge(i, nouv_maison)
    pos[nouv_maison] = np.array(pos[i]) + perp_vector




# Affichage
nx.draw(G, pos, with_labels=True)
plt.show()


# finir la fonction "_build_graph(self, params):" par "return G"
