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


option = st.sidebar.multiselect("Options",['Laboratoir','Scada','Chantier'])


if option == ['Laboratoir']:
    excel_file = pd.ExcelFile('suivi qualité.xlsx')
    sheet_names = excel_file.sheet_names[1:]
    # Barre latérale pour la sélection de la phase
    st.sidebar.header("Options de Visualisation")
    don = st.sidebar.radio("Phases de traitement :", sheet_names )
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
    don1 = st.sidebar.radio("Phases de traitement :", sheet_names1)
    df1=  pd.read_excel('suivi 3h standart DIPS.xlsx', sheet_name=don1)

    excel_file2 = pd.ExcelFile('suivi qualité.xlsx')
    sheet_names2 = excel_file2.sheet_names[1:]
  
#   Barre latérale pour la sélection de la phase
    st.sidebar.header("Laboratoire")
    don2 = st.sidebar.radio("Phases de traitement :", sheet_names2)
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
            font-family: Arial, sans-serif; 
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
    st.markdown(f"<h3 style='text-align: center;'>Corrélation entre {param1} de {don1} et {param2} de {don2}</h3>", unsafe_allow_html=True)

    fig = px.line(
    df_melted,
    x="Date",
    y="Value",
    color='Parameter',
    color_discrete_sequence=['#1f77b4', '#ff7f0e']
)

    fig.update_layout(
        font=dict(family="Arial", size=14),
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

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df['Date'], y=df[param1],
                            name=param1, yaxis="y1", line=dict(color='#1f77b4')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df[param2],
                            name=param2, yaxis="y2", line=dict(color='#ff7f0e')))

    fig.update_layout(
        title=f"Évolution parallèle de {param1} et {param2}",
        xaxis=dict(title="Date"),
        yaxis=dict(title=param1, titlefont=dict(color='#1f77b4'), tickfont=dict(color='#1f77b4')),
        yaxis2=dict(title=param2, titlefont=dict(color='#ff7f0e'), tickfont=dict(color='#ff7f0e'),
                    overlaying='y', side='right'),
        legend=dict(x=0.5, y=1.1, orientation='h'),
        height=500,
        plot_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)
    
    # corr = df[[param1, param2]].corr()

    # fig, ax = plt.subplots()
    # sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=ax)
    # st.pyplot(fig)

    # st.markdown(f"<h3 style='text-align: center;'>Corrélation entre {param1} de {don1} et {param2} de {don2}</h3>", unsafe_allow_html=True)        
    # fig = px.line(df,x="Date",y=df.columns[1:])
    # fig.update_traces(line=dict(color='#00A8CC'), selector=dict(name=df1.columns[1]))
    # fig.update_traces(line=dict(color='#FF4B4A'), selector=dict(name=df1.columns[2]))
    # st.plotly_chart(fig,use_container_width=True,height = 200)


    
    # # st.plotly_chart(fig, use_container_width=True)
    # fig = make_subplots(specs=[[{"secondary_y": True}]])

    # fig.add_trace(
    #     go.Scatter(x=df['Date'], y=df[df.columns[1]], name=df.columns[1],line=dict(color='#095DBA', width=2)),
    #     secondary_y=False,
    # )

    # fig.add_trace(
    #     go.Scatter(x=df['Date'], y=df[df.columns[2]], name=df.columns[2],line=dict(color='#FF4B4A', width=2),),
    #     secondary_y=True,
    # )

    # fig.update_layout(
    #     title_text=f"Corellation entre {df.columns[1]} et {df.columns[2]}",
    #     title_x=0.3,
    #     height=600,
        
    # )

    # fig.update_xaxes(title_text="Date")

    # fig.update_yaxes(title_text=df.columns[1], secondary_y=False)
    # fig.update_yaxes(title_text=df.columns[2], secondary_y=True)

    # st.plotly_chart(fig, use_container_width=True)

 

