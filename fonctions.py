import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from PIL import Image




def visualise(df,param,on):
    if on == "UF":
        df.replace('F', np.nan, inplace=True)
        df.replace('BW', np.nan, inplace=True)
        df.replace('f', np.nan, inplace=True)
        df.replace('W.BW', np.nan, inplace=True)
        df.replace('w-bw	', np.nan, inplace=True)
        df.replace('W.F	', np.nan, inplace=True)
        df.replace('W-F', np.nan, inplace=True)
        df.replace('wb', np.nan, inplace=True)
        df.replace('SOAK CEB1	', np.nan, inplace=True)
        df.replace('w-f	', np.nan, inplace=True)
        df.replace('HS	', np.nan, inplace=True)
        df.replace('SOAK CEB1	', np.nan, inplace=True)
        df.replace('W-BW	', np.nan, inplace=True)
        df.replace('bw	', np.nan, inplace=True)
        df.replace('W.F	', np.nan, inplace=True)
        df.replace('bw	', np.nan, inplace=True)
        df.replace('w-bw	', np.nan, inplace=True)
        df.replace('WB', np.nan, inplace=True)
        df.replace('bw', np.nan, inplace=True)
    df['combined'] = df['date'].astype(str) + " " + df['poste'].astype(str)
    # df['label_short'] = range(1, len(df) + 1)  # Utiliser des indices numériques pour l'axe X

    st.markdown(f"<h2 style='text-align: center;'>{param} moyen: {np.around(df[param].mean(),2)}</h2>", unsafe_allow_html=True)        
    fig = px.line(df,x="combined",y=param)
    # fig.update_xaxes(
    # tickvals=df['combined'],  # Points de la colonne combinée
    # ticktext=df['label_short'])  # Étiquettes abrégées (indices ou autre)
    st.plotly_chart(fig,use_container_width=True,height = 200)

def consomation(df,param):
    st.markdown(f"<h2 style='text-align: center;'>{param[:-5]} moyen: {np.around(df[param].mean(),2)}</h2>", unsafe_allow_html=True)        
    fig = px.line(df,x="date",y=param)
    st.plotly_chart(fig,use_container_width=True,height = 200)

def   consomation_energie(df,param):
    st.markdown(f"<h2 style='text-align: center;'>{param}: {np.around(df[param].mean(),2)}</h2>", unsafe_allow_html=True)        
    fig = px.line(df,x="Date",y=param)
    st.plotly_chart(fig,use_container_width=True,height = 200)

def anomali(df):

    st.title("Suivi des Anomalies Journalières")

    # Tableau interactif
    st.subheader("Tableau des Anomalies")
    # st.dataframe(df)

    # Filtrage
    lieux = df['Emplacement'].unique()
    lieu_filtre = st.selectbox("Filtrer par lieu :", ["Tous"] + list(lieux))
    if lieu_filtre != "Tous":
        df = df[df["Emplacement"] == lieu_filtre]
    st.dataframe(df)
    # Photos (exemple avec image fictive)
    st.subheader("Photos des Anomalies")
    uploaded_photo = st.file_uploader("Télécharger une photo de l'anomalie :", type=["jpg", "png"])
    if uploaded_photo:
        img = Image.open(uploaded_photo)
        st.image(img, caption="Photo téléchargée", use_column_width=True)

    # # Graphiques
    # st.subheader("Analyse des Causes")
    # cause_counts = df["Cause"].value_counts()
    # st.bar_chart(cause_counts)

    # Ajout de nouvelles anomalies
    st.subheader("Ajouter une Nouvelle Anomalie")
    with st.form("nouvelle_anomalie"):
        anomalie = st.text_input("Anomalie")
        lieu = st.text_input("Lieu")
        cause = st.text_input("Cause")
        consequence = st.text_area("Conséquence")
        action = st.text_area("Action prise")
        submitted = st.form_submit_button("Soumettre")
        if submitted:
            st.success("Nouvelle anomalie ajoutée avec succès !")