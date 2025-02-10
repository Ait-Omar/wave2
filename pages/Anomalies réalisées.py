
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from PIL import Image
from io import BytesIO
import base64

# Configuration de la page
st.set_page_config(
    page_title="Suivi des Anomalies - Station Wave 2",
    page_icon="⚠️",
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
            animation: fadeIn 1.5s ease-in-out;
        }
        .metric-container {
            display: flex;
            justify-content: space-around;
            margin: 20px 0;
        }
        .stMetric {
            text-align: center;
        }
        .form-container {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Titre principal
st.markdown("<h1 style='text-align: center;'>Suivi des Anomalies Journalières</h1>", unsafe_allow_html=True)

# Fonction pour charger les données
def load_data(file_path):
    return pd.read_excel(file_path)

# Charger les données
data_file = 'Réalisée (2).xlsx'
data = load_data(data_file)

# Options de filtrage
st.subheader("Filtrer les Anomalies")
lieux = data['Emplacement'].unique()
statut = data['Statut '].unique()
types = data['Type'].unique()

col1, col2, col3 = st.columns(3)
with col1:
    lieu_filtre = st.selectbox("Filtrer par lieu :", ["Tous"] + list(lieux))
with col2:
    statut_options = st.selectbox("Filtrer par statut :", ["Tous"] + list(statut))
with col3:
    type_filtre = st.selectbox("Filtrer par type :", ["Tous"] + list(types))

# Filtrage des données
filtered_data = data.copy()
if lieu_filtre != "Tous":
    filtered_data = filtered_data[filtered_data["Emplacement"] == lieu_filtre]
if statut_options != "Tous":
    filtered_data = filtered_data[filtered_data["Statut "] == statut_options]
if type_filtre != "Tous":
    filtered_data = filtered_data[filtered_data["Type"] == type_filtre]

# Afficher les données filtrées
st.write(f"### Nombre d'anomalies après filtrage : {len(filtered_data)}")
st.dataframe(filtered_data)

# Résumé dynamique
st.subheader("Résumé Dynamique des Anomalies")
col1, col2, col3 = st.columns(3)
total_anomalies = len(filtered_data)
resolved_anomalies = len(filtered_data[filtered_data['Statut '] == "Réalisée"])
resolved_percentage = (resolved_anomalies / total_anomalies * 100) if total_anomalies > 0 else 0

with col1:
    st.metric(label="Total Anomalies", value=total_anomalies)
with col2:
    st.metric(label="Résolues", value=resolved_anomalies)
with col3:
    st.metric(label="Pourcentage Résolu", value=f"{resolved_percentage:.1f}%")

# Graphique : Répartition des anomalies par statut
st.subheader("Analyse des Anomalies par Statut")
if not filtered_data.empty:
    statut_counts = filtered_data['Statut '].value_counts()
    st.bar_chart(statut_counts)
else:
    st.info("Aucune donnée disponible pour les filtres actuels.")

# Graphique circulaire : Répartition des anomalies par type
st.subheader("Répartition des Anomalies par Type")
if not filtered_data.empty:
    type_counts = filtered_data['Type'].value_counts().reset_index()
    type_counts.columns = ['Type', 'Nombre']
    fig = px.pie(type_counts, names='Type', values='Nombre', title='Répartition des Anomalies par Type')
    fig.update_traces(textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Aucune donnée disponible pour les filtres actuels.")

# Ajouter une nouvelle anomalie
st.subheader("Ajouter une Nouvelle Anomalie Réaliseé")
with st.form("nouvelle_anomalie"):
    anomalie = st.text_input("Anomalie")
    emplacement = st.text_input("Emplacement")
    cause = st.text_input("Cause")
    consequence = st.text_area("Conséquence")
    action = st.text_area("Action prise")
    type_anomalie = st.text_input("Type")
    responsable = st.text_input("Responsable")
    date_realisation = st.date_input("Date de réalisation")
    statut = st.selectbox("Statut", options=["Non réalisée", "En cours", "Réalisée"])
    commentaire = st.text_area("Commentaire")
    submitted = st.form_submit_button("Soumettre")

    if submitted:
        st.success("Nouvelle anomalie ajoutée avec succès !")

# Footer
st.markdown("<div style='text-align: center; color: #7f8c8d;'>© 2025 Station Wave 2 - Jorf Lasfar | Interface développée par DIPS</div>", unsafe_allow_html=True)


