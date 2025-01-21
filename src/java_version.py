# Written by: 0xGuigui
# Date: 2025-21-01
# Description: Fonctions pour extraire la version de Java à partir d'un fichier JAR.

import zipfile
import json

def get_java_version_from_jar(jar_path):
    try:
        with zipfile.ZipFile(jar_path, 'r') as jar:
            if "version.json" in jar.namelist():
                with jar.open("version.json") as version_file:
                    data = json.load(version_file)
                    return data.get("java_version")
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier version.json : {e}")
        return None