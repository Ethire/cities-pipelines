import warnings
warnings.filterwarnings('ignore')  # Supprimer TOUS les warnings (TSNet, wntr, numpy) pour une meilleur lisibilité de l'output
import tsnet
import numpy as np
import matplotlib.pyplot as plt
from file_export import *

# --- Compatibility patch: tsnet temporarily assigns pipe.roughness = 0
# during initialization, but wntr >= 1.x rejects non-positive values.
# We relax the validator to allow zero, restoring tsnet's expected behavior.
import wntr.utils.check_values as _wntr_check
import wntr.network.elements as _wntr_elements

_original_check = _wntr_check._check_positive_non_zero_float

def _check_non_negative_float(value, property_name):
    # Allow zero for "Pipe roughness" (tsnet sets it transiently),
    # keep strict validation for everything else.
    if property_name == "Pipe roughness":
        value = float(value)
        if value < 0:
            raise ValueError(f"{property_name} must be greater than or equal to zero")
        return value
    return _original_check(value, property_name)

# Patch the symbol that wntr.network.elements actually imported.
_wntr_elements._check_positive_non_zero_float = _check_non_negative_float
# --- end of compatibility patch


#------On modifie le fichier INP à la ligne 192 --------------


def extract_faults_from_inp(inp_file):
    """
    Parcourt le fichier INP pour trouver les fautes dans les commentaires.
    L'interface écrit : [normal], [broken], [surge], [zero] ( la fuite)
    Taille de fuite optionnelle : [ZERO:0.05] ou [LEAK:0.1] et sinon 0.01
    """
    broken_sensors = set()
    leak_nodes = {}   # dict : {node_id: leak_coeff} pour modifier les valeurs des fuites
    surge_nodes = set()
    
    with open(inp_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if ';' in line:
                comment = line[line.index(';'):].upper()
                parts = line.split()
                
                item_id = None
                if not line.strip().startswith(';'):
                    item_id = parts[0]
                
                if not item_id:
                    continue
                
                # Capteur cassé : [broken]
                if '[BROKEN]' in comment:
                    broken_sensors.add(item_id)
                    
                # Fuite : [zero] ou [LEAK], avec coefficient optionnel [ZERO:0.05]
                import re
                leak_match = re.search(r'\[(ZERO|LEAK)(?::([\d.]+))?\]', comment) #Fait avec l'IA
                if leak_match:
                    coeff = float(leak_match.group(2)) if leak_match.group(2) else 0.01
                    leak_nodes[item_id] = coeff
                    
                # Demande ×5 : [surge]
                if '[SURGE]' in comment:
                    surge_nodes.add(item_id)
                                    
    return leak_nodes, list(broken_sensors), list(surge_nodes)

def simulate_network(inp_file, chosen_pipes, leak_nodes=None, leak_coeff=0.01, 
                     broken_sensors=None, surge_nodes=None, p_break=0.1):
    """
    Simule le réseau et renvoie le temps, les pressions (aux noeuds des tuyaux) 
    et les vitesses pour les tuyaux choisis.
    Gère les fuites, capteurs cassés et surcharges de demande.
    """
    if broken_sensors is None:
        broken_sensors = []
    if leak_nodes is None:
        leak_nodes = {}
    if surge_nodes is None:
        surge_nodes = []

    # 1. Initialisation du modèle
    tm = tsnet.network.TransientModel(inp_file)
    
    # Forcer les chateaux d'eau à être au dessus du reseau de 20 m
    max_elev = max([n.elevation for _, n in tm.nodes() if hasattr(n, 'elevation')] + [0])
    for _, node in tm.nodes():
        if node.node_type == 'Reservoir':
            if getattr(node, 'base_head', 0) < max_elev + 30:
                node.base_head = max_elev + 30

    # Fixer les diamètres et les coefficients de frottement
    for pipe_name, pipe in tm.links():
        if hasattr(pipe, 'diameter'):
            # Si le tuyau connecte une maison ('M'), c'est un raccordement (20 mm)
            if pipe.start_node_name.startswith('M') or pipe.end_node_name.startswith('M'):
                pipe.diameter = 0.02
            # Sinon, c'est le réseau principal, on le force à 100 mm min pour éviter les crashs
            elif pipe.diameter < 0.1:
                pipe.diameter = 0.1
                
        if hasattr(pipe, 'roughness') and tm.options.hydraulic.headloss == 'H-W' and pipe.roughness < 1.0:
            pipe.roughness = 130.0  # Valeur standard Hazen-Williams pour du PVC/PEHD

    
    dt = 0.1
    tf = 20  # temps de simulation [s]
    wavespeed = 1000.
    
    # Méthode de la conduite équivalente, dans TSNet, la condition est dt <= L / (2*a). Donc la longueur min doit être L_min = 2 * dt * a
    min_length = 2 * dt * wavespeed
    
    for pipe_name, pipe in tm.links():
        if hasattr(pipe, 'length') and pipe.length < min_length:
            old_L = pipe.length
            pipe.length = min_length
            # Ajustement du diamètre pour conserver la même perte de charge afin d'avoir la même physique dans les tuyaux ( normalement ) (L / D^5 = constante)
            pipe.diameter = pipe.diameter * (min_length / old_L)**0.2

    tm.set_wavespeed(wavespeed)
    tm.set_time(tf, dt)
    
    # 2. Ajout des fuites (avec coefficient par noeud)
    for leak_id, coeff in leak_nodes.items():
        if leak_id.startswith('P'):
            pipe = tm.get_link(leak_id)
            tm.add_leak(pipe.start_node_name, coeff)
            print(f" Fuite (coeff={coeff}) ajoutée sur {pipe.start_node_name} (tuyau {leak_id})")
        else:
            tm.add_leak(leak_id, coeff)
            print(f" Fuite (coeff={coeff}) ajoutée au noeud : {leak_id}")
    
    # 2b. Surcharges de demande (×5)
    for surge_id in surge_nodes:
        try:
            node = tm.get_node(surge_id)
            node.demand_timeseries_list[0].base_value *= 5
            print(f" Demande ×5 appliquée au noeud : {surge_id}")
        except Exception:
            print(f" Impossible d'appliquer surge sur {surge_id}")
        
    # 3. Simulation
    t0 = 0.
    engine = 'DD' # Demand Driven
    tm = tsnet.simulation.Initializer(tm, t0, engine)
    
    results_obj = 'results_rural'
    tm = tsnet.simulation.MOCSimulator(tm, results_obj)
    
    # 4. Extraction des résultats
    timestamps = tm.simulation_timestamps
    
    results = {
        'time': timestamps,
        'pipes': {}
    }
    
    for pipe_id in chosen_pipes:
        pipe = tm.get_link(pipe_id)
            
        start_node = pipe.start_node_name
        end_node = pipe.end_node_name
        
        n_start = tm.get_node(start_node)
        n_end = tm.get_node(end_node)
        
        # 4. Récupération des données du tuyau
        # Pressions réelles (Charge totale - Altitude du noeud)
        elev_start = getattr(n_start, 'elevation', 0)
        elev_end = getattr(n_end, 'elevation', 0)
        
        p_start = (np.array(n_start.head) - elev_start) / 10.197  # Conversion mH2O -> bar
        p_end = (np.array(n_end.head) - elev_end) / 10.197
        
        # Vitesse du tuyau
        v_start = np.array(pipe.start_node_velocity)
        v_end = np.array(pipe.end_node_velocity)
        velocity = (v_start + v_end) / 2.0
        
        # 5. Gestion des capteurs cassés
        # Simulation capteur cassé en remplaçant aléatoirement des valeurs par NaN ( pas de valeur ou sinon on peut mettre 0)
        if start_node in broken_sensors:
            mask = np.random.rand(len(p_start)) < p_break
            p_start[mask] = np.nan
            
        if end_node in broken_sensors:
            mask = np.random.rand(len(p_end)) < p_break
            p_end[mask] = np.nan
            
        if pipe_id in broken_sensors:
            mask = np.random.rand(len(velocity)) < p_break
            velocity[mask] = np.nan

        results['pipes'][pipe_id] = {
            'pressure_start': p_start,
            'pressure_end': p_end,
            'velocity': velocity,
            'start_node': start_node,
            'end_node': end_node
        }
        
    return results

if __name__ == "__main__":
    # Nom du fichier INP à utiliser
    inp_file = r'reseau.inp'
    
    # Choix des tuyaux à observer ( à voir pour le CSV )
    chosen_pipes = ['P20', 'P21', 'P22']
    
    # Lecture des fuites, capteurs cassés et surcharges depuis le fichier INP
    leak_nodes, broken_sensors, surge_nodes = extract_faults_from_inp(inp_file)
    
    print("--- Fautes détectées dans le fichier INP ---")
    if leak_nodes:
        for nid, coeff in leak_nodes.items():
            print(f"  Fuite sur {nid} (coeff={coeff})")
    else:
        print("  Fuites : Aucune")
    print(f"  Capteurs cassés    : {broken_sensors if broken_sensors else 'Aucun'}")
    print(f"  Surcharges (surge) : {surge_nodes if surge_nodes else 'Aucune'}")
    
    # Lancement de la simulation
    results = simulate_network(
        inp_file=inp_file,
        chosen_pipes=chosen_pipes,
        leak_nodes=leak_nodes,
        leak_coeff=0.01,
        broken_sensors=broken_sensors,
        surge_nodes=surge_nodes,
        p_break=0.2
    )
    
    print("\n--- Simulation terminée ---")
    print(f"Temps de simulation : {len(results['time'])} pas de temps")
    
    # 5. Pour les data, on sélectionne la pression avec data[node], vitesse data[velocity], ici c'est la moyenne pour l'instant ( pour les tests )


    for pid, data in results['pipes'].items():
        print(f"\nTuyau: {pid} ({data['start_node']} -> {data['end_node']})")
        print(f"  Pression {data['start_node']} (moy) : {np.nanmean(data['pressure_start']):.2f} bar")
        print(f"  Pression {data['end_node']} (moy) : {np.nanmean(data['pressure_end']):.2f} bar")
        print(f"  Vitesse (moy)         : {np.nanmean(data['velocity']):.4f} m/s")

        plt.plot(np.array(results['time']), np.array(data['velocity']))
        plt.title(f"Pipe {pid} : velocity over time")
        plt.show()

        # Affichage des capteurs cassés et du nombre de valeurs manquantes

        nan_count_start = np.isnan(data['pressure_start']).sum()
        nan_count_end = np.isnan(data['pressure_end']).sum()
        nan_count_v = np.isnan(data['velocity']).sum()
        
        if nan_count_start > 0:
             print(f"  [!] Capteur de pression cassé sur {data['start_node']} ({nan_count_start} valeurs manquantes)")
        if nan_count_end > 0:
             print(f"  [!] Capteur de pression cassé sur {data['end_node']} ({nan_count_end} valeurs manquantes)")
        if nan_count_v > 0:
             print(f"  [!] Capteur de vitesse cassé sur {pid} ({nan_count_v} valeurs manquantes)")
