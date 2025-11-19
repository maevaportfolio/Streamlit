#!/bin/bash

# Script pour arrêter et nettoyer l'application Docker
echo "🧹 Nettoyage de l'application Streamlit Adidas..."

CONTAINER_NAME="streamlit-adidas-container"
IMAGE_NAME="streamlit-adidas-app"

# Arrêter le conteneur
if [ "$(docker ps -q -f name=${CONTAINER_NAME})" ]; then
    echo "🛑 Arrêt du conteneur..."
    docker stop ${CONTAINER_NAME}
fi

# Supprimer le conteneur
if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
    echo "🗑️ Suppression du conteneur..."
    docker rm ${CONTAINER_NAME}
fi

# Demander si l'utilisateur veut supprimer l'image
read -p "❓ Voulez-vous aussi supprimer l'image Docker? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ "$(docker images -q ${IMAGE_NAME}:latest)" ]; then
        echo "🗑️ Suppression de l'image..."
        docker rmi ${IMAGE_NAME}:latest
    fi
fi

echo "✅ Nettoyage terminé!"