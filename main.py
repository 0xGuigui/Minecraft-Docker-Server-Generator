#!/usr/bin/env python3

# Written by: 0xGuigui
# Date: 2025-21-01
# Description: Génère et exécute un conteneur Docker d’un serveur Minecraft.

import argparse
import subprocess
import sys
from src.java_version import get_java_version_from_jar
from src.dockerfile import generate_dockerfile

def main():
    parser = argparse.ArgumentParser(description="Génère et exécute un conteneur Docker d’un serveur Minecraft.")
    parser.add_argument("--jar", required=True, help="Chemin vers le fichier .jar du serveur Minecraft")
    parser.add_argument("--image-tag", default="minecraft-server:latest", help="Tag de l'image Docker à construire")
    parser.add_argument("--port", default="25565", help="Port à exposer")
    args = parser.parse_args()

    jar_path = args.jar
    port = args.port

    java_version = get_java_version_from_jar(jar_path)
    if not java_version:
        user_input = input("Impossible de détecter la version de Java. Connaissez-vous la version nécessaire ? (oui/non) : ").strip().lower()
        if user_input == "oui":
            try:
                java_version = int(input("Entrez la version de Java (ex : 8, 11, 17) : ").strip())
            except ValueError:
                print("Entrée invalide. Utilisation par défaut de Java 8.")
                java_version = 8
        else:
            print("Utilisation par défaut de Java 8.")
            java_version = 8

    memory_max = 1024  # Valeur par défaut en Mo
    memory_input = input("Voulez-vous définir une mémoire maximale personnalisée pour le serveur ? (oui/non) : ").strip().lower()
    if memory_input == "oui":
        try:
            memory_max = int(input("Entrez la mémoire maximale en Mo (ex : 2048 pour 2Go) : ").strip())
        except ValueError:
            print("Entrée invalide. Utilisation de la mémoire par défaut (1024M).")

    generate_dockerfile(jar_path, java_version, port, memory_max)

    try:
        subprocess.run(["docker", "build", "-t", args.image_tag, "."], check=True)
        subprocess.run(["docker", "run", "-d", "-p", f"{port}:25565", args.image_tag], check=True)
        print("Conteneur démarré avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la gestion du conteneur : {e}")

if __name__ == "__main__":
    main()