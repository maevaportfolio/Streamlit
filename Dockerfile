# Utiliser l'image officielle Python comme base
FROM python:3.10-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier des requirements
COPY requierements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requierements.txt

# Copier tous les fichiers de l'application
COPY . .

# Exposer le port sur lequel Streamlit fonctionne
EXPOSE 8501

# Définir les variables d'environnement pour Streamlit
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Commande pour lancer l'application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]