#!/bin/bash

# Script pour construire l'image Docker
echo "🐳 Construction de l'image Docker pour l'application Streamlit Adidas..."

# Nom de l'image
IMAGE_NAME="streamlit-adidas-app"
TAG="latest"

# Construire l'image Docker
docker build -t ${IMAGE_NAME}:${TAG} .

# Vérifier si la construction a réussi
if [ $? -eq 0 ]; then
    echo "✅ Image Docker construite avec succès: ${IMAGE_NAME}:${TAG}"
    echo "📋 Pour lancer l'application, utilisez: ./run.sh"
else
    echo "❌ Erreur lors de la construction de l'image Docker"
    exit 1
fi