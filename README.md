## Guide pratique pour l’utilisation du simulateur

# 1. Installation de Python
Vous devez installer le langage Python sur votre machine.  
**Windows / macOS :**  
Allez sur python.org.  
Téléchargez la version 3.12, les suivantes ne fonctionnent pas avec toutes les bibliothèques.  
IMPORTANT (Windows) : Lors de l'installation, cochez absolument la case "Add Python to PATH" avant de cliquer sur Install Now.  
**Linux :**  
Python est souvent pré-installé. Vérifiez en tapant python3 --version dans votre terminal. Sinon :  
sudo apt update && sudo apt install python3 python3-pip  

# 2. Installation des bibliothèques   
Une fois Python installé, vous devez installer les outils spécifiques utilisés par ce projet.  
Ouvrez votre terminal et copiez-collez la commande suivante :  
pip install customtkinter networkx numpy perlin_noise tsnet numpy matplotlib wntr  

# 3. Architecture du code
Sur le lien git Ethire/cities-pipelines vous trouverez tous les fichiers relatifs au code de l’interface utilisateur ainsi que ceux du simulateur avec un exemple de simulation.
Les fichiers principaux sont InterfaceV2 et Simulateur_Operationnel pour respectivement créer un réseau de canalisations, l'exporter en fichier INP, et simuler le fichier créé.

# 4. Guide d'utilisation
- Dans un premier temps, vous devez lancer le fichier Interface.py. Une fenêtre s’ouvrira et vous pourrez ensuite saisir les informations que vous voulez pour votre simulation.  
- Le réseau que vous voulez simuler apparaîtra ainsi sur fenêtre dédiée (à votre droite)  
- Une icône à droite de la fenêtre permet de générer un fichier d’entrée (fichier .inp)  qui sera ensuite importé dans le code du simulateur  
- Exécuter ensuite Simulateur_Operationnel pour simuler le réseau et extraire les données  



