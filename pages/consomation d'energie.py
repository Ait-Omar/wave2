import streamlit as st
import pandas as pd
from PIL import Image
import base64
from io import BytesIO
import plotly.express as px
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Analyse Énergie - Station Wave 2",
    page_icon="⚡",
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
            font-family: 'Jost';
            font-size: 16px;
            font-weight: 600;
            width: 100%;
            transition: all 0.3s ease;
        }

        section[data-testid="stSidebar"] button:hover {
            background-color: #e6e6e6;
            color: #4A90E2;
        }
       body {
            background-color: #FAF7F0;
        }
        h2 {
            font-family: Jost;
            color: #34495e;
            animation: slideIn 1s ease-in-out;
        }
        .kpi-box {
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            font-family: Jost;
            color: #2c3e50;
        }
        .stMetric {
            margin-bottom: 15px;
        }
        .footer {
            font-size: 14px;
            color: #7f8c8d;
            text-align: center;
            padding-top: 40px;
            padding-bottom: 20px;
        }
        @keyframes slideIn {
            from { transform: translateX(-50px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Charger les données
df = pd.read_excel('Consommation spécifique.xlsx', sheet_name='Energie')

df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Define the start and end dates for filtering
startDate = df['date'].min()
endDate = df['date'].max()

# Sidebar for date range selection
st.sidebar.subheader("Filtrer par période")
date1 = pd.to_datetime(st.sidebar.date_input("Date de début", startDate))
date2 = pd.to_datetime(st.sidebar.date_input("Date de fin", endDate))

# Filter the data by date range
df = df[(df["date"] >= date1) & (df["date"] <= date2)]

# Titre principal
st.markdown("<h2 style='text-align: center;font-family: Jost;'> Consommation Énergie</h2>", unsafe_allow_html=True)


# Sélection du paramètre pour l'analyse
param = st.sidebar.selectbox(f"Paramètre à visualiser", df.columns[2:])

# Visualisation des données
def consomation_energie(df, param):
    # Indicateurs clés en haut
    st.markdown(
        f"<h3 style='text-align: center; color: #4A90E2;font-family:Jost;'> {param.capitalize()}</h3>",
        unsafe_allow_html=True
    )
    if param == "Energie spécifique":
      st.markdown(
        """
        <style>
        .kpi-box {
           background-color: #F9F9F9; 
        border: 1px solid #D1D1D1; 
        border-radius: 8px; 
        padding: 20px; 
        margin: 0 auto 20px auto; 
        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1); 
        width: 60%; /* Ajustez ce pourcentage selon vos besoins */
        max-width: 800px; /* Largeur maximale pour éviter une trop grande expansion */
        }
   
        """,
        unsafe_allow_html=True
    )
      st.markdown(
            f"""
            <div class="kpi-box">
                <h2 style="
                text-align: center; 
                color: #4A90E2; 
                font-family: Jost; 
                margin-bottom: 0;">
                Energie spécifique : {np.around(df[param].iloc[-1],3)}
                </h2>
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        # Style CSS pour les boîtes KPI
        st.markdown(
        """
        <style>
        .kpi-box {
           background-color: #F9F9F9; 
        border: 1px solid #D1D1D1; 
        border-radius: 8px; 
        padding: 20px; 
        margin: 0 auto 20px auto; 
        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1); 
        width: 60%; /* Ajustez ce pourcentage selon vos besoins */
        max-width: 800px; /* Largeur maximale pour éviter une trop grande expansion */
        }
   
        """,
        unsafe_allow_html=True
    )

    # Colonne 1 : Moyenne

        st.markdown(
        f"""
        <div class="kpi-box">
            <h2 style="
            text-align: center; 
            color: #4A90E2; 
            font-family: Jost; 
            margin-bottom: 0;">
            Consommation journalière : {np.around(df[param].iloc[-1],3)}
            </h2>
        </div>
        """, 
        unsafe_allow_html=True
    )



   


    # Graphique de la tendance
    fig = px.line(
        df, 
        x="date", 
        y=param, 
        title=f"Tendance de {param.capitalize()} pendant  {date1.strftime('%d/%m/%Y')} - {date2.strftime('%d/%m/%Y')}",
        labels={"date": "Date", param: param.capitalize()},
        template="plotly_white"
    )

    fig.update_layout(
        title=dict(
            text=f"Évolution de {param.capitalize()} Pendant {date1.strftime('%d/%m/%Y')} - {date2.strftime('%d/%m/%Y')}",
            font=dict(size=20, family='Jost'),
            x=0.5,
            xanchor="center"
        ),
        font=dict(size=14),
        xaxis=dict(
        title=dict(text="Date", font=dict(size=16)),
        tickangle=0,
        showgrid=False,
        showticklabels=True,
        tickformat="%d",  # ✅ Only the day of the month (e.g., 01, 15, 30)
        tickfont=dict(size=20, color='black', family='Jost', weight='bold'),
         ),
        yaxis=dict(
            title=dict(text="Valeur", font=dict(size=16)),
            showgrid=False  # ❌ No horizontal grid lines
        ),
        margin=dict(l=40, r=40, t=60, b=40),
        height=500,
    )

    st.plotly_chart(fig, use_container_width=True)


    # Analyse de la distribution
if st.sidebar.button('Apply'):
    consomation_energie(df, param)

st.markdown(
    """
    <div class="footer">
        © 2025 Station de Dessalement Wave 2 - Jorf Lasfar | Interface développée par DIPS
    </div>
    """,
    unsafe_allow_html=True
)
