# import streamlit as st
# import pandas as pd
# from PIL import Image
# import base64
# from io import BytesIO
# import plotly.express as px
# import json
# from datetime import datetime
# import numpy as np
# from fonctions import visualise, consomation,consomation_energie,anomali,load_data

# df = pd.read_excel('Consommation spécifique.xlsx',sheet_name='Energie')
# # Ajouter des KPI
# col1, col2, col3 = st.columns(3)

# with col1:
#     st.metric("Consommation Moyenne (kWh)", f"{np.around(df['Consommation KWh'].mean(), 2)}")

# with col2:
#     st.metric("Production Moyenne (kWh)", f"{np.around(df['Prod'].mean(), 2)}")

# with col3:
#     st.metric("Énergie Spécifique Moyenne", f"{np.around(df['Energie spécifique'].mean(), 2)}")

# param = st.selectbox(f'Paramètre', df.columns[1:]) 

# consomation_energie(df,param)
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

# CSS pour améliorer le design et ajouter des animations
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

# Titre principal
st.markdown("<h2 style='text-align: center;'>Analyse Énergie</h2>", unsafe_allow_html=True)

# Section des KPI
st.markdown("<h3 style='text-align: center;'>Indicateurs Clés</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        f"""
        <div class="kpi-box">
            <h3>Consommation Moyenne (kWh)</h3>
            <p>{np.around(df['Consommation KWh'].mean(), 2)}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="kpi-box">
            <h3>Production Moyenne (kWh)</h3>
            <p>{np.around(df['Prod'].mean(), 2)}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="kpi-box">
            <h3>Énergie Spécifique Moyenne</h3>
            <p>{np.around(df['Energie spécifique'].mean(), 2)}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Sélection du paramètre pour l'analyse
param = st.selectbox(f"Paramètre à visualiser", df.columns[1:])

# Visualisation des données
def consomation_energie(df, param):
    st.markdown(f"<h2 style='text-align: center;'>Visualisation : {param}</h2>", unsafe_allow_html=True)
    
    # Graphique de la tendance
    fig = px.line(df, x="Date", y=param, title=f"Tendance de {param}")
    st.plotly_chart(fig, use_container_width=True)
    
    # Analyse de la distribution
    st.markdown("<h3>Distribution des paramètres</h3>", unsafe_allow_html=True)
    param_to_analyze = st.selectbox("Sélectionnez un paramètre pour analyser sa distribution", df.columns[1:])
    fig_hist = px.histogram(df, x=param_to_analyze, title=f"Distribution de {param_to_analyze}", nbins=20)
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

        # Afficher un tableau propre
        st.write(f"**Statistiques descriptives pour {param}**")
        st.table(stats_clean)

# Appel de la fonction
consomation_energie(df, param)

# Footer
st.markdown(
    """
    <div class="footer">
        © 2025 Station de Dessalement Wave 2 - Analyse Énergie
    </div>
    """, 
    unsafe_allow_html=True
)
