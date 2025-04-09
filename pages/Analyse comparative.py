import streamlit as st
import pandas as pd
from PIL import Image
import base64
from io import BytesIO
import plotly.express as px
import json
from datetime import datetime
import numpy as np
from fonctions import visualise,labo_oper


st.set_page_config(
    page_title="Exploration des Données des Phases- Station Wave 2",
    page_icon="📊",
    layout="wide"
)

st.title("Exploration des Données des Phases")
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

sheets1 = ["Self cleaning","Ultra filtration","Filtre à cartouche","RO-A","RO-B","RO-C","RO-D"]

data1 = {}

for sheet in sheets1:
    data1[sheet] = pd.read_excel('suivi 3h standart DIPS.xlsx', sheet_name=sheet)

# Barre latérale pour la sélection de la phase
st.sidebar.header("Options de Visualisation")
don1 = st.sidebar.selectbox("Suivi sur site", sheets1)
df1 = data1[don1]

param1 = st.sidebar.selectbox(
    'Paramètre 1', 
    df1.columns[2:],
    help=f"Choisissez un paramètre à afficher parmi les colonnes disponibles de {don1}."
)

sheets2 = ["SELF CLEANING", "UF", "RO-A", "RO-B", "RO-C", "RO-D"]
data2 = {}
for sheet in sheets2:
    data2[sheet] = pd.read_excel('SUIVI STANDART DIPS.xlsx', sheet_name=sheet)



don2 = st.sidebar.selectbox("Scada:", sheets2)
df2 = data2[don2]

df2.replace(['wbw','soak ceb1','w-f','f','F','w-bw','WBW','W.BW','W,BW','ceb1','CEB2','bw','wf','wb','W-F','W.F','hs','WF','wB','BW','w,b','W,F','W-BW','ceb2','SOAK CEB1','W,B','CEB1','SOAK CEB2','HS',
                ], 
               np.nan, inplace=True)
param2 = st.sidebar.selectbox(
    'Paramètre 2', 
    df2.columns[2:],
    help=f"Choisissez un paramètre à afficher parmi les colonnes disponibles de {don2}."
)


# Préparation des données
df2['date'] = pd.to_datetime(df2['date'])
df2['date'] = df2['date'].dt.strftime('%d/%m/%Y')  # Format 'dd/mm/yyyy'

# Définir les dates de début et de fin
startDate = pd.to_datetime(df2["date"], format='%d/%m/%Y').min()
endDate = pd.to_datetime(df2["date"], format='%d/%m/%Y').max()

# Sélection des dates dans la barre latérale
st.sidebar.subheader("Filtrer par période")
date1 = pd.to_datetime(st.sidebar.date_input("Date de début", startDate))
date2 = pd.to_datetime(st.sidebar.date_input("Date de fin", endDate))

# Filtrer les données par plage de dates
df2['date'] = pd.to_datetime(df2['date'], format='%d/%m/%Y')
df2 = df2[(df2["date"] >= date1) & (df2["date"] <= date2)]
df2['date'] = df2['date'].dt.strftime('%d/%m/%Y')  # Format pour affichage

# st.sidebar.markdown(
#     """
#     <h3 style="
#         color: #4A90E2; 
#         font-family: Arial, sans-serif; 
#         margin-bottom: 15px;
#     ">
#         Sélectionnez un paramètre
#     </h3>
#     """,
#     unsafe_allow_html=True
# )

# Sélection du paramètre à visualiser



# Style pour le titre de la phase
st.markdown(
    f"""
    <h2 style="
        text-align: center; 
        color: #4A90E2; 
        font-family: Arial, sans-serif; 
        margin-bottom: 10px;
    ">
        correlation entre {param1} de {don1}  et {param2} de {don2}
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
labo_oper(data1,data2,don1,don2,param1,param2)

