#!/usr/bin/env python3

# Written by: 0xGuigui
# Date: 2025-21-01
# Description: Génère et exécute un conteneur Docker d’un serveur Minecraft.

import argparse
import subprocess
import sys
from src.java_version import *
from src.dockerfile import generate_dockerfile

def main():
    parser = argparse.ArgumentParser(description="Génère et exécute un conteneur Docker d’un serveur Minecraft.")
    parser.add_argument("--jar", required=True, help="Chemin vers le fichier .jar du serveur Minecraft")
    parser.add_argument("--image-tag", default="minecraft-server:latest", help="Tag de l'image Docker à construire")
    parser.add_argument("--port", default="25565", help="Port à exposer")
    args = parser.parse_args()

    jar_path = args.jar
    port = args.port

    try:
        java_version = determine_java_version(jar_path)

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

    except KeyboardInterrupt:
        print("\nInterruption par l'utilisateur. Fermeture du programme.")
        sys.exit(0)

if __name__ == "__main__":
    main()