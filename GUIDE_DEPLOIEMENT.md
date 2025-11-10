# 🚀 Guide de Déploiement Local - Application Streamlit Adidas

## 📁 Structure actuelle du projet
```
Streamlit-main/
├── app.py                 # Application principale Streamlit
├── dataset/
│   └── adidas.csv         # Données CSV
├── images/                # Images et logos
├── requierements.txt      # Dépendances Python
├── Dockerfile            # Configuration Docker
├── build.sh              # Script construction Docker
├── run.sh                # Script lancement Docker  
├── stop.sh               # Script arrêt Docker
├── test.sh               # Script test Docker
├── start.sh              # Script démarrage rapide interactif
├── deploy.ps1            # Script PowerShell (optionnel)
└── README.md             # Documentation
```

## 🎯 Méthodes de déploiement

### **Méthode 1 : Déploiement Local Direct (Recommandé pour développement)**

#### A. Installation des dépendances
```bash
# Installer les packages Python requis
pip install -r requierements.txt
```

#### B. Lancement de l'application
```bash
# Lancer Streamlit
streamlit run app.py
```

#### C. Accès à l'application
- Ouvrir dans le navigateur : **http://localhost:8501**
- L'application se lance avec l'animation de chargement
- Tester tous les onglets et filtres

---

### **Méthode 2 : Déploiement avec Docker (Production)**

#### A. Prérequis
- Docker installé et démarré
- Tous les fichiers du projet présents

#### B. Scripts automatisés Bash
```bash
# Option 1: Script interactif (Recommandé pour débutants)
chmod +x start.sh
./start.sh

# Option 2: Scripts individuels
# Construction de l'image
chmod +x build.sh
./build.sh

# Lancement de l'application
chmod +x run.sh
./run.sh

# Test complet (optionnel)
chmod +x test.sh
./test.sh
```

#### C. Scripts manuels
```bash
# 1. Construction de l'image
docker build -t streamlit-adidas-app .

# 2. Lancement du conteneur
docker run -d --name streamlit-adidas-container -p 8501:8501 streamlit-adidas-app

# 3. Vérification
docker ps
```

#### D. Gestion du conteneur
```bash
# Voir les logs
docker logs streamlit-adidas-container

# Logs en temps réel
docker logs -f streamlit-adidas-container

# Arrêter l'application
docker stop streamlit-adidas-container

# Redémarrer
docker restart streamlit-adidas-container

# Supprimer
docker rm streamlit-adidas-container

# Nettoyage complet
chmod +x stop.sh
./stop.sh
```

---

## ✅ Checklist de vérification

### Avant le déploiement :
- [ ] Fichier `dataset/adidas.csv` présent
- [ ] Dossier `images/` avec tous les logos
- [ ] Python installé (version 3.9+)
- [ ] Packages installés (`pip install -r requierements.txt`)

### Test de l'application :
- [ ] Animation de chargement (2 secondes)
- [ ] Logo Adidas en arrière-plan
- [ ] Onglet "Accueil" avec photos du comité
- [ ] Onglet "Vue globale" avec KPIs et graphiques
- [ ] Onglet "Géographie" avec carte USA
- [ ] Onglet "Produits" avec treemap et graphiques
- [ ] Onglet "Fournisseurs" avec analyses
- [ ] Onglet "Prix & Méthodes" avec scatter plots
- [ ] Sidebar avec filtres fonctionnels
- [ ] Téléchargement CSV en bas de la sidebar

### Performance :
- [ ] Chargement rapide (< 10 secondes)
- [ ] Pas d'erreurs dans la console
- [ ] Responsive design (fonctionne sur différentes tailles d'écran)

---

## 🐛 Résolution de problèmes courants

### Problème : "Module not found"
```bash
# Solution : Installer les dépendances
pip install -r requierements.txt
```

### Problème : "Fichier dataset/adidas.csv introuvable"
```bash
# Vérifier la présence du fichier
ls dataset/adidas.csv

# Si absent, le télécharger depuis Google Drive ou autre source
```

### Problème : Port 8501 occupé
```bash
# Voir qui utilise le port
netstat -tulpn | grep 8501

# Utiliser un autre port
streamlit run app.py --server.port 8502
```

### Problème : Docker - "Port already in use"
```bash
# Arrêter le conteneur existant
docker stop streamlit-adidas-container
docker rm streamlit-adidas-container

# Ou utiliser un autre port
docker run -d --name streamlit-adidas-container -p 8502:8501 streamlit-adidas-app
```

### Problème : Images ne s'affichent pas
```bash
# Vérifier la présence des images
ls images/

# Vérifier les chemins dans app.py (doivent être relatifs)
```

### Problème : Permission denied sur les scripts
```bash
# Rendre les scripts exécutables
chmod +x build.sh run.sh stop.sh test.sh
```

---

## 🎯 Commandes de démarrage rapide

### Pour développement (local) :
```bash
cd "/c/Users/HK6691/OneDrive - ENGIE/Bureau/Streamlit-main"
pip install -r requierements.txt
streamlit run app.py
```

### Pour production (Docker) - Méthode rapide :
```bash
cd "/c/Users/HK6691/OneDrive - ENGIE/Bureau/Streamlit-main"
chmod +x build.sh run.sh
./build.sh && ./run.sh
```

### Pour production (Docker) - Étape par étape :
```bash
cd "/c/Users/HK6691/OneDrive - ENGIE/Bureau/Streamlit-main"

# 1. Construire l'image
chmod +x build.sh
./build.sh

# 2. Lancer l'application
chmod +x run.sh
./run.sh

# 3. (Optionnel) Tester
chmod +x test.sh
./test.sh
```

---

## 📊 URLs et informations importantes

- **Application locale** : http://localhost:8501
- **Port par défaut** : 8501
- **Logs Streamlit** : Visibles dans le terminal
- **Logs Docker** : `docker logs streamlit-adidas-container`
- **Arrêt local** : `Ctrl+C` dans le terminal
- **Arrêt Docker** : `./stop.sh` ou `docker stop streamlit-adidas-container`

---

## 🏆 Déploiement recommandé selon le contexte

| Contexte | Méthode | Commande |
|----------|---------|----------|
| **Développement/Test** | Local Direct | `streamlit run app.py` |
| **Démonstration** | Docker Scripts | `./build.sh && ./run.sh` |
| **Production** | Docker Manuel | `docker build` + `docker run` |

---

## 📋 Ordre de déploiement recommandé

### 🥇 **Méthode 1 : Test local rapide**
```bash
# Navigation
cd "/c/Users/HK6691/OneDrive - ENGIE/Bureau/Streamlit-main"

# Installation et test
pip install -r requierements.txt
streamlit run app.py
```
**➡️ Ouvrir http://localhost:8501**

### 🥈 **Méthode 2 : Docker avec scripts (Recommandé)**
```bash
# Rendre les scripts exécutables
chmod +x build.sh run.sh stop.sh test.sh

# Construction et lancement
./build.sh
./run.sh

# Optionnel : test automatisé
./test.sh
```
**➡️ Ouvrir http://localhost:8501**

### 🥉 **Méthode 3 : Docker manuel (Contrôle total)**
```bash
# Construction
docker build -t streamlit-adidas-app .

# Lancement
docker run -d --name streamlit-adidas-container -p 8501:8501 streamlit-adidas-app

# Vérification
docker ps && docker logs streamlit-adidas-container
```

**🎉 Votre application Streamlit Adidas est maintenant prête à être déployée !**