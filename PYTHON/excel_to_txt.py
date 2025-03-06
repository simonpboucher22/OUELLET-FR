import pandas as pd
import os
import openpyxl
import re
import sys
import subprocess
import zipfile
from pathlib import Path

def install_package(package):
    """
    Install a Python package if it's not already installed
    """
    try:
        __import__(package)
        print(f"{package} est déjà installé.")
    except ImportError:
        print(f"Installation de {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"{package} a été installé avec succès.")

# Vérifier si xlrd est installé, sinon l'installer
try:
    import xlrd
except ImportError:
    install_package("xlrd")
    import xlrd

def excel_to_txt_files(excel_file_path, output_dir=None):
    """
    Crée un fichier txt pour chaque onglet d'un fichier Excel
    en préservant exactement la structure et les tabulations.
    Supporte les formats .xlsx (openpyxl) et .xls (xlrd).
    
    Args:
        excel_file_path (str): Chemin vers le fichier Excel
        output_dir (str, optional): Répertoire où enregistrer les fichiers txt
    """
    # Vérifier si le fichier existe
    if not os.path.exists(excel_file_path):
        print(f"Erreur: Le fichier {excel_file_path} n'existe pas.")
        return
    
    # Créer le répertoire de sortie s'il n'existe pas
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Déterminer le format du fichier (.xlsx ou .xls) en fonction de l'extension
    file_extension = Path(excel_file_path).suffix.lower()
    
    print(f"Lecture du fichier Excel: {excel_file_path}")
    
    try:
        if file_extension == ".xlsx":
            # Pour les fichiers .xlsx, utiliser openpyxl
            try:
                workbook = openpyxl.load_workbook(excel_file_path)
                
                # Parcourir chaque onglet
                for sheet_name in workbook.sheetnames:
                    sheet = workbook[sheet_name]
                    
                    # Nettoyer le nom de la feuille pour le nom de fichier
                    safe_sheet_name = re.sub(r'[\\/*?:"<>|]', "_", sheet_name)
                    
                    # Créer le nom du fichier txt
                    txt_file_name = f"{safe_sheet_name}.txt"
                    if output_dir:
                        txt_file_path = os.path.join(output_dir, txt_file_name)
                    else:
                        txt_file_path = txt_file_name
                    
                    # Écrire le contenu de la feuille dans un fichier txt
                    with open(txt_file_path, 'w', encoding='utf-8') as f:
                        for row in sheet.rows:
                            # Convertir chaque cellule en texte
                            row_values = [str(cell.value) if cell.value is not None else '' for cell in row]
                            # Joindre avec des tabulations et écrire dans le fichier
                            f.write('\t'.join(row_values) + '\n')
                    
                    print(f"Fichier créé: {txt_file_path}")
                
            except zipfile.BadZipFile:
                print(f"Erreur: Le fichier {excel_file_path} a l'extension .xlsx mais n'est pas un fichier Excel valide ou est au format .xls.")
                print("Tentative d'ouverture en tant que fichier .xls...")
                # Essayer avec xlrd si le fichier est en fait un .xls avec une extension incorrecte
                file_extension = ".xls"
            
        if file_extension == ".xls":
            # Pour les fichiers .xls, utiliser xlrd
            workbook = xlrd.open_workbook(excel_file_path)
            # Parcourir chaque onglet
            for sheet_index in range(workbook.nsheets):
                sheet = workbook.sheet_by_index(sheet_index)
                sheet_name = sheet.name
                
                # Nettoyer le nom de la feuille pour le nom de fichier
                safe_sheet_name = re.sub(r'[\\/*?:"<>|]', "_", sheet_name)
                
                # Créer le nom du fichier txt
                txt_file_name = f"{safe_sheet_name}.txt"
                if output_dir:
                    txt_file_path = os.path.join(output_dir, txt_file_name)
                else:
                    txt_file_path = txt_file_name
                
                # Écrire le contenu de la feuille dans un fichier txt
                with open(txt_file_path, 'w', encoding='utf-8') as f:
                    for row_index in range(sheet.nrows):
                        # Lire toutes les valeurs dans la ligne
                        row_values = [str(sheet.cell_value(row_index, col_index)) if sheet.cell_value(row_index, col_index) is not None else '' 
                                     for col_index in range(sheet.ncols)]
                        # Joindre avec des tabulations et écrire dans le fichier
                        f.write('\t'.join(row_values) + '\n')
                
                print(f"Fichier créé: {txt_file_path}")
            
    except Exception as e:
        print(f"Erreur lors du traitement du fichier Excel: {str(e)}")
        print("Assurez-vous que le fichier est un fichier Excel valide (.xlsx ou .xls).")
        return
    
    print("Conversion terminée!")

if __name__ == "__main__":
    # Demander à l'utilisateur le chemin du fichier Excel
    excel_path = input("Entrez le chemin du fichier Excel: ")
    
    # Demander le répertoire de sortie (facultatif)
    output_directory = input("Entrez le répertoire de sortie (laissez vide pour le répertoire courant): ")
    
    if output_directory == "":
        output_directory = None
    
    # Vérifier l'extension du fichier
    file_extension = Path(excel_path).suffix.lower()
    if file_extension not in ['.xlsx', '.xls']:
        print(f"Attention: L'extension {file_extension} n'est pas une extension Excel reconnue (.xlsx ou .xls).")
        confirm = input("Voulez-vous quand même essayer de traiter ce fichier? (o/n): ")
        if confirm.lower() != 'o':
            print("Opération annulée.")
            sys.exit(0)
    
    # Exécuter la fonction
    excel_to_txt_files(excel_path, output_directory)
