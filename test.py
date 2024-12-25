import streamlit as st
import pandas as pd
import plotly.express as px

# Titre de l'application
st.title("Suivi de performance - Station de dessalement")

# Charger les données des feuilles dans un dictionnaire
@st.cache_data
def load_excel_sheets(file_path):
    xls = pd.ExcelFile(file_path)
    return {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names[1:]}

file_path = "SUIVI DIPS (1).xlsx"
sheets_data = load_excel_sheets(file_path)

# Sélectionner une feuille
st.sidebar.header("Navigation")
sheet_name = st.sidebar.selectbox("Choisir une feuille :", list(sheets_data.keys()))

# Charger les données de la feuille sélectionnée
data = sheets_data[sheet_name]
st.subheader(f"Affichage des données - Feuille : {sheet_name}")
st.dataframe(data.head())

# Filtrage des colonnes
st.sidebar.header("Filtres")
columns = st.sidebar.multiselect("Choisir les colonnes :", data.columns, default=data.columns[:5])

if columns:
    filtered_data = data[columns]
    st.write("### Données filtrées")
    st.dataframe(filtered_data)

    # Visualisation interactive avec Plotly
    st.subheader("Visualisation des données (Graphique linéaire)")
    # x_axis = st.selectbox("Axe X :", filtered_data.columns, index=0)
    y_axis = st.selectbox("Axe Y :", filtered_data.columns, index=1)

    # Créer le graphique avec Plotly Express
    fig = px.line(filtered_data, x='date', y=y_axis, color='poste',title=f"Variation de   {y_axis}")
    st.plotly_chart(fig)

else:
    st.warning("Sélectionnez au moins une colonne à afficher.")

# Option d'export des données filtrées
st.sidebar.header("Export des données")
if st.sidebar.button("Exporter en CSV"):
    filtered_data.to_csv("filtered_data.csv", index=False)
    st.success("Données exportées en 'filtered_data.csv' avec succès !")
