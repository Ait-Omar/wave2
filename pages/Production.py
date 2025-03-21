import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from datetime import datetime
from fonctions import visualise

# Configuration de la page
st.set_page_config(
    page_title="Production Wave 2",
    page_icon="📊",
    layout="wide"
)

# Titre et description
st.title("📊 Production - Station Wave 2")
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
        Cette section vous permet d'analyser la production de la station de dessalement <strong>Wave 2</strong>.
        Sélectionnez une période, choisissez un train de production et visualisez les performances pour une 
        meilleure gestion et optimisation du processus de dessalement.
    </div>
    """,
    unsafe_allow_html=True
)

# Chargement des données
try:
    df = pd.read_excel('PRODUCTION 2025.xlsx', sheet_name="Production")
except FileNotFoundError:
    st.error("Le fichier de production n'a pas été trouvé. Veuillez vérifier son emplacement.")
    st.stop()

# Préparation des données
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df.dropna(subset=['date'], inplace=True)
df['date'] = df['date'].dt.strftime('%d/%m/%Y')  # Format 'dd/mm/yyyy'

# Définition des dates minimales et maximales
startDate = pd.to_datetime(df["date"], format='%d/%m/%Y').min()
endDate = pd.to_datetime(df["date"], format='%d/%m/%Y').max()

# Barre latérale de sélection
st.sidebar.header("🔍 Options de Filtrage")
st.sidebar.subheader("📅 Filtrer par période")
date1 = pd.to_datetime(st.sidebar.date_input("Date de début", startDate))
date2 = pd.to_datetime(st.sidebar.date_input("Date de fin", endDate))

# Filtrage des données par plage de dates
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
df = df[(df["date"] >= date1) & (df["date"] <= date2)]
df['date'] = df['date'].dt.strftime('%d/%m/%Y')

# Sélection du paramètre à visualiser
st.sidebar.subheader("🚄 Sélection du Train de Production")
if len(df.columns) > 2:
    param = st.sidebar.selectbox("Choisissez un train :", df.columns[2:])
else:
    st.error("Aucune donnée de production disponible pour cette période.")
    st.stop()

# Affichage des informations sélectionnées
st.markdown(
    f"""
    <h2 style="
        text-align: center; 
        color: #4A90E2; 
        font-family: Arial, sans-serif; 
        margin-bottom: 10px;
    ">
        Train : {param[-1]}
    </h2>
    """,
    unsafe_allow_html=True
)

df.replace(['wbw','soak ceb1','w-f','f','F','w-bw','WBW','W.BW','W,BW','ceb1','CEB2','bw','wf','wb','W-F','W.F','hs','WF','wB','BW','w,b','W,F','W-BW','ceb2','SOAK CEB1','W,B','CEB1','SOAK CEB2','HS',
                ], 
               np.nan, inplace=True)
col1,col2,col3 = st.columns((3))
with col1:
    st.markdown(
    f"""
    <div style="
        background-color: #F9F9F9; 
        border: 1px solid #D1D1D1; 
        border-radius: 8px; 
        padding: 20px; 
        margin: 0 auto 20px auto; 
        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1); 
        width: 100%; /* Ajustez ce pourcentage selon vos besoins */
        max-width: 800px; /* Largeur maximale pour éviter une trop grande expansion */
    ">
        <h2 style="
            text-align: center; 
            color: #4A90E2; 
            font-family: Arial, sans-serif; 
            margin-bottom: 0;
        ">
            Production journalière : {df[param].iloc[-1]} m³
        </h2>
    </div>
    """, 
    unsafe_allow_html=True
)
    with col2:
        st.markdown(
    f"""
    <div style="
        background-color: #F9F9F9; 
        border: 1px solid #D1D1D1; 
        border-radius: 8px; 
        padding: 20px; 
        margin: 0 auto 20px auto; 
        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1); 
        width: 100%; /* Ajustez ce pourcentage selon vos besoins */
        max-width: 800px; /* Largeur maximale pour éviter une trop grande expansion */
    ">
        <h2 style="
            text-align: center; 
            color: #4A90E2; 
            font-family: Arial, sans-serif; 
            margin-bottom: 0;
        ">
            Production Prévue : 15000 m³
        </h2>
    </div>
    """, 
    unsafe_allow_html=True
)
    with col3:
        st.markdown(
    f"""
    <div style="
        background-color: #F9F9F9; 
        border: 1px solid #D1D1D1; 
        border-radius: 8px; 
        padding: 20px; 
        margin: 0 auto 20px auto; 
        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1); 
        width: 100%; /* Ajustez ce pourcentage selon vos besoins */
        max-width: 800px; /* Largeur maximale pour éviter une trop grande expansion */
    ">
        <h2 style="
            text-align: center; 
            color: #4A90E2; 
            font-family: Arial, sans-serif; 
            margin-bottom: 0;
        ">
            Taux de production : {np.round(df[param].iloc[-1]/15000*100,2)} %
        </h2>
    </div>
    """, 
    unsafe_allow_html=True
)

# Personnalisation du graphique avec un style moderne
fig = px.line(
    df,
    x="date",
    y=param,
    title=f"Évolution de {param.capitalize()} au fil du temps",
    labels={
        "dete": "date",
        param: param.capitalize()
    },
    template="plotly_white",  # Thème moderne
)

# Options pour améliorer le design
fig.update_traces(line=dict(width=3))  # Épaisseur des lignes
fig.update_layout(
    title=dict(
        text=f"Évolution de la Production pendant {date1.strftime('%d/%m/%Y')} - {date2.strftime('%d/%m/%Y')}",
        font=dict(size=20),
        x=0.5,
        xanchor="center"
    ),
    xaxis=dict(
        title_text="",
        tickangle=-45,
        showticklabels=False  # Hide the date labels on the x-axis
    ),
    yaxis=dict(title_text=f"{param.capitalize()}"),
    margin=dict(l=50, r=50, t=60, b=40),
    height=400,
)


# Affichage du graphique
st.plotly_chart(fig, use_container_width=True)
