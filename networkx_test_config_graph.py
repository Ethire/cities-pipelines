import networkx as nx
import matplotlib.pyplot as plt
import random
from scipy.spatial import distance, Delaunay
import numpy as np


config = 3
# entre 1 et 22

if config == 1:
    G = nx.balanced_tree(6, 4)  # r = nb de ramifications, h = profondeur des ramifications

elif config == 2:
    G = nx.barbell_graph(3, 5) # inutile

elif config == 3:
    G = nx.binomial_tree(6)  # sorte d'arbre, d'ordre n, soit 2**n noeuds, forme un peu aléatoire
    pos = nx.spring_layout(G, k=0.3, iterations=100, seed=30)   # permet d'avoir une forme où les noeuds se croisent le moins possible 
    G.add_edge('pompe', 0)
    pos['pompe'] = pos[0]+0.05   # pos est un dictionnaire qui contient les coordonnées de chaque noeud, cette ligne permet d'ajouter la pompe à proximité du noeud 0
    G.add_edge('pompe', 'chateau')
    pos['chateau'] = pos['pompe']-0.3*random.random()
    nx.draw(G, pos, with_labels=True)
    plt.show()
    

elif config == 4:
    G = nx.complete_graph(10) # tous les noeuds sont reliés

elif config == 5:
    G = nx.complete_multipartite_graph(5, [1, 2])  # à vérifier comment ça fonctionne

elif config == 6:
    G = nx.circular_ladder_graph(10)  # mignon mais pas utile

elif config == 7:
    G = nx.circulant_graph(20, [1, 2, 5])  # n = nb de noeuds, offsets = liste d'entiers pour dire + ou - quels noeuds sont reliés entre eux (constituent la liste des x)

elif config == 8:
    G = nx.cycle_graph(5)  # c'est juste un cercle avec n = nb de noeuds

elif config == 9:
    G = nx.dorogovtsev_goltsev_mendes_graph(3)

elif config == 10:
    G = nx.empty_graph(5)  # crée graphe sans liens

elif config == 11:
    G = nx.full_rary_tree(5, 8)  # bizarre

elif config == 12:
    G = nx.kneser_graph(5, 3)  #bizarre

elif config == 13:
    G = nx.ladder_graph(5)  # mignon mais inutile pour nous

elif config == 14:
    G = nx.lollipop_graph(10, 5) # crée un graphe en forme de sucette, m = nb de noeuds dans la sucette, n = nb de noeuds sur la tige

elif config == 15:
    G = nx.null_graph()  # graphe sans noeud

elif config == 16:
    G = nx.path_graph(10) # c'est juste une ligne de noeuds, n = nb de noeuds

elif config == 17:
    G = nx.star_graph(10)  # 1 noeud au centre et des noeuds autour

elif config == 18:
    G = nx.tadpole_graph(8, 10)  # forme de cerf-volant

elif config == 19:
    G = nx.trivial_graph()  # 1 seul noeud

elif config == 20:
    G = nx.turan_graph(10, 9)  # un peu comme circulant

elif config == 21:
    G = nx.wheel_graph(10)  # les noeuds forme 1 cercle + 1 noeud au milieu, chaque noeud est relié à son voisin gauche + droite et au noeud central

elif config == 22:
    # 1. Création de 10 points (coordonnées x, y entre 0 et 1)
    n_points = 20
    points = np.random.rand(n_points, 2)

    # 2. Calcul de la triangulation de Delaunay via SciPy
    tri = Delaunay(points)

    # 3. Création du graphe NetworkX
    G = nx.Graph()

    # Les 'simplices' de Delaunay sont les triangles (ex: [node1, node2, node3])
    for triangle in tri.simplices:
        # On ajoute les 3 arêtes de chaque triangle
        G.add_edge(triangle[0], triangle[1])
        G.add_edge(triangle[1], triangle[2])
        G.add_edge(triangle[2], triangle[0])

    # 4. Stockage des positions pour l'affichage (important !)
    pos = {i: points[i] for i in range(n_points)}
    print(pos[0])
    
    # Pour rajouter une maison (un noeud) à chaque noeud deja existant, sauf le noeud 0 ! A AMELIORER
    for i in range(1, len(pos)):
        G.add_edge(i, i+n_points)
        pos[i + n_points] = np.array([pos[i][0] + 0.05*random.randint(-1, 1), pos[i][1] + 0.05*random.randint(-1, 1)])

    G.add_edge('pompe', 0)
    pos['pompe'] = pos[0]+0.05   # pos est un dictionnaire qui contient les coordonnées de chaque noeud, cette ligne permet d'ajouter la pompe à proximité du noeud 0
    G.add_edge('pompe', 'chateau')
    pos['chateau'] = pos['pompe']-0.3*random.random()

    # 5. Affichage
    nx.draw(G, pos, with_labels=True)
    plt.show()





# print(G.nodes)  # permet d'afficher le nom des noeuds



# nx.draw(G, pos, with_labels=True)
# plt.show()
