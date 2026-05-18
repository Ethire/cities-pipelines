from Simulateur_Operationnel import *


inp_file = 'example_network.inp'

# P25 links the water castle, P1 in the mess, P20 is far away from the mess
chosen_pipes = ['P25', 'P1', 'P20']

# Read every dynamic faults injected
leak_nodes, broken_sensors, surge_nodes, tf_extracted = extract_faults_from_inp(inp_file)

print("--- Fautes détectées dans le fichier INP ---")
if leak_nodes:
    for nid, coeff in leak_nodes.items():
        print(f"  Fuite sur {nid} (coeff={coeff})")
else:
    print("  Fuites : Aucune")
print(f"  Capteurs cassés    : {broken_sensors if broken_sensors else 'Aucun'}")
print(f"  Surcharges (surge) : {surge_nodes if surge_nodes else 'Aucune'}")

# Simulation start
results = simulate_network(
    inp_file=inp_file,
    chosen_pipes=chosen_pipes,
    leak_nodes=leak_nodes,
    leak_coeff=0.01,
    broken_sensors=broken_sensors,
    surge_nodes=surge_nodes,
    p_break=0.0,
    tf=tf_extracted
)

print("\n--- Simulation terminée ---")
print(f"Temps de simulation : {len(results['time'])} pas de temps")


en_tete_export = "t|"
liste_export = []
liste_export.append(results['time'])

for pid, data in results['pipes'].items():
    print(f"\nTuyau: {pid} ({data['start_node']} -> {data['end_node']})")
    print(f"  Pression {data['start_node']} (moy) : {np.nanmean(data['pressure_start']):.2f} bar")
    print(f"  Pression {data['end_node']} (moy) : {np.nanmean(data['pressure_end']):.2f} bar")
    print(f"  Vitesse (moy)         : {np.nanmean(data['velocity']):.4f} m/s")

    en_tete_export += pid + "|"
    liste_export.append(list(data['velocity']))

    plt.plot(np.array(results['time']), np.array(abs(data['velocity'])))
    plt.title(f"Pipe {pid} : velocity over time")
    plt.show()

    nan_count_start = np.isnan(data['pressure_start']).sum()
    nan_count_end = np.isnan(data['pressure_end']).sum()
    nan_count_v = np.isnan(data['velocity']).sum()

    if nan_count_start > 0:
        print(f"  [!] Capteur de pression cassé sur {data['start_node']} ({nan_count_start} valeurs manquantes)")
    if nan_count_end > 0:
        print(f"  [!] Capteur de pression cassé sur {data['end_node']} ({nan_count_end} valeurs manquantes)")
    if nan_count_v > 0:
        print(f"  [!] Capteur de vitesse cassé sur {pid} ({nan_count_v} valeurs manquantes)")

en_tete_export = en_tete_export[:-1]
list_to_csv(en_tete_export, liste_export)