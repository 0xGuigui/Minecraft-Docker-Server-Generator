# Written by: 0xGuigui
# Date: 2025-21-01
# Description: Fonctions pour extraire la version de Java à partir d'un fichier JAR

import zipfile
import json
from packaging import version

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

def get_bytecode_version(jar_path):
    try:
        with zipfile.ZipFile(jar_path, 'r') as jar:
            for file in jar.namelist():
                if file.endswith(".class"):
                    with jar.open(file) as class_file:
                        class_file.read(4)  # Skip the first 4 bytes
                        major_version = int.from_bytes(class_file.read(2), byteorder='big')
                        return major_version
    except Exception as e:
        print(f"Erreur lors de l'analyse du fichier .jar : {e}")
    return None

def map_major_version_to_java(major_version):
    version_mapping = {
        52: 8,   # Java 8
        53: 9,   # Java 9
        54: 10,  # Java 10
        55: 11,  # Java 11
        56: 12,  # Java 12
        57: 13,  # Java 13
        58: 14,  # Java 14
        59: 15,  # Java 15
        60: 16,  # Java 16
        61: 17,  # Java 17
        62: 18   # Java 18
    }
    return version_mapping.get(major_version, "Inconnu")

def get_java_version_from_known_versions(minecraft_version, config_path="minecraft_versions.json"):
    try:
        with open(config_path, "r") as f:
            version_mapping = json.load(f)

        sorted_versions = sorted(version_mapping.keys(), key=version.parse)

        for known_version in sorted_versions:
            if version.parse(minecraft_version) <= version.parse(known_version):
                return version_mapping[known_version]

        if version.parse(minecraft_version) > version.parse(sorted_versions[-1]):
            return 17

        return "Inconnu"
    except FileNotFoundError:
        print(f"Erreur : Le fichier de configuration {config_path} est introuvable.")
    except json.JSONDecodeError:
        print(f"Erreur : Le fichier {config_path} contient une erreur de format.")
    return "Inconnu"

def determine_java_version(jar_path):
    # Récupérer la version de java dans le .jar
    java_version = get_java_version_from_jar(jar_path)
    if java_version:
        return java_version

    # Récupérer la version de bytecode pour les vieilles versions
    bytecode_version = get_bytecode_version(jar_path)
    if bytecode_version:
        java_version = map_major_version_to_java(bytecode_version)
        if java_version != "Inconnu":
            return java_version

    # Si y a pas
    user_version = input("Entrez la version de Minecraft (ex : 1.8.9) ou laissez vide pour Java 8 par défaut : ").strip()
    if user_version:
        java_version = get_java_version_from_known_versions(user_version)
        if java_version != "Inconnu":
            return java_version

    print("Impossible de déterminer la version de Java. Utilisation par défaut de Java 8.")
    return 8