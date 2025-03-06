import os
import anthropic
from dotenv import load_dotenv

# Charger les variables d'environnement depuis un fichier .env
load_dotenv()

# Récupérer la clé API depuis les variables d'environnement
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Initialiser le client Anthropic
client = anthropic.Anthropic(
    api_key=ANTHROPIC_API_KEY,
)

def process_product_data(content, file_name):
    """Traiter les données de produits avec Claude pour les structurer et organiser"""
    try:
        prompt = f"""
# Mission: Structuration de données produits
- Analyse ce document contenant des informations sur un ou plusieurs produits/modèles
- Extrais et structure toutes les données en un format bien organisé et lisible
- Mets le titre du modèle/produit principal au début du document
- Pour chaque tableau, répète le code et nom du produit au-dessus avec un format "Tableau [code produit] - [nom produit]"
- Entre chaque tableau et les sections de caractéristiques, ajoute des séparateurs "-------" pour permettre un embedding éventuel

# Instructions CRUCIALES pour la transformation des tableaux:
1. Transforme TOUS les tableaux au format suivant:
   - Utilise le point-virgule (`;`) comme séparateur entre les valeurs d'une même ligne
   - Utilise la barre oblique (`/`) pour marquer le changement de ligne
   - Conserve les tirets (`-`) pour les valeurs manquantes
   - Exemple de transformation:
     ```
     Colonne1  Colonne2  Colonne3
     ValeurA1  ValeurA2  -
     ValeurB1  -         ValeurB3
     ```
     Devient:
     ```
     Tableau [CODE] - [NOM PRODUIT]
     Colonne1;Colonne2;Colonne3/ValeurA1;ValeurA2;-/ValeurB1;-;ValeurB3
     -------
     ```

2. Pour le reste du contenu:
   - Organise toutes les spécifications techniques de façon cohérente
   - Conserve le texte descriptif dans un format lisible
   - N'omets absolument aucune information du document original
   - Assure-toi que les séparateurs "-------" sont présents entre chaque section

# Nom du fichier traité: {file_name}

# Contenu à structurer:
{content}

# Table des produits pour le nom de chaque page traiter, choisis celui approprié

| Code produit | Nom complet |
|-------------|-------------|
| OFM | Plinthe électrique standard |
| ODL | Plinthe électrique haut de gamme |
| OCE | Convecteur de style européen |
| OCT | Convecteur contemporain |
| OCL | Convecteur standard |
| ORC | Appareil rayonnant |
| OPP | Plinthe électrique pour porte patio |
| OPPM | Mini plinthe électrique pour porte patio |
| OHY | Combiné convection et air forcé |
| OVC | Ventilo-convecteur électronique compact |
| OVE | Ventilo-convecteur de style européen pour salle de bain |
| OFB | Ventilo-convecteur compact mural |
| OVS | Ventilo-convecteur résidentiel mural |
| OVRP | Ventilo-convecteur compact de plafond |
| OCP | Ventilo-convecteur coup-de-pied |
| OFH | Ventilo-convecteur de plancher |
| OFE-C | Fournaise électrique Confort |
| OFE-A | Fournaise électrique Avantage |
| OFE-B | Fournaise électrique Nortron première génération |
| OFE-ECM | Fournaise électrique écoénergétique |
| OSAME115R | VRE - Échangeur d'air récupérateur d'énergie avec recirculation |
| OSALE115 | VRE - Échangeur d'air récupérateur d'énergie |
| OSALE150 | VRE - Échangeur d'air récupérateur d'énergie |
| OSAME230R | VRE - Échangeur d'air récupérateur d'énergie avec recirculation |
| OTP-E | Thermopompe simple zone Eagle sans conduit de ventilation |
| OTP-H | Thermopompe simple zone Harmony sans conduit de ventilation |
| OTP-C | Thermopompe simple zone Champagne sans conduit de ventilation |
| OTP-P | Thermopompe simple zone Pacific sans conduit de ventilation |
| OTP-O | Thermopompe simple zone Olympia sans conduit de ventilation |
| OTP-MZ | Thermopompe multizone Myriad Plus sans conduit de ventilation |
| OTP | Options |
| OTP-F | Thermopompe centrale Flexx et système de serpentin couvert |
| OTM | Câble de plancher chauffant sur treillis |
| OTR | Câble de plancher chauffant pour membrane |
| OWF-R | Câble de plancher chauffant pour pose sur gabarit |
| OWC-M | Câble chauffant à béton sur treillis |
| OWC-R | Câble chauffant à béton en rouleau |
| OWS-T | Câble chauffant pour fonte de neige en tapis |
| ORF-P | Câble chauffant à résistance fixe 120V préassemblé pour tuyaux |
| ORF-R | Câble chauffant à résistance fixe 120V préassemblé pour déglaçage de toitures et gouttières |
| OSR-PI | Câble chauffant autorégulant 120V préassemblé |
| OSR-NA | Câble chauffant autorégulant tout usage ELSR-NA |
| OSR-MA | Câble chauffant autorégulant micro ELSR-MA |
| OSR-WA | Câble chauffant autorégulant moyenne température ELSR-WA |
| OSR-HA | Câble chauffant autorégulant haute température ELSR-HA |
| OSR | Options et Contrôles |
| ELK-MI | Câble à isolation minérale (M.I.) en alliage 825 |
| OCF | Chauffe-terrasse infrarouge |
| DECOR | Chauffe-terrasse infrarouge architectural en vitrocéramique |
| ORP | Panneau Radiant Architectural |
| OTS | Convecteur de tranchée |
| OMP | Mini plinthe électrique en aluminium |
| OMB | Mini plinthe coupe-brise en aluminium |
| OHB | Plinthe coupe-brise haute densité en aluminium |
| ODB | Plinthe coupe-brise en aluminium |
| ODI | Plinthe coupe-brise en aluminium à dessus incliné |
| OCB | Plinthe coupe-brise robuste en aluminium |
| ODBA | Plinthe coupe-brise en acier |
| ODIA | Plinthe coupe-brise en acier à dessus incliné |
| OPR | Plinthe électrique robuste en acier |
| OPA | Convecteur architectural |
| OPI | Convecteur architectural à dessus incliné |
| OLA | Convecteur architectural haute densité |
| OLI | Convecteur architectural haute densité à dessus incliné |
| OCA | Aérotherme console |
| OAWH | Aéroconvecteur architectural mural en aluminium |
| OAC | Aéroconvecteur commercial mural |
| OACP | Aéroconvecteur commercial de plafond |
| ODS | Aérotherme de plafond |
| ORA-PA15 | Rideau d'air pour service à l'auto / Comptoir de service |
| ORA-C | Rideau d'air commercial C Range |
| ORA-HX | Rideau d'air commercial HX Range |
| ORA-EC40 | Rideau d'air commercial et industriel |
| OAE | Aérotherme économique |
| OCC | Chaufferette de construction portative |
| OCC-WB | Chaufferette avec support |
| OCC-RF | Chaufferette à raccordement fixe |
| OKB | Appareil radiant infrarouge |
| OAU | Aérotherme agricole lavable |
| OHV | Aérotherme commercial |
| OPH | Aérotherme pour Plenum |
| ODH | Serpentin électrique |
| OAS | Aérotherme suspendu commercial industriel |
| OAS-MD | Option pour l'exploitation minière |
| OAV | Aérotherme vertical |
| OWD | Aérotherme lavable |
| OHX | Aérotherme antidéflagrant |
| XB | Convecteur antidéflagrant |
| OPXA | Plinthe antidéflagrante à dessus incliné |
| OSM-AF | Sèche-mains haute vélocité à buses multiples AirForceTM |
| OSM-AD | Sèche-mains et sèche-cheveux AirDuo |
| OSM-AT | Sèche-mains AirTempest |
| OSM-VD | Sèche-mains haute vélocité à profil mince VERDEdriTM |
| OSM-SD | Sèche-mains polyvalent SMARTdriTM Plus |
| XCE | Sèche-mains haute vélocité Xlerator |
"""

        print("Envoi de la requête à Claude...")
        
        # Utiliser le streaming pour traiter de grandes quantités de données
        with client.messages.stream(
            model="claude-3-7-sonnet-20250219",
            max_tokens=64000,
            temperature=0,
            system="""Tu es un expert en transformation de données tabulaires. Ta mission est de convertir 
            tous les tableaux en un format délimité spécifique: TOUJOURS utiliser des point-virgules (;) 
            entre les valeurs d'une même ligne, utiliser des barres obliques (/) pour indiquer un changement 
            de ligne, et conserver les tirets (-) pour les valeurs manquantes. Ne modifie jamais ce format 
            de transformation et applique-le à TOUS les tableaux du document. Pour chaque tableau, indique le 
            code et nom du produit au-dessus dans un format "Tableau [code produit] - [nom produit]". 
            Ajoute "-------" entre chaque tableau et section de caractéristiques.""",
            messages=[
                {"role": "user", "content": prompt}
            ]
        ) as stream:
            result = ""
            print("Réception de la réponse: ", end="", flush=True)
            for text in stream.text_stream:
                result += text
                # Afficher des points pour montrer que ça avance
                if len(result) % 500 == 0:
                    print(".", end="", flush=True)
            
            print("\nRéponse reçue!")
            return result
            
    except Exception as e:
        print(f"\nErreur lors du traitement avec Claude: {e}")
        return f"ERREUR DE TRAITEMENT: {e}\n\n{content[:1000]}...[contenu tronqué]"

def main():
    # Demander le chemin du dossier contenant les fichiers texte
    input_folder = input("Entrez le chemin du dossier contenant les fichiers texte à traiter: ")
    
    if not os.path.exists(input_folder) or not os.path.isdir(input_folder):
        print(f"Le dossier {input_folder} n'existe pas ou n'est pas un dossier.")
        return
    
    # Créer le dossier de sortie s'il n'existe pas
    output_directory = "txt_processed"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Récupérer tous les fichiers .txt dans le dossier
    txt_files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
    
    if not txt_files:
        print(f"Aucun fichier .txt trouvé dans le dossier {input_folder}.")
        return
    
    print(f"Fichiers trouvés: {len(txt_files)}")
    
    # Traiter chaque fichier texte
    for file_name in txt_files:
        print(f"\n{'='*50}")
        print(f"Traitement du fichier: {file_name}")
        
        file_path = os.path.join(input_folder, file_name)
        
        try:
            # Lire le contenu du fichier
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            print(f"Contenu du fichier lu: {len(content)} caractères")
            
            # Si le fichier est très grand, avertir l'utilisateur
            if len(content) > 25000:
                print(f"ATTENTION: Le fichier {file_name} est volumineux ({len(content)} caractères).")
            
            # Traiter le contenu avec Claude
            processed_content = process_product_data(content, file_name)
            
            # Générer le nom du fichier de sortie
            output_file_name = f"{os.path.splitext(file_name)[0]}_processed.txt"
            output_file_path = os.path.join(output_directory, output_file_name)
            
            # Écrire le résultat dans le fichier de sortie
            with open(output_file_path, 'w', encoding='utf-8') as out_file:
                out_file.write(processed_content)
            
            print(f"Traitement terminé pour le fichier {file_name}. Résultat écrit dans {output_file_name}")
            
        except Exception as e:
            print(f"Erreur lors du traitement du fichier {file_name}: {e}")
            continue  # Passer au fichier suivant
    
    print(f"\nTraitement de tous les fichiers terminé.")

if __name__ == "__main__":
    main()
