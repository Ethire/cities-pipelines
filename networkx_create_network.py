import networkx as nx
import matplotlib.pyplot as plt
import random
from scipy.spatial import distance, Delaunay
import numpy as np


config =    "rurale"   #"urbaine"



if config == "rurale":
    order = 7   # profondeur max
    G = nx.binomial_tree(order)  # sorte d'arbre, d'ordre n, soit 2**n noeuds, forme un peu aléatoire
    pos = nx.spring_layout(G, k=0.3, iterations=100, seed=30)   # permet d'avoir une forme où les noeuds se croisent le moins possible 
    
    # Ajout de pompe et chateau d'eau
    G.add_edge('pompe', 0)
    pos['pompe'] = pos[0]+0.05   # pos est un dictionnaire qui contient les coordonnées de chaque noeud, cette ligne permet d'ajouter la pompe à proximité du noeud 0
    G.add_edge('pompe', 'chateau')
    pos['chateau'] = pos['pompe']-0.3*random.random()
    
    # Affichage
    nx.draw(G, pos, with_labels=True)
    plt.show()
    

elif config == "urbaine":
    nb_pts = 20
    points = np.random.rand(nb_pts, 2)

    # Calcul de la triangulation de Delaunay via SciPy
    tri = Delaunay(points)

    G = nx.Graph()

    # Les 'simplices' de Delaunay sont les triangles (ex: [node1, node2, node3])
    for triangle in tri.simplices:
        # On ajoute les 3 arêtes de chaque triangle
        G.add_edge(triangle[0], triangle[1])
        G.add_edge(triangle[1], triangle[2])
        G.add_edge(triangle[2], triangle[0])

    # Stockage des positions pour l'affichage (important !)
    pos = {i: points[i] for i in range(nb_pts)}
    
    # Pour rajouter une maison (un noeud) à chaque noeud deja existant, sauf le noeud 0 
    for i in range(1, len(pos)):
        G.add_edge(i, i+nb_pts)
        pos[i + nb_pts] = np.array([pos[i][0] + 0.05*random.randint(-1, 1), pos[i][1] + 0.05*random.randint(-1, 1)])

    G.add_edge('pompe', 0)
    pos['pompe'] = pos[0]+0.05   # pos est un dictionnaire qui contient les coordonnées de chaque noeud, cette ligne permet d'ajouter la pompe à proximité du noeud 0
    G.add_edge('pompe', 'chateau')
    pos['chateau'] = pos['pompe']-0.3*random.random()

    # Affichage
    nx.draw(G, pos, with_labels=True)
    plt.show()




# print(G.nodes)  # permet d'afficher le nom des noeuds

