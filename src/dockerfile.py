# Written by: 0xGuigui
# Date: 2025-21-01
# Description: Génère un Dockerfile pour un serveur Minecraft

import os

def generate_dockerfile(jar_path, java_version, port, memory_max):
    jar_filename = os.path.basename(jar_path)
    dockerfile_content = f"""
FROM openjdk:{java_version}-jdk-slim
WORKDIR /mcserver
COPY {jar_filename} server.jar
EXPOSE {port}
CMD ["java", "-Xmx{memory_max}M", "-Xms1024M", "-jar", "server.jar", "nogui"]
"""
    try:
        with open("Dockerfile", "w") as f:
            f.write(dockerfile_content)
        print("Dockerfile généré avec succès.")
    except Exception as e:
        print(f"Erreur lors de la génération du Dockerfile : {e}")