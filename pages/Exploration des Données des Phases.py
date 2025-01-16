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
st.write(
    """
    Explorez les données de performance des différentes phases de traitement de la station de dessalement Wave 2.
    Sélectionnez une phase, définissez une période et visualisez les paramètres clés.
    """
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

# Sélection du paramètre à visualiser
st.sidebar.subheader("Sélectionnez un paramètre")
param = st.sidebar.selectbox(f'Paramètre', df.columns[2:])

# Titre de la phase
st.subheader(f"Phase de traitement : {don}")
st.write(f"### Période : {date1.strftime('%d/%m/%Y')} - {date2.strftime('%d/%m/%Y')}")

# Affichage des données filtrées
st.write("### Données Filtrées")
st.dataframe(df)

# Appel de la fonction de visualisation
st.write(f"### Visualisation de {param}")
visualise(df, param, don)
# sheets =["SELF CLEANING","UF","RO-A","RO-B","RO-C","RO-D","PRODUCTION"]
# data = {}
# for sheet in sheets:
#         data[sheet] = pd.read_excel('SUIVI DIPS (1).xlsx',sheet_name=sheet)
# don = st.sidebar.radio('Phases de traitement:',
#                                 [
#                                     "SELF CLEANING",
#                                     "UF",
#                                     "RO-A",
#                                     "RO-B",
#                                     "RO-C",
#                                     "RO-D",
#                                     "PRODUCTION"
#                                     ])  
# df = pd.read_excel('SUIVI DIPS (1).xlsx',sheet_name=don)

# df['date'] = pd.to_datetime(df['date'])
# df['date'] = df['date'].dt.strftime('%d/%m/%Y')  # Format to 'dd/mm/yyyy'

# # Start and end dates for filtering (convert back to datetime)
# startDate = pd.to_datetime(df["date"], format='%d/%m/%Y').min()
# endDate = pd.to_datetime(df["date"], format='%d/%m/%Y').max()

# col1, col2 = st.columns((2))
# with col1:
#     date1 = pd.to_datetime(st.date_input("Start Date", startDate))
# with col2:
#     date2 = pd.to_datetime(st.date_input("End Date", endDate))

# # Convert back to datetime for filtering
# df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
# df = df[(df["date"] >= date1) & (df["date"] <= date2)]

# # Convert back to formatted string for display
# df['date'] = df['date'].dt.strftime('%d/%m/%Y')


# param = st.selectbox(f'Paramètre', df.columns[2:]) 
# visualise(df,param,don)