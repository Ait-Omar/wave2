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

# df = pd.read_excel('Consommation spécifique.xlsx',sheet_name='PC')
# param = st.selectbox(f'Paramètre', df.columns[1:]) 
    
# consomation(df,param)
import streamlit as st
import pandas as pd
from PIL import Image
import base64
from io import BytesIO
import plotly.express as px
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Consommation Spécifique - Analyse",
    page_icon="📊",
    layout="wide"
)

# CSS pour le style et les animations
st.markdown(
    """
    <style>
        body {
            background-color: #f7f9fc;
        }
        h1, h2, h3 {
            font-family: 'Arial', sans-serif;
            color: #2c3e50;
            animation: fadeIn 2s ease-in-out;
        }
        .footer {
            font-size: 14px;
            color: #7f8c8d;
            text-align: center;
            padding-top: 40px;
            padding-bottom: 20px;
        }
        .description {
            font-size: 18px;
            line-height: 1.6;
            color: #2c3e50;
            margin-bottom: 30px;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes slideIn {
            from { transform: translateX(-50px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        .stSelectbox {
            font-size: 16px;
            color: #34495e;
            padding: 10px;
            border-radius: 8px;
            animation: slideIn 1s ease-in-out;
        }
        .stPlotlyChart {
            animation: fadeIn 2s ease-in-out;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Titre principal
st.markdown(
    "<h1 style='text-align: center;'>Consommation Spécifique - Analyse</h1>", 
    unsafe_allow_html=True
)

# Charger les données
df = pd.read_excel('Consommation spécifique.xlsx', sheet_name='PC')

# Sélection du paramètre
st.markdown("<h2 style='text-align: center;'>Sélectionnez un paramètre :</h2>", unsafe_allow_html=True)
param = st.selectbox(f'Paramètre', df.columns[1:])

# Fonction de consommation
def consomation(df, param):
    # Calcul de la moyenne
    moyenne = np.around(df[param].mean(), 2)
    st.markdown(
        f"<h2 style='text-align: center;'>{param[:-5]} moyen : {moyenne}</h2>", 
        unsafe_allow_html=True
    )

    # Graphique interactif avec Plotly
    fig = px.line(
        df,
        x="date",
        y=param,
        title=f"Évolution de {param} au cours du temps",
        labels={"date": "Date", param: "Consommation"},
        template="plotly_white"
    )
    fig.update_layout(
        title_x=0.5,  # Centrer le titre
        font=dict(size=14),
        xaxis=dict(title="Date"),
        yaxis=dict(title="Valeur"),
    )
    st.plotly_chart(fig, use_container_width=True)

# Appel de la fonction avec le paramètre sélectionné
if param:
    consomation(df, param)

# Footer
st.markdown(
    """
    <div class="footer">
        © 2025 Analyse de la Consommation Spécifique | Interface développée par DIPS
    </div>
    """,
    unsafe_allow_html=True
)
