#!/bin/bash

# Script pour lancer l'application Streamlit en conteneur Docker
echo "🚀 Lancement de l'application Streamlit Adidas..."

# Nom de l'image et du conteneur
IMAGE_NAME="streamlit-adidas-app"
CONTAINER_NAME="streamlit-adidas-container"
PORT="8501"

# Arrêter et supprimer le conteneur existant s'il existe
if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
    echo "🛑 Arrêt du conteneur existant..."
    docker stop ${CONTAINER_NAME}
    docker rm ${CONTAINER_NAME}
fi

# Lancer le nouveau conteneur
echo "▶️ Démarrage du conteneur..."
docker run -d \
    --name ${CONTAINER_NAME} \
    -p ${PORT}:8501 \
    ${IMAGE_NAME}:latest

# Vérifier si le conteneur fonctionne
if [ $? -eq 0 ]; then
    echo "✅ Application lancée avec succès!"
    echo "🌐 Accédez à l'application sur: http://localhost:${PORT}"
    echo "📊 Dashboard Adidas prêt à l'utilisation"
    echo ""
    echo "📋 Commandes utiles:"
    echo "   - Voir les logs: docker logs ${CONTAINER_NAME}"
    echo "   - Arrêter l'app: docker stop ${CONTAINER_NAME}"
    echo "   - Redémarrer: docker restart ${CONTAINER_NAME}"
else
    echo "❌ Erreur lors du lancement du conteneur"
    exit 1
fi