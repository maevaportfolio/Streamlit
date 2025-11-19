#!/bin/bash

# Script de déploiement automatisé - Appelle build.sh puis run.sh
echo "🚀 Déploiement automatisé de l'application Streamlit Adidas"
echo ""

# Vérifier que les scripts existent
if [ ! -f "build.sh" ]; then
    echo "❌ Erreur: build.sh non trouvé"
    exit 1
fi

if [ ! -f "run.sh" ]; then
    echo "❌ Erreur: run.sh non trouvé"
    exit 1
fi

# Rendre les scripts exécutables
echo "🔧 Préparation des scripts..."
chmod +x build.sh run.sh

# Étape 1: Construction
echo "📋 Étape 1/2: Construction de l'image Docker..."
./build.sh

# Vérifier si la construction a réussi
if [ $? -ne 0 ]; then
    echo "❌ Erreur lors de la construction"
    exit 1
fi

echo ""
echo "📋 Étape 2/2: Lancement de l'application..."
./run.sh

# Vérifier si le lancement a réussi
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Déploiement terminé avec succès!"
    echo "🌐 Application disponible sur: http://localhost:8501"
    echo ""
    echo "📋 Commandes utiles:"
    echo "   - Voir les logs: docker logs streamlit-adidas-container"
    echo "   - Arrêter l'app: ./stop.sh"
    echo "   - Relancer le conteneur: docker restart streamlit-adidas-container"
else
    echo "❌ Erreur lors du lancement"
    exit 1
fi
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé ou n'est pas dans le PATH"
    echo "💡 Installez Docker Desktop: https://www.docker.com/products/docker-desktop/"
    exit 1
fi