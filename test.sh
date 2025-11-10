#!/bin/bash

# Script de test complet pour vérifier que l'application fonctionne
echo "🔍 Test de l'application Streamlit Adidas en local..."

CONTAINER_NAME="streamlit-adidas-container"
PORT="8501"
IMAGE_NAME="streamlit-adidas-app"

echo "📋 Étape 1: Vérification des prérequis..."

# Vérifier que Docker est installé et fonctionne
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé ou n'est pas dans le PATH"
    exit 1
fi

# Vérifier que Docker daemon fonctionne
if ! docker info &> /dev/null; then
    echo "❌ Docker daemon n'est pas démarré"
    exit 1
fi

echo "✅ Docker est installé et fonctionne"

# Vérifier que les fichiers requis existent
if [ ! -f "app.py" ]; then
    echo "❌ Fichier app.py manquant"
    exit 1
fi

if [ ! -f "requierements.txt" ]; then
    echo "❌ Fichier requierements.txt manquant"
    exit 1
fi

if [ ! -d "dataset" ] || [ ! -f "dataset/adidas.csv" ]; then
    echo "❌ Dossier dataset ou fichier adidas.csv manquant"
    exit 1
fi

if [ ! -d "images" ]; then
    echo "❌ Dossier images manquant"
    exit 1
fi

echo "✅ Tous les fichiers requis sont présents"

echo ""
echo "📋 Étape 2: Construction de l'image Docker..."
docker build -t ${IMAGE_NAME}:latest . || {
    echo "❌ Erreur lors de la construction de l'image"
    exit 1
}
echo "✅ Image construite avec succès"

echo ""
echo "📋 Étape 3: Arrêt des conteneurs existants..."
if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
    docker stop ${CONTAINER_NAME} &> /dev/null
    docker rm ${CONTAINER_NAME} &> /dev/null
fi

echo ""
echo "📋 Étape 4: Lancement du conteneur..."
docker run -d \
    --name ${CONTAINER_NAME} \
    -p ${PORT}:8501 \
    ${IMAGE_NAME}:latest || {
    echo "❌ Erreur lors du lancement du conteneur"
    exit 1
}

echo "✅ Conteneur lancé"

echo ""
echo "📋 Étape 5: Attente du démarrage de l'application..."
sleep 10

# Vérifier que le conteneur fonctionne
if [ "$(docker ps -q -f name=${CONTAINER_NAME})" ]; then
    echo "✅ Conteneur en cours d'exécution"
else
    echo "❌ Le conteneur s'est arrêté"
    echo "📋 Logs du conteneur:"
    docker logs ${CONTAINER_NAME}
    exit 1
fi

echo ""
echo "📋 Étape 6: Test de connectivité..."

# Test HTTP simple
if command -v curl &> /dev/null; then
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:${PORT} || echo "000")
    if [ "$HTTP_STATUS" = "200" ]; then
        echo "✅ Application accessible sur http://localhost:${PORT}"
    else
        echo "⚠️ Application pas encore prête (HTTP $HTTP_STATUS)"
        echo "📋 Attendez quelques secondes et testez manuellement"
    fi
else
    echo "⚠️ curl non disponible, testez manuellement: http://localhost:${PORT}"
fi

echo ""
echo "📋 Étape 7: Informations de débogage..."
echo "🐳 État du conteneur:"
docker ps -f name=${CONTAINER_NAME} --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "📋 Utilisation mémoire:"
docker stats ${CONTAINER_NAME} --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

echo ""
echo "🎉 Test terminé!"
echo ""
echo "📋 Actions suivantes:"
echo "   1. Ouvrez http://localhost:${PORT} dans votre navigateur"
echo "   2. Vérifiez que l'animation de chargement apparaît"
echo "   3. Testez la navigation entre les onglets"
echo "   4. Vérifiez les filtres dans la sidebar"
echo ""
echo "📋 Commandes utiles:"
echo "   - Voir les logs: docker logs ${CONTAINER_NAME}"
echo "   - Logs en temps réel: docker logs -f ${CONTAINER_NAME}"
echo "   - Arrêter: docker stop ${CONTAINER_NAME}"
echo "   - Redémarrer: docker restart ${CONTAINER_NAME}"