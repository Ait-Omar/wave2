
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
st.markdown(
    """
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;600&display=swap" rel="stylesheet">
    </head>
    """,
    unsafe_allow_html=True
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
    "<h1 style='text-align: center;font-family:Jost;'>Consommation Spécifique - Analyse</h1>", 
    unsafe_allow_html=True
)

c=st.sidebar.selectbox(f'Type de Consommation:', ['Consommation spécifique','Consommation Journalière'])
# Charger les données
if c=='Consommation spécifique':
    df = pd.read_excel('Consommation spécifique.xlsx', sheet_name='CS Produits chimiques')
elif c=='Consommation Journalière':
    df = pd.read_excel('Consommation spécifique.xlsx', sheet_name='C Prouits chimiques')
# Préparation des données
# df['date'] = pd.to_datetime(df['date'])
# df['date'] = df['date'].dt.strftime('%d/%m/%Y')  # Format 'dd/mm/yyyy'

# # Définir les dates de début et de fin
# startDate = pd.to_datetime(df["date"], format='%d/%m/%Y').min()
# endDate = pd.to_datetime(df["date"], format='%d/%m/%Y').max()

# # Sélection des dates dans la barre latérale
# st.sidebar.subheader("Filtrer par période")
# date1 = pd.to_datetime(st.sidebar.date_input("Date de début", startDate))
# date2 = pd.to_datetime(st.sidebar.date_input("Date de fin", endDate))

# # Filtrer les données par plage de dates
# df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
# df = df[(df["date"] >= date1) & (df["date"] <= date2)]
# df['date'] = df['date'].dt.strftime('%d/%m/%Y')  # Format pour affichage
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Define the start and end dates for filtering
startDate = df['date'].min()
endDate = df['date'].max()

# Sidebar for date range selection
st.sidebar.subheader("Filtrer par période")
date1 = pd.to_datetime(st.sidebar.date_input("Date de début", startDate))
date2 = pd.to_datetime(st.sidebar.date_input("Date de fin", endDate))

# Filter the data by date range
df = df[(df["date"] >= date1) & (df["date"] <= date2)]

# Sélection du paramètre
st.sidebar.markdown("<h2 style='text-align: center;'>Sélectionnez un paramètre :</h2>", unsafe_allow_html=True)
param = st.sidebar.selectbox(f'Paramètre', df.columns[1:])

# Fonction de consommation
def consomation(df, param):
    
    # Titre des indicateurs
    st.markdown(
        f"<h3 style='text-align: center; color: #4A90E2;'>{param}</h3>", 
        unsafe_allow_html=True
    )


    # Style CSS intégré pour les boîtes KPI
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
        </style>
        """, 
        unsafe_allow_html=True
    )


    st.markdown(
        f"""
        <div class="kpi-box">
            <h2 style="
            text-align: center; 
            color: #4A90E2; 
            font-family: Jost; 
            margin-bottom: 0;">
            Consommation journalière : {np.around(df[param].iloc[-1],3)}
            </h2>
        </div>
        """, 
        unsafe_allow_html=True
    )

    fig = px.line(
        df,
        x="date",
        y=param,
        title=f"Évolution de {param.capitalize()} pendant  {date1.strftime('%d/%m/%Y')} - {date2.strftime('%d/%m/%Y')}",
        labels={"date": "Date", param: param.capitalize()},
        template="plotly_white"
    )

    # Mise en forme avancée du graphique
    
    fig.update_layout(
        title=dict(
            text=f"Évolution de {param.capitalize()} Pendant {date1.strftime('%d/%m/%Y')} - {date2.strftime('%d/%m/%Y')}",
            font=dict(size=15, weight='bold',family='Jost'),
            x=0.5, 
            xanchor="center"
        ),
        font=dict(size=14),
        xaxis=dict(
            title=dict(text="Date", font=dict(size=16, weight='bold')),
            tickangle=-0,
            showticklabels=True,
            tickformat="%d",  # Display date in 'dd/mm/yyyy' format
            tickfont=dict(size=20, color='black',family='Jost', weight='bold')
        ),
        yaxis=dict(
            title=dict(text="Valeur", font=dict(size=16, weight='bold')),
            tickfont=dict(size=20, weight='bold')
        ),
        margin=dict(l=40, r=40, t=60, b=40),
        height=500
    )


    # Tracé plus épais pour la ligne
    fig.update_traces(
        line=dict(width=2),  # Épaisseur de la ligne
        marker=dict(size=6)  # Taille des marqueurs (s'il y en a)
    )

    # Affichage du graphique dans Streamlit
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
