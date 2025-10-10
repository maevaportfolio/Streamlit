import streamlit as st
import pandas as pd

import numpy as np
import plotly.express as px
from pathlib import Path
from datetime import datetime
import random
import base64
import plotly.graph_objects as go
from PIL import Image
import time

# -------------------------
# Animation initiale
# -------------------------
splash = st.empty()  # conteneur temporaire

# Affichage du GIF centré
splash.markdown("""
<div style="display:flex; flex-direction:column; justify-content:center; align-items:center; height:80vh;">
    <h2 style="color:#FFFFFF; margin-bottom:20px;">Chargement...</h2>
    <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcjZ6YWhpaTh5bThwN2U4MjM3ZW9pM3RvNWFmMngxaW1icXpkMW5yaiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/jGFOU6WSXrSzm/giphy.gif" 
         style="max-width:400px; max-height:400px;">
</div>
""", unsafe_allow_html=True)

# Attendre 2 secondes
time.sleep(2)

# Supprimer le GIF et afficher le reste du Streamlit
splash.empty()


# =========================================
# INITIALISATION DE SESSION STATE
# =========================================
st.set_page_config(layout="wide", page_icon="images/adidas_icone_site.jpg")
if "page" not in st.session_state:
    st.session_state["page"] = "Vue globale"  # Valeur par défaut


# =======================
# --- Styles globaux ---
# =======================
st.markdown("""
<style>
/* Fond blanc et titres gras */
.stApp { background-color: #ffffff !important; }
h1, h2, h3, h4, h5, h6 { font-weight: bold !important; }

/* Texte Markdown */
.stMarkdown p {
    font-weight: bold !important;
    font-size: 16px !important;
}

/* Tableaux */
.stDataFrame table td, .stDataFrame table th {
    font-size: 14px !important;
    font-weight: bold !important;
}

/* Texte Plotly */
.plotly .main-svg text {
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

# =======================
# --- Logos Adidas ---
# =======================
logo_path = "images/logo.png"
with open(logo_path, "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode()

# Générer logos sur une grille (10x10)
num_cols = 10
num_rows = 10
cell_width = 100 / num_cols
cell_height = 100 / num_rows

logos_html = ""
for row in range(num_rows):
    for col in range(num_cols):
        top = row * cell_height + random.uniform(0, cell_height - 10)
        left = col * cell_width + random.uniform(0, cell_width - 10)
        size = random.randint(60, 90)
        opacity = random.uniform(0.1, 0.15)
        logos_html += f"""
        <div style="
            position: fixed;
            top: {top}%;
            left: {left}%;
            width: {size}px;
            height: {size}px;
            background-image: url('data:image/png;base64,{logo_b64}');
            background-size: contain;
            background-repeat: no-repeat;
            opacity: {opacity};
            z-index: 0;
            pointer-events: none;
        "></div>
        """

st.markdown(logos_html, unsafe_allow_html=True)
# -------------------------
# Preprocessing
# -------------------------

def clean_currency(x):
    if pd.isna(x):
        return np.nan
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x).replace('$', '').replace(',', '').strip()
    try:
        return float(s)
    except:
        return np.nan

@st.cache_data
def load_data(path="dataset/adidas.csv"):
    p = Path(path)
    if not p.exists():
        st.error(f"Fichier introuvable : {path}. Place 'adidas.csv' dans dataset/.")
        st.stop()
    df = pd.read_csv(p)
    df.columns = [c.strip() for c in df.columns]
    expected = ["Retailer","Retailer ID","Invoice Date","Region","State","City","Product",
                "Price per Unit","Units Sold","Total Sales","Operating Profit","Sales Method"]
    missing = [c for c in expected if c not in df.columns]
    if missing:
        st.error("Colonnes manquantes dans dataset : " + ", ".join(missing))
        st.stop()

    df = df.drop([6529,6530,6531,6532]) # Suppression lignes à vars manquantes
    df.loc[df["Product"] == "Men's aparel", "Product"] = "Men's Apparel" # Correction
    # Colonnes
    df["Price per Unit"] = df["Price per Unit"].apply(clean_currency)
    df["Operating Profit"] = df["Operating Profit"].apply(clean_currency)
    df["Units Sold"] = pd.to_numeric(df["Units Sold"], errors="coerce").fillna(0).astype(int)
    df["Total Sales"] = df["Total Sales"].apply(clean_currency)
    df["Invoice Date"] = pd.to_datetime(df["Invoice Date"], format="%m/%d/%Y", errors="coerce")
    # Nouvelles colonnes
    df["YearMonth"] = df["Invoice Date"].dt.to_period("M").dt.to_timestamp()
    df["Margin (€)"] = df["Operating Profit"]
    df["Margin (%)"] = np.where(df["Total Sales"] > 0, df["Operating Profit"] / df["Total Sales"], np.nan)
    df["Price"] = round(df["Total Sales"] / df["Units Sold"], 2).apply(clean_currency)
    df["Total Cost"] = round(df["Total Sales"] - df["Operating Profit"], 2).apply(clean_currency)
    df["Sexe"] = np.where(
    df["Product"].str.contains("Men", case=True, na=False), "Men",
    np.where(df["Product"].str.contains("Women", case=True, na=False), "Women", "Unisex")
    )
    return df


# -------------------------
# Load data
# -------------------------

df = load_data("dataset/adidas.csv")

# Mapping noms -> abréviations
state_to_code = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH",
    "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
    "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
    "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN",
    "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
}
df["Code"] = df["State"].map(state_to_code)

# Pour gradients de couleurs
dark_blue = px.colors.sequential.Blues[2:]  
dark_green = px.colors.sequential.Greens[2:]
dark_orange = px.colors.sequential.Oranges[2:]
dark_purple = px.colors.sequential.Purples[2:]
dark_bleu_vert = px.colors.sequential.Teal        # bleu-vert
dark_rose_violet = px.colors.sequential.Magenta   # rose-violet
dark_rouge = px.colors.sequential.Reds            # rouge


# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.image("images/Adidas-Logo.png",caption="") # Logo Adidas
st.sidebar.header("Filtres")

# Intervalle de dates
date_range = st.sidebar.slider(
    "Période :",
    min_value=df["Invoice Date"].min().date(),
    max_value=df["Invoice Date"].max().date(),
    value=(df["Invoice Date"].min().date(), df["Invoice Date"].max().date())
)

# Region
select_all = st.sidebar.checkbox("Toutes les régions", value=True)
regions = df["Region"].unique().tolist() 
if select_all:
    # Si "Tout" est coché, toutes les régions sont sélectionnées
    selected_region = regions
else:
    # Sinon, on choisit une case pour chaque région
    selected_region = []
    for region in regions:
        if st.sidebar.checkbox(region):
            selected_region.append(region)

# Produit
product_options = ["Tous"] + sorted(df["Product"].dropna().unique().tolist())
selected_product = st.sidebar.selectbox("Sélectionnez le Produit :", product_options, index=0)

# Retailer
retailer_options = ["Tous"] + sorted(df["Retailer"].dropna().unique().tolist())
selected_retailer = st.sidebar.selectbox("Sélectionnez le Fournisseur :", retailer_options, index=0)

# Canal / Méthode de vente
selected_channel = st.sidebar.multiselect(
    "Sélectionnez le Canal :",
    options=df["Sales Method"].unique(),
    default=df["Sales Method"].unique()
)


if selected_product == "Tous":
    product_filter = df["Product"].notna()
else:
    product_filter = df["Product"] == selected_product

# Appliquer filtre Retailer
if selected_retailer != "Tous":
    df= df[df["Retailer"] == selected_retailer]

# Appliquer filtre Produit
if selected_product != "Tous":
    df = df[df["Product"] == selected_product]


df_filtered = df[
    (df["Region"].isin(selected_region)) &
    (df["Sales Method"].isin(selected_channel)) &
    product_filter &
    (df["Invoice Date"].dt.date >= date_range[0]) &
    (df["Invoice Date"].dt.date <= date_range[1])
]

# # Appliquer filtre Retailer
# if selected_retailer != "Tous":
#     df_filtered = df_filtered[df_filtered["Retailer"] == selected_retailer]

# # Appliquer filtre Produit
# if selected_product != "Tous":
#     df_filtered = df_filtered[df_filtered["Product"] == selected_product]


# CSS pour agrandir les tabs
st.markdown("""
    <style>
    /* Agrandir les onglets */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        padding: 0px 24px;
        font-size: 18px;
        font-weight: 600;
    }
    
    /* Optionnel : améliorer l'apparence */
    .stTabs [data-baseweb="tab-list"] button {
        border-radius: 8px 8px 0px 0px;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

# Noms des tabs
tabs = st.tabs(["Accueil", "Vue globale", "Géographie", "Produits",
                "Fournisseurs", "Prix & Méthodes","Conclusion"])


@st.cache_data
def load_committee_images():
    img1 = Image.open("images/Elodie_prix.png")
    img2 = Image.open("images/Julie_produit.png")
    img3 = Image.open("images/mike_geographie.png")
    img4 = Image.open("images/paul_fournisseurs.png")
    return [img1, img2, img3, img4]

# -------------------------
# Page Accueil
# -------------------------
with tabs[0]:
    
    st.markdown("""
        <div style='background: white; 
                    padding: 2rem; 
                    border-radius: 10px; 
                    margin-bottom: 2rem;
                    border-left: 5px solid #000000;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
            <h2 style='color: #1a1a1a; margin: 0; font-weight: 600;'>
                Dashboard Stratégique | Comité d'Entreprise Adidas
            </h2>
            <p style='color: #666666; margin-top: 0.5rem; font-size: 0.95rem;'>
                Réunion annuelle des responsables – 15 mars 2022
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    #st.image("images/Adidas.jpg", caption="Adidas – Analyse du marché US", use_container_width=True)
    

    # Section contexte avec design épuré
    st.markdown("""
    <div style='background-color: #f8f9fa; 
                padding: 1.5rem; 
                border-radius: 8px; 
                border-left: 4px solid #000000;
                margin-bottom: 2rem;'>
        <h3 style='color: #1a1a1a; margin-top: 0; font-size: 1.3rem;'>
            📊 Contexte & Finalité
        </h3>
        <p style='color: #2c3e50; line-height: 1.7; margin-bottom: 1rem;'>
            Ce rapport accompagne le <strong>comité annuel</strong> dans ses décisions stratégiques 
            en offrant une analyse consolidée de la performance d'Adidas sur le marché américain.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Points clés avec icônes
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
    <div style='background-color: white; 
                padding: 1.2rem; 
                border-radius: 8px; 
                border: 2px solid #000000;
                height: 100%;'>
        <h4 style='color: #000000; margin-top: 0;'>🎯 Objectifs</h4>
        <ul style='color: #2c3e50; line-height: 1.8; margin: 0;'>
            <li>Analyser les <strong>ventes 2020-2021</strong></li>
            <li>Identifier les <strong>déterminants du chiffre d'affaires</strong></li>
            <li>Évaluer la <strong>rentabilité par région</strong></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
    <div style='background-color: white; 
                padding: 1.2rem; 
                border-radius: 8px; 
                border: 2px solid #000000;
                height: 100%;'>
        <h4 style='color: #000000; margin-top: 0;'>📈 Périmètre</h4>
        <ul style='color: #2c3e50; line-height: 1.8; margin: 0;'>
            <li>Marché : <strong>États-Unis</strong></li>
            <li>Période : <strong>2020-2021</strong></li>
            <li>Canaux : <strong>Online, In-store, Outlet</strong></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style='background-color: white; 
                padding: 1.5rem; 
                border-radius: 8px; 
                border: 2px solid #000000;
                margin-bottom: 1rem;'>
        <h3 style='color: #1a1a1a; margin-top: 0;'>🎯 Problématique principale</h3>
        <p style='color: #2c3e50; line-height: 1.7; margin: 0;'>
            <strong>Quels sont les principaux déterminants qui influencent le chiffre d’affaires d’Adidas, et quelles actions peuvent être mises en place pour l’augmenter ?</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # --- Photos des responsables du comité ---
    st.markdown("### 👥 Responsables du comité")

    # Chargement des images depuis le cache
    images = load_committee_images()

        # Création de colonnes (autant que d'images)
    cols = st.columns(len(images), gap="large")

    # Affichage horizontal : 1 image par colonne
    for col, img in zip(cols, images):
        with col:
            st.image(img, width=220)
    


    # --- Bouton vers la page Overview ---
    if st.button("🚀 Lancer l'analyse (Overview)"):
        st.session_state["page"] = "Overview"
        st.rerun()  # ✅ relance l'app en gardant l'état


# -------------------------
# Page Overview
# -------------------------
with tabs[1]:
    st.session_state["current_tab"] = "Overview"
    
    if st.session_state["page"] == "Overview":

        # --- Calcul des KPIs actuels ---
        total_sales = df_filtered["Total Sales"].sum()
        total_profit = df_filtered["Operating Profit"].sum()
        total_units = df_filtered["Units Sold"].sum()
        avg_margin_pct = (total_profit / total_sales) if total_sales != 0 else np.nan

        # --- Calcul des KPIs période précédente (2020 vs 2021) ---
        df['Year'] = pd.to_datetime(df['Invoice Date']).dt.year
        
        # KPIs 2021 (période actuelle)
        df_2021 = df[df['Year'] == 2021]
        sales_2021 = df_2021["Total Sales"].sum()
        profit_2021 = df_2021["Operating Profit"].sum()
        units_2021 = df_2021["Units Sold"].sum()
        margin_2021 = (profit_2021 / sales_2021) if sales_2021 != 0 else 0
        
        # KPIs 2020 (période précédente)
        df_2020 = df[df['Year'] == 2020]
        sales_2020 = df_2020["Total Sales"].sum()
        profit_2020 = df_2020["Operating Profit"].sum()
        units_2020 = df_2020["Units Sold"].sum()
        margin_2020 = (profit_2020 / sales_2020) if sales_2020 != 0 else 0

        # Calcul des variations (%)
        delta_sales = ((sales_2021 - sales_2020) / sales_2020 * 100) if sales_2020 != 0 else 0
        delta_profit = ((profit_2021 - profit_2020) / profit_2020 * 100) if profit_2020 != 0 else 0
        delta_units = ((units_2021 - units_2020) / units_2020 * 100) if units_2020 != 0 else 0
        delta_margin = (margin_2021 - margin_2020) * 100

        # Fonction pour générer les KPI avec polices agrandies
        def kpi_card(title, value, delta_pct):
            # Déterminer la couleur et la flèche
            if delta_pct > 0:
                color = "#10b981"  # Vert
                arrow = "↑"
                sign = "+"
            elif delta_pct < 0:
                color = "#ef4444"  # Rouge
                arrow = "↓"
                sign = ""
            else:
                color = "#6b7280"  # Gris
                arrow = "→"
                sign = ""
            
            delta_html = f"""
            <div style='font-size:16px; color:{color}; font-weight:600; margin-top:8px;'>
                <span style='font-size:20px;'>{arrow}</span> {sign}{delta_pct:.1f}%
            </div>
            """ if delta_pct != 0 else "<div style='height:30px;'></div>"
            
            return f"""
            <div style="
                background-color: white; 
                padding: 24px; 
                border-radius: 8px; 
                text-align: center; 
                border: 1px solid #e5e7eb;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05); 
                font-family: 'Inter', sans-serif;
                height: 100%;
                min-height: 160px;
            ">
                <div style="font-size:15px; font-weight:600; color:#6b7280; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:12px;">
                    {title}
                </div>
                <div style="font-size:34px; font-weight:700; margin-top:8px; color:#111827; line-height:1.2;">
                    {value}
                </div>
                {delta_html}
            </div>
            """

        k1, k2, k3, k4 = st.columns(4)
        k1.markdown(
            kpi_card("Chiffre d'affaires", f"${total_sales:,.0f}", delta_sales), 
            unsafe_allow_html=True
        )
        k2.markdown(
            kpi_card("Profit opérationnel", f"${total_profit:,.0f}", delta_profit), 
            unsafe_allow_html=True
        )
        k3.markdown(
            kpi_card("Unités vendues", f"{total_units:,d}", delta_units), 
            unsafe_allow_html=True
        )
        k4.markdown(
            kpi_card("Marge moyenne", f"{avg_margin_pct:.1%}", delta_margin), 
            unsafe_allow_html=True
        )

        st.markdown("---")
    # ---------------------------------------
    # Analyse temporelle & saisonnalité
    # ---------------------------------------

    st.subheader(" Évolution temporelle du chiffre d’affaires et du profit")

    # --- Agrégation mensuelle ---
    df_time = (
        df_filtered.groupby("YearMonth", as_index=False)
        .agg({
            "Total Sales": "sum",
            "Operating Profit": "sum",
            "Units Sold": "sum",
            "Price per Unit": "mean",
            "Total Cost": "sum"
        })
        .sort_values("YearMonth")
    )

    # --- Calcul des croissances ---
    def growth(current, previous):
        if previous == 0 or np.isnan(previous):
            return np.nan
        return (current - previous) / previous

    if len(df_time) >= 2:
        current = df_time.iloc[-1]
        previous = df_time.iloc[-2]

        growth_sales = growth(current["Total Sales"], previous["Total Sales"])
        growth_profit = growth(current["Operating Profit"], previous["Operating Profit"])
        growth_units = growth(current["Units Sold"], previous["Units Sold"])
        growth_price = growth(current["Price per Unit"], previous["Price per Unit"])
        growth_cost = growth(current["Total Cost"], previous["Total Cost"])
    else:
        growth_sales = growth_profit = growth_units = growth_price = growth_cost = np.nan



    # --- Graphique temporel ---
    fig_time = go.Figure()

    fig_time.add_trace(go.Scatter(
        x=df_time["YearMonth"], y=df_time["Total Sales"],
        mode="lines+markers", name="Chiffre d'affaires",
        line=dict(width=3)
    ))
    fig_time.add_trace(go.Scatter(
        x=df_time["YearMonth"], y=df_time["Operating Profit"],
        mode="lines+markers", name="Profit opérationnel",
        line=dict(width=3, dash="dot")
    ))

    fig_time.update_layout(
    xaxis_title="Mois",
    yaxis_title="Montants ($)",
    plot_bgcolor="white",
    paper_bgcolor="white",
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    font=dict(color="black"),          # <-- texte général en noir
    xaxis=dict(title_font=dict(color="black"), tickfont=dict(color="black")),
    yaxis=dict(title_font=dict(color="black"), tickfont=dict(color="black"))
)

    st.plotly_chart(fig_time, use_container_width=True)


    # --- Bouton de retour à l’accueil ---
    if st.button("⬅️ Retour à l’accueil"):
        st.session_state["page"] = "Accueil"
        st.rerun()

    else:
        st.info("👉 Cliquez sur *Lancer l'analyse* dans l’Accueil pour voir les résultats.")

# -------------------------
# Autres onglets
# -------------------------
with tabs[2]:
    st.header("🌍 Analyse Géographique")

    # --- Style pour les commentaires (comme pour les fournisseurs) ---
    st.markdown("""
    <style>
        .insight {
            font-size: 17px !important;
            font-weight: bold !important;
            color: #222;
            background-color: #f9f9f9;
            padding: 8px 14px;
            border-left: 4px solid #1f77b4;
            border-radius: 6px;
            margin-top: 6px;
            margin-bottom: 6px;
        }
    </style>
    """, unsafe_allow_html=True)

    # =======================
    # --- Carte + Tableaux côte à côte ---
    # =======================
    col_map, col_tables = st.columns([2, 1])

    with col_map:
        df_sum = df_filtered.groupby(["State", "Code"], as_index=False)["Operating Profit"].sum()
        fig_map = px.choropleth(
            df_sum,
            locations="Code",
            locationmode="USA-states",
            color="Operating Profit",
            scope="usa",
            hover_name="State",
            hover_data={"Operating Profit": ":,.0f"},
            color_continuous_scale=px.colors.sequential.Blues
        )
        scatter_layer = go.Scattergeo(
            locationmode="USA-states",
            locations=df_sum["Code"],
            text=df_sum["Code"],
            mode="text",
            showlegend=False
        )
        fig_map.add_trace(scatter_layer)
        fig_map.update_layout(
            title="Carte : Operating Profit par État (USA)",
            margin=dict(l=0, r=0, t=40, b=0),
            height=400
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with col_tables:
        if not df_sum.empty:
            top2 = df_sum.nlargest(2, "Operating Profit")[["State", "Operating Profit"]]
            bottom2 = df_sum.nsmallest(2, "Operating Profit")[["State", "Operating Profit"]]

            st.markdown("##### 🥇 Top 2 États les plus rentables")
            st.dataframe(
                top2.style.format({"Operating Profit": "${:,.0f}"}),
                use_container_width=True,
                height=120
            )

            st.markdown("##### ⚠ Top 2 États les moins rentables")
            st.dataframe(
                bottom2.style.format({"Operating Profit": "${:,.0f}"}),
                use_container_width=True,
                height=120
            )

    st.markdown("---")

    # =======================
    # --- Chiffre d'affaires et prix moyen ---
    # =======================
    df_sales_price = df_filtered.groupby("Region", as_index=False).agg({
        "Total Sales": "sum",
        "Price per Unit": "mean",
        "Operating Profit": "sum"
    })

    col_sales, col_price = st.columns([2, 1])

    with col_sales:
        fig_sales = px.bar(
            df_sales_price,
            x="Region",
            y="Total Sales",
            text=df_sales_price["Total Sales"].round(0),
            color="Total Sales",
            color_continuous_scale=px.colors.sequential.Blues,
            title="Chiffre d'affaires par Région (avec prix moyen)"
        )
        fig_sales.update_traces(texttemplate='%{text}', textposition='outside')
        fig_sales.update_layout(margin=dict(l=0, r=0, t=40, b=0), height=350)
        st.plotly_chart(fig_sales, use_container_width=True)

    with col_price:
        st.markdown("##### 💡 Prix moyen par région (USD)")
        st.dataframe(df_sales_price[["Region", "Price per Unit"]].round(2), use_container_width=True, height=200)

    st.markdown("---")

    # =======================
    # --- Répartition des canaux de vente ---
    # =======================
    st.subheader("📊 Répartition des canaux de vente par région")

    df_filtered["Sales Method"] = df_filtered["Sales Method"].str.strip().str.title()
    unique_channels = df_filtered["Sales Method"].unique()

    # 🔵 Palette bleue plus foncée pour les camemberts
    dark_blue_palette = px.colors.sequential.Blues[3:]

    # Organisation en une seule ligne
    regions_order = ["West", "Northeast", "Midwest", "South"]
    selected_regions_present = [r for r in regions_order if r in selected_region]

    if selected_regions_present:
        cols = st.columns(len(selected_regions_present))
        for i, region in enumerate(selected_regions_present):
            df_region = df_filtered[df_filtered["Region"] == region]
            df_method = df_region.groupby("Sales Method", as_index=False).size().rename(columns={"size": "Count"})

            if df_method.empty:
                cols[i].warning(f"Aucune donnée pour {region}")
                continue

            df_method["Pourcentage"] = (df_method["Count"] / df_method["Count"].sum() * 100).round(1)

            fig = go.Figure(go.Pie(
                labels=df_method["Sales Method"],
                values=df_method["Count"],
                hole=0.45,
                marker_colors=dark_blue_palette[:len(df_method)],
                textinfo='percent+label',
                textposition='inside',
                insidetextfont=dict(size=15)
            ))
            fig.update_layout(
                title_text=f"{region}",
                height=320,
                margin=dict(l=0, r=0, t=40, b=0),
                showlegend=False,
                title_font=dict(size=18)
            )
            cols[i].plotly_chart(fig, use_container_width=True)

        # === Commentaires dynamiques stylisés ===
        if set(selected_regions_present) >= {"West", "Northeast"}:
            st.markdown("""
                <div class='insight'>
                🌎 Les régions <b>West</b> et <b>Northeast</b> ont des distributions de canaux assez similaires 
                et représentent les meilleurs profits parmi les régions analysées.
                </div>
            """, unsafe_allow_html=True)

        if set(selected_regions_present) >= {"Midwest", "South"}:
            st.markdown("""
                <div class='insight'>
                📉 Les régions <b>Midwest</b> et <b>South</b> montrent plus de déséquilibre dans la répartition des canaux 
                et correspondent aux profits les plus faibles parmi les régions analysées.
                </div>
            """, unsafe_allow_html=True)

# -------------------------
# Products tab
# -------------------------

with tabs[3]:
    st.header("👟Analyse de la composante Produit")

    # Treemap du CA par produit, coloré par la marge
    ### Aggrégation par produit du CA et du profit
    marge_produit = df_filtered.groupby("Product").agg(
        TotalSales=("Total Sales", "sum"),
        Profit=("Operating Profit", "sum")
    ).reset_index()
    ###
    total_sales_all = marge_produit["TotalSales"].sum()
    marge_produit["margin_ratio"] = marge_produit["Profit"] / marge_produit["TotalSales"].replace({0: np.nan})
    marge_produit["sales_share"] = marge_produit["TotalSales"] / total_sales_all

    fig_margin = px.treemap(
        marge_produit,
        path=["Product"],
        values="TotalSales",
        color="margin_ratio",
        color_continuous_scale=dark_blue,
        title="Chiffre d'Affaires par produit (couleur = marge)"
    )
    fig_margin.update_traces(
        texttemplate="<b>%{label}</b><br>"
                     "CA : %{value:$,.0f}<br>"
                     "Part : %{customdata[1]:.1%}<br>"
                     "Marge : %{customdata[0]:.1%}",
        hovertemplate="<b>%{label}</b><br>"
                      "CA : %{value:$,.0f}<br>"
                      "Part du CA : %{customdata[1]:.1%}<br>"
                      "Marge : %{customdata[0]:.1%}<br>",
        customdata=marge_produit[["margin_ratio", "sales_share"]].values
    )
    fig_margin.update_layout(
        title_x=0.5,  # ✅ titre centré
        paper_bgcolor="rgba(0,0,0,0)",  # ✅ fond transparent
        plot_bgcolor="rgba(0,0,0,0)",   # ✅ fond transparent
        margin=dict(t=60, b=10, l=0, r=0)
    )
    st.plotly_chart(fig_margin, use_container_width=True)

 # --- Deux graphiques côte à côte ---
    col1, col2 = st.columns(2)

    with col1:
        # Donut chart : Répartition des unités vendues par sexe
        ventes_sexe = df_filtered.groupby("Sexe", as_index=False)["Units Sold"].sum()

        fig_donut = px.pie(
            ventes_sexe,
            names="Sexe",
            values="Units Sold",
            color="Sexe",
            color_discrete_map={
                "Men": "#043E78",     # Bleu
                "Women": "#CF0B15"   # Rouge
            },
            title="Répartition des Unités Vendues par Genre",
            hole=0.6
        )

        # Symbole homme/femme au centre du donut
        fig_donut.add_annotation(
            text="♂♀",
            x=0.5, y=0.5,
            font_size=35,
            showarrow=False,
            font_color="#000000"
        )

        # Ajustements visuels
        fig_donut.update_traces(
            textposition="inside",
            textinfo="percent+label",
            textfont_size=12,
            pull=[0.02, 0.02, 0.02]
        )
        fig_donut.update_layout(
            showlegend=True,
            legend_title_text="Genre",
            title_x=0.0,  # titre aligné à gauche
            width=360,    # ✅ taille réduite
            height=360,   # ✅ taille réduite
            margin=dict(t=60, b=10, l=0, r=0)
        )

        st.plotly_chart(fig_donut, use_container_width=True)
            

    with col2:
        # Bar chart horizontal : Prix moyen par produit
        prix_moyen = df_filtered.groupby(["Product", "Sexe"], as_index=False)["Price per Unit"].mean()
        prix_moyen = prix_moyen.sort_values("Price per Unit", ascending=True)

        fig_bar = px.bar(
            prix_moyen,
            x="Price per Unit",
            y="Product",
            orientation="h",
            text="Price per Unit",
            color="Sexe",
            color_discrete_map={
                "Men": "#043E78",     # Bleu
                "Women": "#CF0B15"   # Rouge
            },
            title="Prix Moyen par Produit (par Genre)"
        )

        # Affichage du texte à l'intérieur des barres en dollars
        fig_bar.update_traces(
            texttemplate="$%{text:.2f}",
            textposition="inside",
            insidetextanchor="middle",
            textfont_size=12
        )

        fig_bar.update_layout(
            showlegend=True,
            xaxis_title="Prix moyen ($)",
            yaxis_title="Produit",
            title_x=0.0,  # titre aligné à gauche
            width=380,    # ✅ taille réduitede
            height=380,   # ✅ taille réduite
            margin=dict(t=60, b=10, l=10, r=40)
        )

        st.plotly_chart(fig_bar, use_container_width=True)
    ## Commentaire dynamique
    if "Women" in prix_moyen["Sexe"].values:
        prix_femmes = prix_moyen[prix_moyen["Sexe"] == "Women"]["Price per Unit"].mean()
        prix_hommes = prix_moyen[prix_moyen["Sexe"] == "Men"]["Price per Unit"].mean()
        if prix_femmes > prix_hommes:   
            st.markdown(f"""
                <div class='insight'>
                    Le prix moyen des produits pour femmes (${prix_femmes:.2f}) est supérieur à celui des produits pour hommes (${prix_hommes:.2f}).
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class='insight'>
                    Le prix moyen des produits pour hommes (${prix_hommes:.2f}) est supérieur à celui des produits pour femmes (${prix_femmes:.2f}).
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class='insight'>
                Tous les produits analysés sont destinés aux hommes, ce qui pourrait indiquer une opportunité de diversification vers des produits pour femmes.
            </div>
        """, unsafe_allow_html=True)    
                
with tabs[4]:
    st.header("🏬 Analyse Fournisseurs - Profit, Ventes et Catégories")

    # --- Style : commentaires lisibles mais compacts ---
    st.markdown("""
    <style>
        .insight {
            font-size: 17px !important;
            font-weight: bold !important;
            color: #222;
            background-color: #f9f9f9;
            padding: 8px 14px;
            border-left: 4px solid #1f77b4;
            border-radius: 6px;
            margin-top: 6px;
            margin-bottom: 6px;
        }
    </style>
    """, unsafe_allow_html=True)

    # =======================
    # --- PROFIT + TOP 2 CATÉGORIES côte à côte ---
    # =======================
    col1, col2 = st.columns(2)

    with col1:
        df_profit = df_filtered.groupby("Retailer", as_index=False)["Operating Profit"].sum().sort_values("Operating Profit", ascending=False)
        fig_profit = px.bar(
            df_profit,
            x="Retailer",
            y="Operating Profit",
            text="Operating Profit",
            color="Operating Profit",
            color_continuous_scale=px.colors.sequential.Blues[3:],  # bleu foncé
            title="Profit par Retailer"
        )
        fig_profit.update_traces(texttemplate='%{text}', textposition='outside')
        fig_profit.update_layout(
            margin=dict(l=10, r=10, t=40, b=10),
            height=350,
            title_font=dict(size=18)
        )
        st.plotly_chart(fig_profit, use_container_width=True)

    with col2:
        df_cat = df_filtered.groupby(["Retailer", "Product"], as_index=False)["Units Sold"].sum()
        df_cat = df_cat.sort_values(["Retailer", "Units Sold"], ascending=[True, False])
        df_top2_cat = df_cat.groupby("Retailer").head(2)

        fig_top2_cat = px.bar(
            df_top2_cat,
            x="Retailer",
            y="Units Sold",
            text="Units Sold",
            color="Product",
            color_discrete_sequence=px.colors.sequential.Blues[2:],
            title="Top 2 Catégories vendues (Units Sold)"
        )
        fig_top2_cat.update_traces(texttemplate='%{text}', textposition='outside')
        fig_top2_cat.update_layout(
            margin=dict(l=10, r=10, t=40, b=10),
            height=350,
            title_font=dict(size=18)
        )
        st.plotly_chart(fig_top2_cat, use_container_width=True)

    # --- Détection automatique : fournisseurs vendant uniquement des produits hommes ---
    df_top2_cat["is_men"] = df_top2_cat["Product"].str.contains("Men", case=False)
    fournisseurs_hommes = (
        df_top2_cat.groupby("Retailer")["is_men"]
        .apply(lambda x: x.all())
        .reset_index()
    )
    fournisseurs_hommes = fournisseurs_hommes[fournisseurs_hommes["is_men"] == True]["Retailer"].tolist()

    if len(fournisseurs_hommes) > 0:
        st.markdown(
            f"<div class='insight'>🧍 Les fournisseurs <b>{', '.join(fournisseurs_hommes)}</b> vendent uniquement des <b>produits hommes</b> parmi leurs deux meilleures catégories.</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown("<div class='insight'>Aucun retailer ne vend exclusivement des produits hommes dans son top 2 catégories.</div>", unsafe_allow_html=True)

    st.markdown("---")

    # =======================
    # --- ÉVOLUTION DES VENTES DANS LE TEMPS ---
    # =======================
# =======================
# --- ÉVOLUTION DES VENTES DANS LE TEMPS ---
# =======================
    df_time = df_filtered.copy()
    df_time["Month"] = df_time["Invoice Date"].dt.to_period("M").astype(str)
    df_time_grouped = df_time.groupby(["Month", "Retailer"], as_index=False)["Total Sales"].sum()

    fig_time = px.line(
        df_time_grouped,
        x="Month",
        y="Total Sales",
        color="Retailer",  # chaque Retailer a sa couleur unique
        title="Évolution des Total Sales par Retailer"
        # markers=True  -> supprimé pour ne plus afficher les points
    )
    fig_time.update_layout(
        xaxis_tickangle=-45,
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        title_font=dict(size=18)
    )
    st.plotly_chart(fig_time, use_container_width=True)


    # =======================
    # --- Détection automatique des pics saisonniers ---
    # =======================
    df_time_grouped["Month_dt"] = pd.to_datetime(df_time_grouped["Month"])
    df_time_grouped["month_num"] = df_time_grouped["Month_dt"].dt.month
    df_peak = df_time_grouped.loc[df_time_grouped.groupby("Retailer")["Total Sales"].idxmax()]

    christmas_fournisseurs = df_peak[df_peak["month_num"].isin([12, 1])]["Retailer"].tolist()
    backtoschool_fournisseurs = df_peak[df_peak["month_num"].isin([9, 10])]["Retailer"].tolist()

    if christmas_fournisseurs or backtoschool_fournisseurs:
        text = ""
        if christmas_fournisseurs:
            text += f"🎄 Le pic de ventes en <b>décembre-janvier</b> concerne <b>{', '.join(christmas_fournisseurs)}</b>, probablement lié aux <b>promotions de Noël</b>.  "
        if backtoschool_fournisseurs:
            text += f"🎒 Les pics de <b>septembre-octobre</b> concernent <b>{', '.join(backtoschool_fournisseurs)}</b>, liés aux <b>promotions de rentrée</b>."
        st.markdown(f"<div class='insight'>{text}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='insight'>Aucun pic saisonnier clair détecté pour les fournisseurs dans la période sélectionnée.</div>", unsafe_allow_html=True)

with tabs[5]:
    st.header("🛒 Analyse du prix et du canal sur les ventes")

    # -----------------------------------------------------------
    # PRÉPARATION DES DONNÉES
    # -----------------------------------------------------------
    df_price_channel = df_filtered.groupby("Sales Method").agg({
        "Price per Unit": "mean",
        "Units Sold": "sum"
    }).reset_index()

    df_channel_perf = df_filtered.groupby("Sales Method").agg({
        "Total Sales": "sum"
    }).reset_index()

    # -----------------------------------------------------------
    # LAYOUT EN 2 COLONNES
    # -----------------------------------------------------------
    col1, col2 = st.columns(2)

    # -----------------------------------------------------------
    # GRAPHIQUE 1 : Sensibilité au prix (colonne gauche)
    # -----------------------------------------------------------
    with col1:
        st.markdown("#### 📈 Sensibilité au prix")
        
        fig1 = px.scatter(
            df_price_channel,
            x="Price per Unit",
            y="Units Sold",
            color="Sales Method",
            size="Units Sold",
            text="Sales Method",
            labels={"Price per Unit": "Prix moyen (€)", "Units Sold": "Unités vendues"},
            height=400
        )
        fig1.update_traces(textposition="top center")
        fig1.update_layout(
            plot_bgcolor="white", 
            paper_bgcolor="white",
            margin=dict(l=20, r=20, t=40, b=20),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        st.markdown(
            """
            <div style="background-color:#f8f9fa; padding:12px; border-radius:6px; margin-top:10px;">
                <span style="font-size:14px; color:#2c3e50;">
                    💡 Les canaux <b>Online</b> et <b>Outlet</b> montrent une forte sensibilité au prix : 
                    plus le prix baisse, plus les ventes augmentent.
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # -----------------------------------------------------------
    # GRAPHIQUE 2 : Comparaison des canaux (colonne droite)
    # -----------------------------------------------------------
    with col2:
        st.markdown("#### 🏷️ Performance par canal")
        
        fig2 = px.bar(
            df_channel_perf,
            x="Sales Method",
            y="Total Sales",
            text_auto='.2s',
            color="Sales Method",
            labels={
                "Sales Method": "Canal de vente",
                "Total Sales": "Chiffre d'affaires (€)"
            },
            height=400
        )
        fig2.update_layout(
            plot_bgcolor="white", 
            paper_bgcolor="white",
            margin=dict(l=20, r=20, t=40, b=20),
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown(
            """
            <div style="background-color:#f8f9fa; padding:12px; border-radius:6px; margin-top:10px;">
                <span style="font-size:14px; color:#2c3e50;">
                    💡 Le canal <b>In-store</b> génère le chiffre d'affaires le plus élevé, 
                    atteignant <b>35,66M €</b>.
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )


# -------------------------
# Conclusion
# -------------------------
with tabs[6]:

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center; background-color:#f9f9f9; padding:20px; border-radius:10px;'>
        <h3 style='color:#000000; font-weight:bold;'> Conclusion</h3>
        <p style='color:#000000; font-size:16px;'>
            Blabla blabla et voilà.
        </p>
        <img src="https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3a2szZHFxaDN0NTByYm1kNXVxN283OGh6cng1YXBqNmo5eWRqNXNmZiZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/UaowfCTS0INxkW48N4/giphy.gif" 
            alt="animation" style="width:150px; margin-top:10px;">
    </div>
    """, unsafe_allow_html=True)







# -------------------------
# Export filtered data        
# -------------------------
st.sidebar.markdown("---")
st.sidebar.download_button(
    "⬇ Télécharger données filtrées (CSV)", 
    df_filtered.to_csv(index=False).encode('utf-8'), 
    file_name="adidas_filtered.csv"
)