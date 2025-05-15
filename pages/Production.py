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
st.markdown(
        """
        <head>
            <link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;600&display=swap" rel="stylesheet">
        </head>
        """,
        unsafe_allow_html=True
    )
st.markdown("""
    <style>
            body, .stApp {
        background-color: #FAF7F0;
    }
    /* Target all buttons in the sidebar */
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
# Titre et description
st.title("Production - Station Wave 2")
st.markdown(
    """
    <div style="
        text-align: justify; 
        color: #333333; 
        font-family: Jost; 
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

df['date'] = pd.to_datetime(df['date'], errors='coerce')
df.dropna(subset=['date'], inplace=True)

# Define the date range for filtering
startDate = df['date'].min()
endDate = df['date'].max()

# Sidebar for date range selection
st.sidebar.header("🔍 Options de Filtrage")
st.sidebar.subheader("📅 Filtrer par période")
date1 = pd.to_datetime(st.sidebar.date_input("Date de début", startDate))
date2 = pd.to_datetime(st.sidebar.date_input("Date de fin", endDate))

# Filter the DataFrame based on the selected date range
df = df[(df["date"] >= date1) & (df["date"] <= date2)]

# Sélection du paramètre à visualiser
st.sidebar.subheader("🚄 Sélection du Train de Production")
if len(df.columns) > 2:
    param = st.sidebar.selectbox("Choisissez un train :", df.columns[2:])
else:
    st.error("Aucune donnée de production disponible pour cette période.")
    st.stop()

# Affichage des informations sélectionnées

if st.sidebar.button('Apply'):
    df.replace(['wbw','soak ceb1','w-f','f','F','w-bw','WBW','W.BW','W,BW','ceb1','CEB2','bw','wf','wb','W-F','W.F','hs','WF','wB','BW','w,b','W,F','W-BW','ceb2','SOAK CEB1','W,B','CEB1','SOAK CEB2','HS',
                ], 
               np.nan, inplace=True)
    
    if param != "total production ":
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
        col1,col2,col3,col4 = st.columns((4))
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
                <h3 style="
                    text-align: center; 
                    color: #4A90E2; 
                    font-family: Jost; 
                    margin-bottom: 0;
                ">
                    Réalisé : {df[param].iloc[-1]} m³
                </h3>
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
                <h3 style="
                    text-align: center; 
                    color: #4A90E2; 
                    font-family: Jost; 
                    margin-bottom: 0;
                ">
                    Prévue : 15000 m³
                </h3>
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
                <h3 style="
                    text-align: center; 
                    color: #4A90E2; 
                    font-family: Jost; 
                    margin-bottom: 0;
                ">
                    Ecart: {np.round(df[param].iloc[-1]-15000,2)} m³
                </h3>
            </div>
            """, 
            unsafe_allow_html=True
        )
            with col4:
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
                <h3 style="
                    text-align: center; 
                    color: #4A90E2; 
                    font-family: Jost; 
                    margin-bottom: 0;
                ">
                    Taux: {np.round(df[param].iloc[-1]/15000*100,2)} %
                </h3>
            </div>
            """, 
            unsafe_allow_html=True
        )

    

        fig = px.line(
            df,
            x="date",
            y=param,
            title=f"Évolution de {param.capitalize()} au fil du temps",
            labels={
                "date": "date",
                param: param.capitalize()
            },
            template="plotly_white",  # Thème moderne
        )

        # Options pour améliorer le design
        fig.update_traces(line=dict(width=2))  # Épaisseur des lignes
        fig.update_layout(
            title=dict(
                text=f"Évolution de la Production pendant {date1.strftime('%d/%m/%Y')} - {date2.strftime('%d/%m/%Y')}",
                font=dict(size=20, family='Jost'),
                x=0.5,
                xanchor="center"
            ),
            xaxis=dict(
                title_text="",
                tickangle=0,
                showticklabels=True,
                tickformat="%d",
                tickfont=dict(size=20, color='black', family='Jost', weight='bold'),
                showgrid=False  # Removes vertical grid lines (optional)
            ),
            yaxis=dict(
                title_text=f"{param.capitalize()}",
                showgrid=False  # ✅ This removes horizontal grid lines
            ),
            margin=dict(l=40, r=40, t=60, b=40),
            height=400,
        )

        fig.add_hline(y=15000, line_color="red", line_width=1)
        fig.add_annotation(
                    x=df['date'].iloc[-1], 
                    y=15000, 
                    text="Production Prévue (15000 m³)",  
                    showarrow=True, 
                    arrowhead=2,  
                    ax=0, 
                    ay=-40  
                )



        # Affichage du graphique
        st.plotly_chart(fig, use_container_width=True)
    else:
        col1,col2,col3,col4 = st.columns((4))
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
                <h3 style="
                    text-align: center; 
                    color: #4A90E2; 
                    font-family: Jost; 
                    margin-bottom: 0;
                ">
                    Réalisé: {df[param].iloc[-1]} m³
                </h3>
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
                <h3 style="
                    text-align: center; 
                    color: #4A90E2; 
                    font-family:Jost; 
                    margin-bottom: 0;
                ">
                Prévue: 120000 m³
                </h3>
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
                <h3 style="
                    text-align: center; 
                    color: #4A90E2; 
                    font-family: Jost; 
                    margin-bottom: 0;
                ">
                    Ecart: {np.round(df[param].iloc[-1]-120000,2)} m³
                </h3>
            </div>
            """, 
            unsafe_allow_html=True
        )
            with col4:
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
                <h3 style="
                    text-align: center; 
                    color: #4A90E2; 
                    font-family:Jost; 
                    margin-bottom: 0;
                ">
                    Taux: {np.round(df[param].iloc[-1]/120000*100,2)} %
                </h3>
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
        fig.update_traces(line=dict(width=2))  # Épaisseur des lignes
        fig.update_layout(
            title=dict(
                text=f"Évolution de la Production pendant {date1.strftime('%d/%m/%Y')} - {date2.strftime('%d/%m/%Y')}",
                font=dict(size=20, family='Jost'),
                x=0.5,
                xanchor="center"
            ),
            xaxis=dict(
                title_text="",
                tickangle=0,
                showticklabels=True,
                tickformat="%d",
                tickfont=dict(size=20, color='black', family='Jost', weight='bold'),
                showgrid=False  # Removes vertical grid lines (optional)
            ),
            yaxis=dict(
                title_text=f"{param.capitalize()}",
                showgrid=False  # ✅ This removes horizontal grid lines
            ),
            margin=dict(l=40, r=40, t=60, b=40),
            height=400,
        )

        fig.add_hline(y=120000, line_color="red", line_width=2)
        fig.add_annotation(
                    x=df['date'].iloc[-1], 
                    y=120000, 
                    text="Production Prévue (120000 m³)", 
                    showarrow=True, 
                    arrowhead=2,  
                    ax=0, 
                    ay=-40  
                )


        # Affichage du graphique
        st.plotly_chart(fig, use_container_width=True)


st.markdown(
    """
    <div class="footer">
        © 2025 Station de Dessalement Wave 2 - Jorf Lasfar | Interface développée par DIPS
    </div>
    """,
    unsafe_allow_html=True
)