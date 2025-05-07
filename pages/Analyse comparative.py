import streamlit as st
import pandas as pd
from PIL import Image
import base64
from io import BytesIO
import plotly.express as px
import json
from datetime import datetime
import numpy as np
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from fonctions import laboratoir,transform_laboratory_data

st.set_page_config(
    page_title="Suivi laboratoire - Station Wave 2",
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

st.markdown(
    """
    <h1 style='text-align: center; 
               font-family: "Jost", sans-serif; 
               font-weight: 600;
               font-size: 42px;
               margin-bottom: 30px;'>
        Analyse Comparative
    </h1>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <div style=' text-align: justify; 
#         color: #333333; 
#         font-family: Jost; 
#         line-height: 1.6; 
#         border-left: 4px solid #4A90E2; 
#         padding-left: 10px;
#         margin-bottom: 20px;'
#        >
        <strong>Explorez les données de performance</strong> des différentes phases de traitement de la station de dessalement <strong>Wave 2</strong>. 
         Sélectionnez une phase, définissez une période et visualisez les paramètres clés pour mieux comprendre et analyser le processus.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>
            body, .stApp {
        background-color: #FAF7F0;
    }
            section[data-testid="stSidebar"] button {
        background-color: #F9F9F9;
        border: 1px solid #D1D1D1;
        border-radius: 8px;
        padding: 15px;
        margin-top: 10px;
        margin-bottom: 20px;
        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
        color: #4A90E2;
        font-family: 'Jost', sans-serif;
        font-size: 16px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
    }

    section[data-testid="stSidebar"] button:hover {
        background-color: #e6e6e6;
        color: #4A90E2;
    }
            .footer {
            font-size: 14px;
            color: #7f8c8d;
            text-align: center;
            padding-top: 40px;
            padding-bottom: 20px;
            body {
        background-color: #FAF7F0;
        }
    </style>
""", unsafe_allow_html=True)

option = st.sidebar.multiselect("Options",['Laboratoir','Scada','Chantier'])

if option == ['Laboratoir']:
    excel_file = pd.ExcelFile('suivi qualité.xlsx')
    sheet_names = excel_file.sheet_names[1:]
    # Barre latérale pour la sélection de la phase
    st.sidebar.header("Options de Visualisation")
    don = st.sidebar.radio("Phases de traitement :", sheet_names )
    df_labo = transform_laboratory_data('suivi qualité.xlsx', sheet_name=don)
    print(df_labo)
  
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

    if st.sidebar.button('Apply'):
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
    excel_file = pd.ExcelFile('SUIVI STANDART DIPS.xlsx')
    sheet_names = excel_file.sheet_names[1:]
    # Barre latérale pour la sélection de la phase
    st.sidebar.header("Options de Visualisation")
    don = st.sidebar.radio("Phases de traitement :", sheet_names)
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
    if st.sidebar.button('Apply'):
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
    excel_file = pd.ExcelFile('suivi 3h standart DIPS.xlsx')
    sheet_names = excel_file.sheet_names[1:]

#   Barre latérale pour la sélection de la phase
    st.sidebar.header("Options de Visualisation")
    don = st.sidebar.radio("Phases de traitement :", sheet_names)
    df=  pd.read_excel('suivi 3h standart DIPS.xlsx', sheet_name=don)


    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.strftime('%d/%m/%Y')  # Format 'dd/mm/yyyy'
    


    startDate = pd.to_datetime(df["date"], format='%d/%m/%Y').min()
    endDate = pd.to_datetime(df["date"], format='%d/%m/%Y').max()


    st.sidebar.subheader("Filtrer par période")
    date1 = pd.to_datetime(st.sidebar.date_input("Date de début", startDate))
    date2 = pd.to_datetime(st.sidebar.date_input("Date de fin", endDate))

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
         [col for col in df.columns if col not in ['date', 'Heur']] ,
        help="Choisissez un paramètre à afficher parmi les colonnes disponibles."
    )
    if st.sidebar.button('Apply'):
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

            # df['Date'] = df['date'].astype(str)
        df[param] = df[param].astype(str).str.replace(',', '.')
        df.replace(['-'], np.nan, inplace=True)
        df[param] = pd.to_numeric(df[param], errors='coerce')
        df['Date'] = df['date'].astype(str) + " " + df['Heur'].astype(str)
        # Conteneur professionnel avec largeur personnalisée
        st.markdown(
            f"""
            <div style="
                background-color: #F9F9F9; 
                border: 1px solid #D1D1D1; 
                border-radius: 8px; 
                padding: 20px; 
                margin: 0 auto 20px auto; 
                box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1); 
                width: 60%; /* Ajustez ce pourcentage selon vos besoins */
                max-width: 800px; /* Largeur maximale pour éviter une trop grande expansion */
            ">
                <h2 style="
                    text-align: center; 
                    color: #4A90E2; 
                    font-family: Arial, sans-serif; 
                    margin-bottom: 0;
                ">
                    {param.capitalize()} Journalièr: {np.around(df[param].iloc[-1], 2)} 
                </h2>
            </div>
            """, 
            unsafe_allow_html=True
        )



        # Personnalisation du graphique avec un style moderne
        fig = px.line(
            df,
            x="Date",
            y=param,
            title=f"Évolution de {param.capitalize()} au fil du temps",
            labels={
                "Date": "Date",
                param: param.capitalize()
            },
            template="plotly_white",  # Thème moderne
        )
        fig.update_layout(
        title=dict(
            text=f"Évolution de {param.capitalize()}",
            font=dict(size=20),
            x=0.5,
            xanchor="center"
        ),
        xaxis=dict(
            title_text="Date",
            tickangle=-45,
            showticklabels=False  # This hides the date labels on the x-axis
        ),
        yaxis=dict(title_text=f"{param.capitalize()}"),
        margin=dict(l=50, r=50, t=60, b=40),
        height=400,
        )

        st.plotly_chart(fig, use_container_width=True)
elif option == ['Laboratoir', 'Chantier']:
    excel_file1 = pd.ExcelFile('suivi 3h standart DIPS.xlsx')
    sheet_names1 = excel_file1.sheet_names[1:]

#   Barre latérale pour la sélection de la phase
    st.sidebar.header("Chantier")
    don1 = st.sidebar.selectbox("Phases de traitement :", sheet_names1)

    df1=  pd.read_excel('suivi 3h standart DIPS.xlsx', sheet_name=don1)

    excel_file2 = pd.ExcelFile('suivi qualité.xlsx')
    sheet_names2 = excel_file2.sheet_names[1:]
  
#   Barre latérale pour la sélection de la phase
    st.sidebar.header("Laboratoire")
    don2 = st.sidebar.selectbox("Phases de traitement :", sheet_names2)
    df2 = transform_laboratory_data('suivi qualité.xlsx', sheet_name=don2)
    # df2=  pd.read_excel('suivi qualité.xlsx', sheet_name=don2)

    startDate = pd.to_datetime(df1["date"], format='%d/%m/%Y').min()
    endDate = pd.to_datetime(df1["date"], format='%d/%m/%Y').max()

    st.sidebar.subheader("Filtrer par période")
    date1 = pd.to_datetime(st.sidebar.date_input("Date de début", startDate))
    date2 = pd.to_datetime(st.sidebar.date_input("Date de fin", endDate))

    df1['date'] = pd.to_datetime(df1['date'], format='%d/%m/%Y')
    df1 = df1[(df1["date"] >= date1) & (df1["date"] <= date2)]
    df1['date'] = df1['date'].dt.strftime('%d/%m/%Y')  # Format pour affichage
 
    st.sidebar.markdown(
        """
        <h3 style="
            color: #4A90E2; 
            font-family: Jost; 
            margin-bottom: 15px;
        ">
            Sélectionnez un paramètre
        </h3>
        """,
        unsafe_allow_html=True
    )

    # Sélection du paramètre à visualiser
    param1 = st.sidebar.selectbox(
        'Paramètre', 
         [col for col in df1.columns if col not in ['date', 'Heur']] ,
        help="Choisissez un paramètre à afficher parmi les colonnes disponibles."
    )
    param2 = st.sidebar.selectbox(
        'Paramètre', 
        [col for col in df2.columns if col not in ['date', 'point', 'poste', 'source']],
        help="Choisissez un paramètre à afficher parmi les colonnes disponibles."
    )

    if st.sidebar.button('Apply'):
            # df['Date'] = df['date'].astype(str)
        df1[param1] = df1[param1].astype(str).str.replace(',', '.')
        df1.replace(['-'], np.nan, inplace=True)
        df1[param1] = pd.to_numeric(df1[param1], errors='coerce')
        df1['Date'] = df1['date'].astype(str) + " " + df1['Heur'].astype(str)


        df2.replace(0, np.nan, inplace=True)
        df2.replace('/', np.nan, inplace=True)
        df2.replace('-', np.nan, inplace=True)
        df2.replace('CIP', np.nan, inplace=True)
        df2.replace('erroné', np.nan, inplace=True)
        df2.replace('en cours', np.nan, inplace=True)
        df = {
        'Date': df1['Date'],
        param1: pd.to_numeric(df1[param1], errors='coerce'),
        param2: pd.to_numeric(df2[param2], errors='coerce')
        }
        df = pd.DataFrame(df)

        # Melt for long-form to control styling better
        df_melted = df.melt(id_vars='Date', var_name='Parameter', value_name='Value')

        # Title
        st.markdown(f"<h3 style='text-align: center;font-family:Jost;'>Corrélation entre {param1} de {don1} et {param2} de {don2}</h3>", unsafe_allow_html=True)

        fig = px.line(
        df_melted,
        x="Date",
        y="Value",
        color='Parameter',
        color_discrete_sequence=['#1f77b4', '#ff7f0e']
    )

        fig.update_layout(
            font=dict(family="Jost", size=14),
            legend=dict(
                title="",
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            xaxis=dict(
                title="Date",
                tickformat="%d/%m",  # Only show day/month
                tickangle=0,
                nticks=10,  # Limit number of ticks shown
                showgrid=False
            ),
            yaxis=dict(
                title="Valeur",
                showgrid=True,
                gridcolor="lightgrey"
            ),
            plot_bgcolor="white",
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)
elif option == ['Laboratoir', 'Scada']:
    excel_file1 = pd.ExcelFile('SUIVI STANDART DIPS.xlsx')
    sheet_names1 = excel_file1.sheet_names[1:]

    st.sidebar.header("Scada")
    don1 = st.sidebar.selectbox("Phases de traitement (Scada):", sheet_names1)

    df1 = pd.read_excel('SUIVI STANDART DIPS.xlsx', sheet_name=don1)

    excel_file2 = pd.ExcelFile('suivi qualité.xlsx')
    sheet_names2 = excel_file2.sheet_names[1:]

    st.sidebar.header("Laboratoire")
    don2 = st.sidebar.selectbox("Phases de traitement (Laboratoire):", sheet_names2)
    df2 = transform_laboratory_data('suivi qualité.xlsx', sheet_name=don2)

    # Définir les bornes de date
    startDate = pd.to_datetime(df1["date"], format='%d/%m/%Y').min()
    endDate = pd.to_datetime(df1["date"], format='%d/%m/%Y').max()

    st.sidebar.subheader("Filtrer par période")
    date1 = pd.to_datetime(st.sidebar.date_input("Date de début", startDate))
    date2 = pd.to_datetime(st.sidebar.date_input("Date de fin", endDate))

    df1['date'] = pd.to_datetime(df1['date'], format='%d/%m/%Y')
    df1 = df1[(df1["date"] >= date1) & (df1["date"] <= date2)]
    df1['date'] = df1['date'].dt.strftime('%d/%m/%Y')

    st.sidebar.markdown("<h3 style='color: #4A90E2;'>Sélectionnez un paramètre</h3>", unsafe_allow_html=True)

    param1 = st.sidebar.selectbox('Paramètre Scada', [col for col in df1.columns if col not in ['date', 'poste']])
    param2 = st.sidebar.selectbox('Paramètre Laboratoire', [col for col in df2.columns if col not in ['date', 'point', 'poste', 'source']])
    if st.sidebar.button('Apply'):
        # Nettoyage Scada
        df1[param1] = df1[param1].astype(str).str.replace(',', '.')
        df1.replace(['-'], np.nan, inplace=True)
        df1[param1] = pd.to_numeric(df1[param1], errors='coerce')
        df1['Date'] = pd.to_datetime(df1['date'], format='%d/%m/%Y', errors='coerce')
        # df1['Date'] = df1['date']

        # Nettoyage Labo
        df2.replace([0, '/', '-', 'CIP', 'erroné', 'en cours'], np.nan, inplace=True)
        df2[param2] = pd.to_numeric(df2[param2], errors='coerce')
        df2['Date'] = pd.to_datetime(df2['date'], format='%d/%m/%Y', errors='coerce')
        # df2['Date'] = df2['date']

        # Jointure intelligente par date
        df = pd.merge(df1[['Date', param1]], df2[['Date', param2]], on='Date', how='inner')

        df_melted = df.melt(id_vars='Date', var_name='Parameter', value_name='Value')

        st.markdown(f"<h3 style='text-align: center;font-family:Jost;'>Corrélation entre {param1} (Scada) et {param2} (Laboratoire)</h3>", unsafe_allow_html=True)

        fig = px.line(
            df_melted,
            x="Date",
            y="Value",
            color='Parameter',
            color_discrete_sequence=['#2ca02c', '#d62728']
        )

        fig.update_layout(
            font=dict(family="Jost", size=14),
            legend=dict(title="", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(title="Date", tickformat="%d/%m", tickangle=0),
            yaxis=dict(title="Valeur"),
            plot_bgcolor="white",
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
        """
        <div class="footer">
            © 2025 Station de Dessalement Wave 2 - Jorf Lasfar | Interface développée par DIPS
        </div>
        """,
        unsafe_allow_html=True
    )    
elif option == ['Scada', 'Chantier']:
    # Charger SCADA
    excel_file1 = pd.ExcelFile('SUIVI STANDART DIPS.xlsx')
    sheet_names1 = excel_file1.sheet_names[1:]
    st.sidebar.header("SCADA")
    don1 = st.sidebar.selectbox("Phases de traitement (Scada):", sheet_names1)
    df1 = pd.read_excel('SUIVI STANDART DIPS.xlsx', sheet_name=don1)

    # Charger CHANTIER
    excel_file2 = pd.ExcelFile('suivi 3h standart DIPS.xlsx')
    sheet_names2 = excel_file2.sheet_names[1:]
    st.sidebar.header("Chantier")
    don2 = st.sidebar.selectbox("Phases de traitement (Chantier):", sheet_names2)
    df2 = pd.read_excel('suivi 3h standart DIPS.xlsx', sheet_name=don2)

    # Définir plage de dates
    startDate = pd.to_datetime(df1["date"], format='%d/%m/%Y').min()
    endDate = pd.to_datetime(df1["date"], format='%d/%m/%Y').max()
    st.sidebar.subheader("Filtrer par période")
    date1 = pd.to_datetime(st.sidebar.date_input("Date de début", startDate))
    date2 = pd.to_datetime(st.sidebar.date_input("Date de fin", endDate))

    # Nettoyage Scada
    df1['date'] = pd.to_datetime(df1['date'], format='%d/%m/%Y')
    df1 = df1[(df1["date"] >= date1) & (df1["date"] <= date2)]
    df1['date'] = df1['date'].dt.strftime('%d/%m/%Y')

    # Nettoyage Chantier
    df2['date'] = pd.to_datetime(df2['date'], format='%d/%m/%Y')
    df2 = df2[(df2["date"] >= date1) & (df2["date"] <= date2)]
    df2['date'] = df2['date'].dt.strftime('%d/%m/%Y')

    st.sidebar.markdown("<h3 style='color: #4A90E2;'>Sélectionnez un paramètre</h3>", unsafe_allow_html=True)

    param1 = st.sidebar.selectbox('Paramètre Scada', [col for col in df1.columns if col not in ['date', 'poste']])
    param2 = st.sidebar.selectbox('Paramètre Chantier', [col for col in df2.columns if col not in ['date', 'Heur']])
    if st.sidebar.button('Apply'):
        # Nettoyage des valeurs
        df1[param1] = df1[param1].astype(str).str.replace(',', '.')
        df1.replace(['-'], np.nan, inplace=True)
        df1[param1] = pd.to_numeric(df1[param1], errors='coerce')
        df1['Date'] = pd.to_datetime(df1['date'], format='%d/%m/%Y', errors='coerce')
        # df1['Date'] = df1['date']

        df2[param2] = df2[param2].astype(str).str.replace(',', '.')
        df2.replace(['-'], np.nan, inplace=True)
        df2[param2] = pd.to_numeric(df2[param2], errors='coerce')
        df2['Date'] = pd.to_datetime(df2['date'], format='%d/%m/%Y', errors='coerce')
        # df2['Date'] = df2['date'] + " " + df2['Heur'].astype(str)

        # Fusion intelligente par date simple (tu peux faire plus précis par heure si besoin)
        df_merge = pd.merge(df1[['Date', param1]], df2[['Date', param2]], on='Date', how='inner')

        df_melted = df_merge.melt(id_vars='Date', var_name='Parameter', value_name='Value')

        st.markdown(f"<h3 style='text-align: center;font-family:Jost;'>Corrélation entre {param1} (Scada) et {param2} (Chantier)</h3>", unsafe_allow_html=True)

        fig = px.line(
            df_melted,
            x="Date",
            y="Value",
            color='Parameter',
            color_discrete_sequence=['#17becf', '#bcbd22']
        )

        fig.update_layout(
            font=dict(family="Jost", size=14),
            legend=dict(title="", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(title="Date", tickformat="%d/%m", tickangle=0),
            yaxis=dict(title="Valeur"),
            plot_bgcolor="white",
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)
