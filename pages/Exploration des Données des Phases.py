import streamlit as st
import pandas as pd
from PIL import Image
import base64
from io import BytesIO
import plotly.express as px
import json
from datetime import datetime
import numpy as np
from fonctions import visualise


st.set_page_config(
    page_title="Exploration des Données des Phases- Station Wave 2",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Exploration des Données des Phases")
st.markdown(
    """
    <div style="
        text-align: justify; 
        color: #333333; 
        font-family: Arial, sans-serif; 
        line-height: 1.6; 
        border-left: 4px solid #4A90E2; 
        padding-left: 10px;
        margin-bottom: 20px;
    ">
        <strong>Explorez les données de performance</strong> des différentes phases de traitement de la station de dessalement <strong>Wave 2</strong>. 
        Sélectionnez une phase, définissez une période et visualisez les paramètres clés pour mieux comprendre et analyser le processus.
    </div>
    """,
    unsafe_allow_html=True
)

# Chargement des données
sheets = ["SELF CLEANING", "UF", "RO-A", "RO-B", "RO-C", "RO-D", "PRODUCTION"]
data = {}
for sheet in sheets:
    data[sheet] = pd.read_excel('SUIVI DIPS (1).xlsx', sheet_name=sheet)

# Barre latérale pour la sélection de la phase
st.sidebar.header("Options de Visualisation")
don = st.sidebar.radio("Phases de traitement :", sheets)

# Charger la feuille sélectionnée
df = data[don]

# Préparation des données
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

st.sidebar.markdown(
    """
    <h3 style="
        color: #4A90E2; 
        font-family: Arial, sans-serif; 
        margin-bottom: 15px;
    ">
        Sélectionnez un paramètre
    </h3>
    """,
    unsafe_allow_html=True
)

# Sélection du paramètre à visualiser
param = st.sidebar.selectbox(
    'Paramètre', 
    df.columns[2:],
    help="Choisissez un paramètre à afficher parmi les colonnes disponibles."
)

# Style pour le titre de la phase
st.markdown(
    f"""
    <h2 style="
        text-align: center; 
        color: #4A90E2; 
        font-family: Arial, sans-serif; 
        margin-bottom: 10px;
    ">
        Phase de traitement : {don}
    </h2>
    """,
    unsafe_allow_html=True
)

# Période formatée avec un style professionnel
st.markdown(
    f"""
    <h4 style="
        text-align: center; 
        color: #333333; 
        font-family: Arial, sans-serif; 
        margin-top: 5px;
    ">
        Période : {date1.strftime('%d/%m/%Y')} - {date2.strftime('%d/%m/%Y')}
    </h4>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <h3 style="
        text-align: center; 
        color: #4A90E2; 
        font-family: Arial, sans-serif; 
        margin-bottom: 20px;
    ">
        Visualisation de {param.capitalize()}
    </h3>
    """,
    unsafe_allow_html=True
)

visualise(df, param)
