# Déploiement Docker de l’Application Streamlit : Adidas Sales Performance Dashboard

Dans un premier temps, nous allons expliquer comment lancer l'application sur votre système d'exploitation à l’aide de Docker. L’objectif est de garantir que chacun dispose du même environnement, afin d’éviter les différences de configuration entre nos machines.

Une fois l’application démarrée, nous présenterons ensuite le Dashboard Adidas : son objectif, sa logique d’analyse et les principaux indicateurs qu’il met en avant.

| **Lien de l’application** |
|------------------------------|
|[Accéder au dashboard en ligne 🔗](https://app-m6mwbx8fwhwhedavfmnc4b.streamlit.app/)  |

--- 

## 🚀 **Lancer l'application avec Docker**

### Étape 1 — Cloner le dépôt :

Ouvre ton terminal (ou VS Code) et exécute :

```bash
git clone https://github.com/maevaportfolio/Streamlit.git
```

```bash
cd ton_repo
```

--- 

### Étape 2 — Passer sur la bonne branche

Nous avons deux branches :

| Branche              | Rôle                                              |
|----------------------|--------------------------------------------------|
| `main`               | Version stable / application locale              |
| `deployment_branch`  | Travail collaboratif + déploiement Docker (✅ nous travaillons ici) |


La branche principale de travail est **deployment_branch**.
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

### Étape 3 — Vérifier que Docker est installé et ouvert

Télécharger Docker si besoin → https://www.docker.com/products/docker-desktop/

- Lancer Docker Desktop et l'ouvrir avant de continuer

-- 

### Étape 4 — Lancer l'application

Une fois le dépôt cloné, la bonne branche sélectionnée et Docker ouvert,
tu peux lancer l’application avec la commande suivante :

```bash
./deploy.sh
```

Le script deploy.sh va automatiquement :
- Construire l’image Docker
- Lancer le conteneur
- Ouvrir l’application
  

Pour arrêter l'application, il suffit de faire :

```bash
./stop.sh
```
---

## 📎 Structure du projet

| Élément                 | Type               | Description |
|------------------------|-------------------|-------------|
| `dataset/`             | 📁 Dossier        | Contient les données de l’application |
| `images/`              | 📁 Dossier        | Images utilisées dans l’interface |
| `app.py`               | 📜 Script Python  | Application Streamlit principale |
| `Dockerfile`           | 📜 Fichier Docker | Instructions pour construire l'image Docker |
| `deploy.sh`            | 🟢 Script Bash    | Build + run automatisé (script principal) |
| `build.sh`             | 🔧 Script Bash    | Construit l’image Docker |
| `run.sh`               | ⚙️ Script Bash    | Lance le conteneur Docker |
| `stop.sh`              | 🛑 Script Bash    | Arrête le conteneur |
| `test.sh`              | 🧪 Script Bash    | Tests liés au conteneur |
| `requierements.txt`    | 📜 Fichier        | Liste des dépendances Python |
| `README.md`            | 📜 Documentation  | Instructions de lancement |
| `GUIDE-DEPLOIEMENT.md` | 📜 Documentation  | Guide détaillé du déploiement |
| `GUIDE-TEST.md`        | 📜 Documentation  | Guide des scénarios de test |



---

## 📊 **Présentation et analyse du projet**

Ce projet a pour objectif de **visualiser, analyser et interpréter les performances commerciales d’Adidas** à travers un **dashboard interactif Streamlit**.  
L’application permet de mesurer **l’impact des prix, des canaux de vente (online, in-store, outlet)**, les performances par **fournisseurs** et **produits**, ainsi que les disparités **régionales**.

> 🎯 Objectif principal : Fournir un outil d’aide à la décision pour les équipes **pricing, marketing, régionales et commerciales**, afin d’ajuster les politiques tarifaires, les stratégies multicanales et les partenariats de distribution.
---

## 🚀 **Fonctionnalités principales**

| Thématique | Description |
|-------------|-------------|
| 💰 **Impact du prix et du canal** | Analyse de la relation prix moyen ↔ volume ↔ chiffre d’affaires par canal (Online / In-store / Outlet) et visualisation de la sensibilité au prix et identification des canaux prioritaires pour les promotions ou la stratégie premium.|
| 🌍 **Analyse géographique** | Visualisation interactive des performances par région et zone commerciale. |
| 🧮 **Distributeurs (Retailers)** | Analyse de la performance par retail partner (CA, marge, part de marché) |
| 🧠 **Insights Produits** | Mix produit : top ventes, poids mort, performance par catégorie |

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




