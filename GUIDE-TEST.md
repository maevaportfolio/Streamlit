# Guide de vérification pour l'application Streamlit Adidas

## 🔍 Tests à effectuer en local

### 1. Test automatisé complet
```bash
# Rendre le script exécutable
chmod +x test.sh

# Lancer le test complet
./test.sh
```

### 2. Tests manuels pas à pas

#### A. Vérification des prérequis
```bash
# Vérifier Docker
docker --version
docker info

# Vérifier les fichiers
ls -la app.py requierements.txt
ls -la dataset/adidas.csv
ls -la images/
```

#### B. Construction et test de l'image
```bash
# Construire l'image
docker build -t streamlit-adidas-app .

# Vérifier que l'image est créée
docker images | grep streamlit-adidas-app
```

#### C. Lancement du conteneur
```bash
# Lancer le conteneur
docker run -d --name streamlit-adidas-container -p 8501:8501 streamlit-adidas-app

# Vérifier que le conteneur fonctionne
docker ps
```

#### D. Tests de connectivité
```bash
# Test HTTP
curl -I http://localhost:8501

# Ou avec PowerShell sur Windows
Invoke-WebRequest -Uri http://localhost:8501 -Method Head
```

### 3. Tests fonctionnels dans le navigateur

#### ✅ Checklist de vérification

**Page d'accueil:**
- [ ] Animation de chargement (GIF) s'affiche pendant 2 secondes
- [ ] Logo Adidas visible en arrière-plan
- [ ] Photos du comité visibles
- [ ] Bouton "Lancer l'analyse" fonctionne

**Sidebar:**
- [ ] Logo Adidas affiché
- [ ] Filtres de date fonctionnels
- [ ] Sélection des régions fonctionne
- [ ] Dropdown produits et fournisseurs fonctionnels
- [ ] Bouton de téléchargement CSV disponible

**Onglet Vue globale:**
- [ ] KPIs affichés avec couleurs et flèches
- [ ] Graphique temporel visible
- [ ] Données se mettent à jour avec les filtres

**Onglet Géographie:**
- [ ] Carte des États-Unis s'affiche
- [ ] Tableaux TOP 2 fonctionnels
- [ ] Graphiques par région visibles
- [ ] Camemberts des canaux de vente

**Onglet Produits:**
- [ ] Treemap du CA par produit
- [ ] Graphique donut homme/femme
- [ ] Prix moyen par produit

**Onglet Fournisseurs:**
- [ ] Graphiques de profit par retailer
- [ ] Évolution temporelle des ventes
- [ ] Commentaires dynamiques

**Onglet Prix & Méthodes:**
- [ ] Scatter plot sensibilité prix
- [ ] Barres performance par canal

### 4. Tests de performance

```bash
# Surveiller l'utilisation des ressources
docker stats streamlit-adidas-container

# Vérifier les logs pour les erreurs
docker logs streamlit-adidas-container

# Test de charge basique
curl -w "@curl-format.txt" -s -o /dev/null http://localhost:8501
```

### 5. Tests d'erreur

```bash
# Tester avec des filtres extrêmes
# - Sélectionner aucune région
# - Période très courte
# - Un seul produit

# Vérifier la gestion des erreurs dans les logs
docker logs streamlit-adidas-container | grep -i error
```

### 6. Nettoyage après test

```bash
# Arrêter et supprimer le conteneur
docker stop streamlit-adidas-container
docker rm streamlit-adidas-container

# Optionnel: supprimer l'image
docker rmi streamlit-adidas-app
```

## 🚨 Problèmes courants et solutions

### Problème: L'application ne démarre pas
```bash
# Vérifier les logs
docker logs streamlit-adidas-container

# Solutions possibles:
# 1. Vérifier requierements.txt
# 2. Vérifier que tous les fichiers sont présents
# 3. Reconstruire l'image
```

### Problème: Port 8501 occupé
```bash
# Vérifier qui utilise le port
netstat -tulpn | grep 8501

# Utiliser un autre port
docker run -d --name streamlit-adidas-container -p 8502:8501 streamlit-adidas-app
```

### Problème: Images/fichiers manquants
```bash
# Vérifier le contenu du conteneur
docker exec -it streamlit-adidas-container ls -la /app/
docker exec -it streamlit-adidas-container ls -la /app/images/
docker exec -it streamlit-adidas-container ls -la /app/dataset/
```

## ✅ Critères de succès

L'application fonctionne correctement si:
1. ✅ Le conteneur reste en vie sans redémarrer
2. ✅ L'URL http://localhost:8501 est accessible
3. ✅ Tous les onglets s'affichent sans erreur
4. ✅ Les filtres modifient bien les données
5. ✅ Aucune erreur dans les logs Docker
6. ✅ Les graphiques s'affichent correctement
7. ✅ L'animation de chargement fonctionne