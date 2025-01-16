import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def load_data(file):
    try:
        data = pd.read_excel(file)
        return data
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier : {e}")
        return None

def preprocess_data(non_realisee, realisee):
    non_realisee = non_realisee.rename(columns=non_realisee.iloc[0]).drop(non_realisee.index[0])
    realisee = realisee.rename(columns=realisee.iloc[0]).drop(realisee.index[0])

    anomalies_non_realisees = non_realisee[['Anomalies', 'Emplacement', 'Type', 'Responsable', 'Date']].dropna()
    anomalies_realisees = realisee[['Anomalies', 'Emplacement', 'Type', 'Responsable', 'Date']].dropna()

    return anomalies_non_realisees, anomalies_realisees

def calculate_statistics(non_realisee, realisee):
    stats = {
        "Total Non Réalisées": len(non_realisee),
        "Total Réalisées": len(realisee),
        "Taux de Réalisation": (len(realisee) / len(non_realisee) * 100) if len(non_realisee) > 0 else 0
    }
    return stats

def visualize_statistics(stats):
    st.subheader("Statistiques des Anomalies")

    # Afficher les statistiques principales
    for key, value in stats.items():
        st.markdown(f"- **{key} :** {value}")

    # Visualisation avec Plotly
    fig = px.bar(
        x=['Non réalisées', 'Réalisées'], 
        y=[stats["Total Non Réalisées"], stats["Total Réalisées"]],
        labels={'x': 'Catégorie', 'y': 'Nombre danomalies'},
        title="Répartition des Anomalies",
        color=['Non réalisées', 'Réalisées']
    )
    st.plotly_chart(fig)

def analyze_realisation_dates(realisee):
    st.subheader("Analyse des Dates de Réalisation")

    # Conversion des dates
    realisee['Date'] = pd.to_datetime(realisee['Date'], errors='coerce')

    # Distribution des réalisations dans le temps
    time_trend = realisee.groupby(realisee['Date'].dt.to_period('M')).size().reset_index(name='count')
    time_trend['Date'] = time_trend['Date'].dt.to_timestamp()

    fig = px.line(
        time_trend, 
        x='Date', 
        y='count', 
        title="Tendance des Réalisations dans le Temps",
        labels={'count': 'Nombre danomalies réalisées', 'Date': 'Mois'}
    )
    st.plotly_chart(fig)

def analyze_types(non_realisee, realisee):
    st.subheader("Analyse des Types d'Anomalies")

    # Répartition par type avec Plotly
    type_counts_non_realisee = non_realisee['Type'].value_counts().reset_index()
    type_counts_non_realisee.columns = ['Type', 'Non réalisées']

    type_counts_realisee = realisee['Type'].value_counts().reset_index()
    type_counts_realisee.columns = ['Type', 'Réalisées']

    merged_counts = pd.merge(type_counts_non_realisee, type_counts_realisee, on='Type', how='outer').fillna(0)

    fig = px.bar(
        merged_counts.melt(id_vars='Type', value_vars=['Non réalisées', 'Réalisées']), 
        x='Type', 
        y='value', 
        color='variable',
        title="Répartition des Types d'Anomalies",
        labels={'value': 'Nombre danomalies', 'variable': 'Catégorie'}
    )
    st.plotly_chart(fig)

def analyze_emplacement(non_realisee, realisee):
    st.subheader("Répartition par Emplacement")

    # Répartition par emplacement avec Plotly
    emplacement_counts_non_realisee = non_realisee['Emplacement'].value_counts().reset_index()
    emplacement_counts_non_realisee.columns = ['Emplacement', 'Non réalisées']

    emplacement_counts_realisee = realisee['Emplacement'].value_counts().reset_index()
    emplacement_counts_realisee.columns = ['Emplacement', 'Réalisées']

    merged_emplacements = pd.merge(emplacement_counts_non_realisee, emplacement_counts_realisee, on='Emplacement', how='outer').fillna(0)

    fig = px.bar(
        merged_emplacements.melt(id_vars='Emplacement', value_vars=['Non réalisées', 'Réalisées']), 
        x='Emplacement', 
        y='value', 
        color='variable',
        title="Répartition des Anomalies par Emplacement",
        labels={'value': 'Nombre danomalies', 'variable': 'Catégorie'}
    )
    st.plotly_chart(fig)

def main():
    st.set_page_config(page_title="Analyse des Anomalies", layout="wide")

    st.title("Analyse Complète des Anomalies")

    st.markdown(
        """Cette application offre une analyse approfondie des anomalies non réalisées et réalisées. 
        Elle fournit des statistiques, des tendances et des insights pour aider l'équipe industrielle à prioriser les actions."""
    )

    # Chargement des fichiers
    uploaded_non_realisee = st.file_uploader("Uploader le fichier des anomalies non réalisées", type=['xlsx'])
    uploaded_realisee = st.file_uploader("Uploader le fichier des anomalies réalisées", type=['xlsx'])

    if uploaded_non_realisee and uploaded_realisee:
        non_realisee = load_data(uploaded_non_realisee)
        realisee = load_data(uploaded_realisee)

        if non_realisee is not None and realisee is not None:
            anomalies_non_realisees, anomalies_realisees = preprocess_data(non_realisee, realisee)

            # Calculer les statistiques
            stats = calculate_statistics(anomalies_non_realisees, anomalies_realisees)

            # Afficher les tableaux
            st.subheader("Tableaux des Anomalies")
            st.markdown("### Anomalies Non Réalisées")
            st.dataframe(anomalies_non_realisees)

            st.markdown("### Anomalies Réalisées")
            st.dataframe(anomalies_realisees)

            # Visualiser les statistiques
            visualize_statistics(stats)

            # Analyse des types
            analyze_types(anomalies_non_realisees, anomalies_realisees)

            # Analyse des emplacements
            analyze_emplacement(anomalies_non_realisees, anomalies_realisees)

            # Tendance dans le temps
            analyze_realisation_dates(anomalies_realisees)

    st.markdown("---")
    st.markdown("**Streamlit Application** - Analyse des anomalies pour l'équipe industrielle.")

if __name__ == "__main__":
    main()
