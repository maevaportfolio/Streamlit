# 🛒 Adidas Sales Performance Dashboard  

## 🚀 Guide d’installation et configuration de l’espace de travail

Ce document explique comment configurer **le même environnement de travail** que celui utilisé pour le projet.  
👉 **Objectif :** que chaque membre du groupe ait le même setup pour éviter les erreurs de dépendances ou de version.

---

## ⚙️ Étape 1 — Cloner le dépôt :

Ouvre ton terminal (ou VS Code) et exécute :

```bash
git clone https://github.com/maevaportfolio/Streamlit.git
```

```bash
cd ton_repo
```

--- 

## 🌿 Étape 2 — Passer sur la bonne branche

La branche principale de travail est deployment_branch.
Vérifie que tu es dessus :

```bash
git checkout deployment_branch
```

Si la branche n’existe pas encore localement :

```bash
git fetch origin
git checkout -b deployment_branch origin/deployment_branch
```

---

## 🧱 Étape 3 — Configuration de l’environnement Python avec UV

On utilise uv pour gérer l’environnement virtuel et les dépendances (plus rapide que pip classique).

1️⃣ Installer les dépendances de base

Assure-toi d’avoir Python 3.11 et pip installé, puis :

```bash
pip install uv
```

2️⃣ Créer un environnement virtuel

```bash
uv venv
```

3️⃣ Activer l’environnement virtuel

**Sur Windows :**
```bash
.venv\Scripts\activate
```

**Sur Mac/Linux :**
```bash
source .venv/bin/activate
```

4️⃣ Initialiser le projet avec uv

Cela génère les fichiers pyproject.toml et uv.lock :

```bash
uv init
```

5️⃣ Ajouter les dépendances nécessaires

Par exemple pour Streamlit et autres outils :

```bash
uv add streamlit pandas numpy requests
```

💡 Tu peux aussi installer toutes les dépendances du projet (si déjà listées dans pyproject.toml) avec :

```bash
uv sync
```

---

## 🧩 Étape 4 — Faire des modifications

Une fois ton environnement configuré, tu peux coder depuis VS Code.
Quand tu as fini tes modifications :

```bash
git add .
git commit -m "Ajout du script de déploiement Bash"
git push
```

**⚠️ Ne pas push directement sur main — toujours depuis ou vers deployment_branch.**

---

## 🧠 Étape 5 — (Optionnel) Créer ta propre sous-branche

Si tu veux développer une fonctionnalité spécifique :

```bash
git checkout -b feature_nom_branch
git push -u origin feature_nom_branch
```

Ensuite, fais une Pull Request sur GitHub pour intégrer ton travail dans deployment_branch.
  
## 📎 Structure du projet

| Élément                  | Type de fichier/dossier | Description |
|---------------------------|--------------------------|-------------|
| `app/`                   | 📁 Dossier               | Code principal Streamlit |
| `scripts/`               | 📁 Dossier               | Scripts de déploiement (dont Bash) |
| `docker/`                | 📁 Dossier               | Dockerfile et fichiers liés à la containerisation |
| `pyproject.toml`         | 📜 Fichier               | Dépendances gérées par UV |
| `uv.lock`                | 📜 Fichier               | Verrouillage des versions |
| `requirements.txt`       | 📜 Fichier (optionnel)   | Compatibilité avec `pip` classique |
| `README.md`              | 📜 Fichier               | Ce guide d’installation et d’utilisation |
| `deploy.sh`              | 📜 Script Bash           | Script principal de déploiement |



---

## 🔗 **Démo en ligne**

> 🌐 https://app-m6mwbx8fwhwhedavfmnc4b.streamlit.app/*
> 

### **Analyse dynamique des ventes, marges et canaux pour les responsables pricing et stratégie commerciale.**

---

## 📊 **Présentation du projet**

Ce projet a pour objectif de **visualiser, analyser et interpréter les performances commerciales d’Adidas** à travers un **dashboard interactif Streamlit**.  
L’application permet de mesurer **l’impact des prix, des canaux de vente (online, in-store, outlet)**, les performances par **fournisseurs** et **produits**, ainsi que les disparités **régionales**.

> 🎯 **Objectif principal :fournir un outil d’aide à la décision pour les équipes **pricing, marketing, régionales et commerciales**, afin d’ajuster les politiques tarifaires, les stratégies multicanales et les partenariats de distribution.
---

## 🚀 **Fonctionnalités principales**

| Thématique | Description |
|-------------|-------------|
| 💰 **Impact du prix et du canal** | Analyse de la relation prix moyen ↔ volume ↔ chiffre d’affaires par canal (Online / In-store / Outlet) et visualisation de la sensibilité au prix et identification des canaux prioritaires pour les promotions ou la stratégie premium.|
| 🌍 **Analyse géographique** | Visualisation interactive des performances par région et zone commerciale. |
| 🧮 **Distributeurs (Retailers)** | Analyse de la performance par retail partner (CA, marge, part de marché) |
| 🧠 **Insights Produits** | Mix produit : top ventes, poids mort, performance par catégorie |

---

## 🧩 **Stack technique**

| Outil / Librairie | Utilisation |
|--------------------|-------------|
| **Python** | Langage principal pour la transformation et la visualisation des données |
| **Streamlit** | Création du dashboard interactif |
| **Pandas** | Nettoyage, agrégation et filtrage des données |
| **Plotly Express** | Visualisations dynamiques et esthétiques |
| **NumPy** | Calculs statistiques et agrégations |
| **Excel / CSV** | Source initiale de données |

---

## 🧰 **Installation et exécution**

### 1️⃣ Cloner le dépôt :
```bash
git clone https://github.com/maevaportfolio/Streamlit.git

```

### 2️⃣ Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Installer les dépendances :
```bash
pip install -r requirements.txt
```

### 4️⃣ Lancer le dashboard :
```bash
streamlit run app.py
```

L’application sera accessible sur :  
👉 **http://localhost:8501**

---

## 🧭 **Comment utiliser le dashboard**

1. Sélectionner les filtres (période, canal de vente, région, retailer, produit) dans la barre latérale.  
2. Explorer les graphiques interactifs : prix moyen vs volume, CA par canal, carte géographique, top produits, performance retailers.  
3. Lire les interprétations dynamiques sous chaque graphique — elles se mettent à jour automatiquement selon les filtres appliqués.  
*Télécharger les données filtrées :
Le dashboard propose un bouton d’export / téléchargement qui permet d’obtenir un CSV correspondant exactement à la sélection active (période, canal, région, etc.).
Utile pour préparer des rapports, envoyer des extraits aux équipes, ou effectuer des analyses complémentaires hors-dashboard.*
5. Utiliser les recommandations générées (par rôle) pour prioriser actions commerciales, promotions et partenariats

---

## 👥 **Public cible**

| Rôle                         | Objectif                                                                                                                        |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **Responsable Partenariats** | Renforcer les collaborations (ex. WestGear, Sports Direct, Foot Locker) et prioriser les retailers à forte contribution.        |
| **Responsable Marketing**    | Lancer des campagnes ciblées (ex. campagnes pour femmes) et mesurer l’impact promo par canal.                                   |
| **Manager Régional**         | Adapter le pricing et le mix canal par région (ex. In-store vs Outlet), optimiser l’allocation des stocks & la présence locale. |
| **Responsable Commercial**   | Ajuster la stratégie tarifaire (notamment online) pour maximiser le CA et la marge.                                             |

---

## 🧩 **Exemples de visualisations**

### 💰 Le profit apr Etat
<img src="https://github.com/user-attachments/assets/a97fda79-b43c-407b-aa8a-0847ba3816c3"/>

### 📊 Analyse du prix et du canal sur les ventes
<img  src="https://github.com/user-attachments/assets/8a279ca6-172a-4cce-b879-3447d3cf2224" />




