import streamlit as st
import pandas as pd
from PIL import Image
import base64
from io import BytesIO
import plotly.express as px
import json
from datetime import datetime
import numpy as np
from fonctions import laboratoir,transform_laboratory_data


st.set_page_config(
    page_title="Suivi laboratoire - Station Wave 2",
    page_icon="📊",
    layout="wide"
)

st.title("Analyse laboratoire")
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
sheets_labo = ["UF feed","PERMEAT UF","AVANT FC sud","AVANT FC nord","cf outlet",
          "PERMEAT RO-A","PERMEAT RO-B","PERMEAT RO-C","PERMEAT RO-D",
          "PERMEAT RO-E","PERMEAT RO-F","PERMEAT RO-G","PERMEAT RO-H"]
data_labo = {}
for sheet in sheets_labo:
    data_labo[sheet] = pd.read_excel('suivi qualité.xlsx', sheet_name=sheet)

sheets_scada = ["SELF CLEANING", "UF", "RO-A", "RO-B", "RO-C", "RO-D"]
data_scada = {}
for sheet in sheets_scada:
    data_scada[sheet] = pd.read_excel('SUIVI STANDART DIPS.xlsx', sheet_name=sheet)

sheets_chantier = ["Self cleaning", "Ultra filtration", "Filtre à cartouche", "RO-A", "RO-B", "RO-C","RO-D"]
data_chantier = {}
for sheet in sheets_chantier:
    data_chantier[sheet] = pd.read_excel('suivi 3h standart DIPS.xlsx', sheet_name=sheet)

option = st.sidebar.multiselect("Options",['Laboratoir','Scada','Chantier'])


if option == ['Laboratoir']:
    # Barre latérale pour la sélection de la phase
    st.sidebar.header("Options de Visualisation")
    don = st.sidebar.radio("Phases de traitement :", sheets_labo)
    df_labo = transform_laboratory_data('suivi qualité.xlsx', sheet_name=don)
    # Charger la feuille sélectionnée
    # df_labo = data_labo[don]

    # Préparation des données
    df_labo['date'] = pd.to_datetime(df_labo['date'])
    df_labo['date'] = df_labo['date'].dt.strftime('%d/%m/%Y')  # Format 'dd/mm/yyyy'

    # Définir les dates de début et de fin
    startDate = pd.to_datetime(df_labo["date"], format='%d/%m/%Y').min()
    endDate = pd.to_datetime(df_labo["date"], format='%d/%m/%Y').max()

    # Sélection des dates dans la barre latérale
    st.sidebar.subheader("Filtrer par période")
    date1 = pd.to_datetime(st.sidebar.date_input("Date de début", startDate))
    date2 = pd.to_datetime(st.sidebar.date_input("Date de fin", endDate))

    # Filtrer les données par plage de dates
    df_labo['date'] = pd.to_datetime(df_labo['date'], format='%d/%m/%Y')
    df_labo = df_labo[(df_labo["date"] >= date1) & (df_labo["date"] <= date2)]
    df_labo['date'] = df_labo['date'].dt.strftime('%d/%m/%Y')  # Format pour affichage

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
        [col for col in df_labo.columns if col not in ['date', 'point', 'poste', 'source']],
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

    laboratoir(df_labo, param,don)
elif option == ['Scada']:
    # Barre latérale pour la sélection de la phase
    st.sidebar.header("Options de Visualisation")
    don = st.sidebar.radio("Phases de traitement :", sheets_scada)
    df_labo =  pd.read_excel('SUIVI STANDART DIPS.xlsx', sheet_name=don)
    # Charger la feuille sélectionnée
    # df_labo = data_labo[don]

    # Préparation des données
    df_labo['date'] = pd.to_datetime(df_labo['date'])
    df_labo['date'] = df_labo['date'].dt.strftime('%d/%m/%Y')  # Format 'dd/mm/yyyy'

    # Définir les dates de début et de fin
    startDate = pd.to_datetime(df_labo["date"], format='%d/%m/%Y').min()
    endDate = pd.to_datetime(df_labo["date"], format='%d/%m/%Y').max()

    # Sélection des dates dans la barre latérale
    st.sidebar.subheader("Filtrer par période")
    date1 = pd.to_datetime(st.sidebar.date_input("Date de début", startDate))
    date2 = pd.to_datetime(st.sidebar.date_input("Date de fin", endDate))

    # Filtrer les données par plage de dates
    df_labo['date'] = pd.to_datetime(df_labo['date'], format='%d/%m/%Y')
    df_labo = df_labo[(df_labo["date"] >= date1) & (df_labo["date"] <= date2)]
    df_labo['date'] = df_labo['date'].dt.strftime('%d/%m/%Y')  # Format pour affichage

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
         [col for col in df_labo.columns if col not in ['date', 'poste']] ,
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

    laboratoir(df_labo, param,don)
elif option == ['Chantier']:
  # Barre latérale pour la sélection de la phase
    st.sidebar.header("Options de Visualisation")
    don = st.sidebar.radio("Phases de traitement :", sheets_chantier)
    df_labo =  pd.read_excel('suivi 3h standart DIPS.xlsx', sheet_name=don)
    print(df_labo.columns)

    df_labo['date'] = df_labo['date'].astype(str) + " " + df_labo['Heur'].astype(str)
    df_labo['date'] = pd.to_datetime(df_labo['date'])
    df_labo['date'] = df_labo['date'].dt.strftime('%d/%m/%Y')  # Format 'dd/mm/yyyy'
    


    # startDate = pd.to_datetime(df_labo["date"], format='%d/%m/%Y').min()
    # endDate = pd.to_datetime(df_labo["date"], format='%d/%m/%Y').max()


    # st.sidebar.subheader("Filtrer par période")
    # date1 = pd.to_datetime(st.sidebar.date_input("Date de début", startDate))
    # date2 = pd.to_datetime(st.sidebar.date_input("Date de fin", endDate))

    # df_labo['date'] = pd.to_datetime(df_labo['date'], format='%d/%m/%Y')
    # df_labo = df_labo[(df_labo["date"] >= date1) & (df_labo["date"] <= date2)]
    # df_labo['date'] = df_labo['date'].dt.strftime('%d/%m/%Y')  # Format pour affichage
 
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

    # # Sélection du paramètre à visualiser
    # param = st.sidebar.selectbox(
    #     'Paramètre', 
    #      [col for col in df_labo.columns if col not in ['date', 'Heur']] ,
    #     help="Choisissez un paramètre à afficher parmi les colonnes disponibles."
    # )

    # # Style pour le titre de la phase
    # st.markdown(
    #     f"""
    #     <h2 style="
    #         text-align: center; 
    #         color: #4A90E2; 
    #         font-family: Arial, sans-serif; 
    #         margin-bottom: 10px;
    #     ">
    #         Phase de traitement : {don}
    #     </h2>
    #     """,
    #     unsafe_allow_html=True
    # )

    # # Période formatée avec un style professionnel
    # st.markdown(
    #     f"""
    #     <h4 style="
    #         text-align: center; 
    #         color: #333333; 
    #         font-family: Arial, sans-serif; 
    #         margin-top: 5px;
    #     ">
    #         Période : {date1.strftime('%d/%m/%Y')} - {date2.strftime('%d/%m/%Y')}
    #     </h4>
    #     """,
    #     unsafe_allow_html=True
    # )

    # st.markdown(
    #     f"""
    #     <h3 style="
    #         text-align: center; 
    #         color: #4A90E2; 
    #         font-family: Arial, sans-serif; 
    #         margin-bottom: 20px;
    #     ">
    #         Visualisation de {param.capitalize()}
    #     </h3>
    #     """,
    #     unsafe_allow_html=True
    # )

    #     # df['Date'] = df['date'].astype(str)
    # df_labo[param] = df_labo[param].astype(str).str.replace(',', '.')
    # df_labo.replace(['-'], np.nan, inplace=True)
    # df_labo[param] = pd.to_numeric(df_labo[param], errors='coerce')
    # df_labo['Date'] = df_labo['date'].astype(str) + " " + df_labo['Heur'].astype(str)
    # print(df_labo.columns)
    # # Conteneur professionnel avec largeur personnalisée
    # st.markdown(
    #     f"""
    #     <div style="
    #         background-color: #F9F9F9; 
    #         border: 1px solid #D1D1D1; 
    #         border-radius: 8px; 
    #         padding: 20px; 
    #         margin: 0 auto 20px auto; 
    #         box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1); 
    #         width: 60%; /* Ajustez ce pourcentage selon vos besoins */
    #         max-width: 800px; /* Largeur maximale pour éviter une trop grande expansion */
    #     ">
    #         <h2 style="
    #             text-align: center; 
    #             color: #4A90E2; 
    #             font-family: Arial, sans-serif; 
    #             margin-bottom: 0;
    #         ">
    #             {param.capitalize()} Journalièr: {np.around(df_labo[param].iloc[-1], 2)} 
    #         </h2>
    #     </div>
    #     """, 
    #     unsafe_allow_html=True
    # )



    # # Personnalisation du graphique avec un style moderne
    # fig = px.line(
    #     df_labo,
    #     x="Date",
    #     y=param,
    #     title=f"Évolution de {param.capitalize()} au fil du temps",
    #     labels={
    #         "Date": "Date",
    #         param: param.capitalize()
    #     },
    #     template="plotly_white",  # Thème moderne
    # )
    # fig.update_layout(
    # title=dict(
    #     text=f"Évolution de {param.capitalize()}",
    #     font=dict(size=20),
    #     x=0.5,
    #     xanchor="center"
    # ),
    # xaxis=dict(
    #     title_text="Date",
    #     tickangle=-45,
    #     showticklabels=False  # This hides the date labels on the x-axis
    # ),
    # yaxis=dict(title_text=f"{param.capitalize()}"),
    # margin=dict(l=50, r=50, t=60, b=40),
    # height=400,
    # )

    # st.plotly_chart(fig, use_container_width=True)