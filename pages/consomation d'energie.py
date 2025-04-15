import streamlit as st
import pandas as pd
from PIL import Image
import base64
from io import BytesIO
import plotly.express as px
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Analyse Énergie - Station Wave 2",
    page_icon="⚡",
    layout="wide"
)

st.markdown(
    """
    <style>
        body {
            background-color: #f7f9fc;
        }
        h2 {
            font-family: 'Arial', sans-serif;
            color: #34495e;
            animation: slideIn 1s ease-in-out;
        }
        .kpi-box {
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            font-family: 'Arial', sans-serif;
            color: #2c3e50;
        }
        .stMetric {
            margin-bottom: 15px;
        }
        .footer {
            font-size: 14px;
            color: #7f8c8d;
            text-align: center;
            padding-top: 40px;
            padding-bottom: 20px;
        }
        @keyframes slideIn {
            from { transform: translateX(-50px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Charger les données
df = pd.read_excel('Consommation spécifique.xlsx', sheet_name='Energie')

df['date'] = pd.to_datetime(df['date'])
df['date'] = df['date'].dt.strftime('%d/%m/%Y')  # Format 'dd/mm/yyyy'

# Définir les dates de début et de fin
startDate = pd.to_datetime(df["date"], format='%d/%m/%Y').min()
endDate = pd.to_datetime(df["date"], format='%d/%m/%Y').max()

# Sélection des dates dans la barre latérale
st.sidebar.subheader("Filtrer par période")
date1 = pd.to_datetime(st.sidebar.date_input("Date de début", startDate))
date2 = pd.to_datetime(st.sidebar.date_input("Date de fin", endDate))

# Filtrer les données par plage de dates
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
df = df[(df["date"] >= date1) & (df["date"] <= date2)]
df['date'] = df['date'].dt.strftime('%d/%m/%Y')  # Format pour affichage

# Titre principal
st.markdown("<h2 style='text-align: center;'> Consommation Énergie</h2>", unsafe_allow_html=True)


# Sélection du paramètre pour l'analyse
param = st.sidebar.selectbox(f"Paramètre à visualiser", df.columns[2:])

# Visualisation des données
def consomation_energie(df, param):
    # Indicateurs clés en haut
    st.markdown(
        f"<h3 style='text-align: center; color: #4A90E2;'> {param.capitalize()}</h3>",
        unsafe_allow_html=True
    )



    # Style CSS pour les boîtes KPI
    st.markdown(
        """
        <style>
        .kpi-box {
           background-color: #F9F9F9; 
        border: 1px solid #D1D1D1; 
        border-radius: 8px; 
        padding: 20px; 
        margin: 0 auto 20px auto; 
        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1); 
        width: 60%; /* Ajustez ce pourcentage selon vos besoins */
        max-width: 800px; /* Largeur maximale pour éviter une trop grande expansion */
        }
   
        """,
        unsafe_allow_html=True
    )

    # Colonne 1 : Moyenne

    st.markdown(
        f"""
        <div class="kpi-box">
            <h2 style="
            text-align: center; 
            color: #4A90E2; 
            font-family: Arial, sans-serif; 
            margin-bottom: 0;">
            Consommation journalière : {np.around(df[param].iloc[-1],3)}
            </h2>
        </div>
        """, 
        unsafe_allow_html=True
    )


    # Graphique de la tendance
    fig = px.line(
        df, 
        x="date", 
        y=param, 
        title=f"Tendance de {param.capitalize()} pendant  {date1.strftime('%d/%m/%Y')} - {date2.strftime('%d/%m/%Y')}",
        labels={"date": "Date", param: param.capitalize()},
        template="plotly_white"
    )
    fig.update_layout(
        title=dict(
            text=f"Évolution de {param.capitalize()} Pendant {date1.strftime('%d/%m/%Y')} - {date2.strftime('%d/%m/%Y')}",
            font=dict(size=20),  # Taille du titre
            x=0.5,  # Centrer le titre
            xanchor="center"
        ),
        font=dict(size=14),  # Taille de la police pour le reste du graphique
        xaxis=dict(
            title=dict(text="Date", font=dict(size=16)),  # Titre de l'axe X
            tickangle=-45,  # Inclinaison des étiquettes de l'axe X pour une meilleure lisibilité
            # showgrid=True ,# Afficher une grille verticale
            showticklabels=False
        ),
        yaxis=dict(
            title=dict(text="Valeur", font=dict(size=16)),  # Titre de l'axe Y
            # showgrid=True  # Afficher une grille horizontale
        ),
        margin=dict(l=40, r=40, t=60, b=40),  # Marges autour du graphique
        height=500,  # Hauteur du graphique
    )
    st.plotly_chart(fig, use_container_width=True)

    # Analyse de la distribution
    st.markdown(
        "<h3 style='text-align: center; color: #4A90E2;'>Distribution des Paramètres</h3>", 
        unsafe_allow_html=True
    )

    fig_hist = px.histogram(
        df, 
        x=param, 
        title=f"Distribution de {param.capitalize()}",
        labels={param: param.capitalize()},
        nbins=20, 
        template="plotly_white"
    )
    fig_hist.update_layout(
        title_x=0.5,  # Centrer le titre du graphique
        height=500,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    # Statistiques descriptives
    if param:
        stats = df[param].describe()

        # Créer un DataFrame propre pour les statistiques descriptives
        stats_clean = pd.DataFrame({
            "Statistique": ["Moyenne", "Médiane", "Min", "Max", "Écart-type", "1er Quartile", "3e Quartile"],
            "Valeur": [
                round(stats["mean"], 2),
                round(stats["50%"], 2),
                round(stats["min"], 2),
                round(stats["max"], 2),
                round(stats["std"], 2),
                round(stats["25%"], 2),
                round(stats["75%"], 2),
            ]
        })

        # Affichage des statistiques descriptives
        st.markdown(
            f"<h3 style='text-align: center; color: #4A90E2;'>Statistiques Descriptives pour {param.capitalize()}</h3>",
            unsafe_allow_html=True
        )
        st.table(stats_clean)


consomation_energie(df, param)

st.markdown(
    """
    <div class="footer">
        © 2025 Station de Dessalement Wave 2 - Analyse Énergie
    </div>
    """, 
    unsafe_allow_html=True
)
