import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from PIL import Image
from datetime import datetime
import base64
import os
import openpyxl
from openpyxl.drawing.image import Image as XLImage
import matplotlib.pyplot as plt
import ezdxf
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re





def visualise(df,params):
    df.replace([
        'wbw','soak ceb1','w-f','f','F','w-bw','WBW','W.BW','W,BW',
        'ceb1','CEB2','bw','wf','wb','Wf','bW','W BW',
        'W-F','W.F','hs','WF','wB','BW','w,b','W,F','W-BW','ceb2',
        'SOAK CEB1','W,B','CEB1','SOAK CEB2','HS'
    ], np.nan, inplace=True)
    
    # Création d'une colonne de date combinée
    df['Date'] = df['date'].astype(str) + " " + df['poste'].astype(str)
    
    for param in params:
        # Conteneur de titre stylisé
        # st.markdown(
        #     f"""
        #     <div style="
        #         background-color: #F9F9F9; 
        #         border: 1px solid #D1D1D1; 
        #         border-radius: 8px; 
        #         padding: 20px; 
        #         margin: 0 auto 20px auto; 
        #         box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1); 
        #         width: 60%;
        #         max-width: 800px;
        #     ">
        #         <h2 style="
        #             text-align: center; 
        #             color: #4A90E2; 
        #             font-family: Arial, sans-serif; 
        #             margin-bottom: 0;
        #         ">
        #             {param.capitalize()} Journalièr: {np.around(df[param].dropna().iloc[-1], 2)}
        #         </h2>
        #     </div>
        #     """, 
        #     unsafe_allow_html=True
        # )

        # Graphique d’évolution temporelle
        fig_line = px.line(
            df,
            x="Date",
            y=param,
            title=f"Évolution de {param.capitalize()} au fil du temps",
            labels={"Date": "Date", param: param.capitalize()},
            template="plotly_white",
        )
        fig_line.update_layout(
            title=dict(text=f"Évolution de {param.capitalize()}", font=dict(size=20), x=0.5, xanchor="center"),
            xaxis=dict(title_text="Date", tickangle=-45, showticklabels=False),
            yaxis=dict(title_text=param.capitalize()),
            margin=dict(l=50, r=50, t=60, b=40),
            height=400,
        )
        st.plotly_chart(fig_line, use_container_width=True)

   
#     df.replace(['wbw','soak ceb1','w-f','f','F','w-bw','WBW','W.BW','W,BW','ceb1','CEB2','bw','wf','wb','W-F','W.F','hs','WF','wB','BW','w,b','W,F','W-BW','ceb2','SOAK CEB1','W,B','CEB1','SOAK CEB2','HS',
#                 ], 
#                np.nan, inplace=True)
#     df['Date'] = df['date'].astype(str) + " " + df['poste'].astype(str)
   

#     # Conteneur professionnel avec largeur personnalisée
#     st.markdown(
#         f"""
#         <div style="
#             background-color: #F9F9F9; 
#             border: 1px solid #D1D1D1; 
#             border-radius: 8px; 
#             padding: 20px; 
#             margin: 0 auto 20px auto; 
#             box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1); 
#             width: 60%; /* Ajustez ce pourcentage selon vos besoins */
#             max-width: 800px; /* Largeur maximale pour éviter une trop grande expansion */
#         ">
#             <h2 style="
#                 text-align: center; 
#                 color: #4A90E2; 
#                 font-family: Arial, sans-serif; 
#                 margin-bottom: 0;
#             ">
#                 {param.capitalize()} Journalièr: {np.around(df[param].iloc[-1], 2)} 
#             </h2>
#         </div>
#         """, 
#         unsafe_allow_html=True
#     )



#     # Personnalisation du graphique avec un style moderne
#     fig = px.line(
#         df,
#         x="Date",
#         y=param,
#         title=f"Évolution de {param.capitalize()} au fil du temps",
#         labels={
#             "Date": "Date",
#             param: param.capitalize()
#         },
#         template="plotly_white",  # Thème moderne
#     )
#     fig.update_layout(
#     title=dict(
#         text=f"Évolution de {param.capitalize()}",
#         font=dict(size=20),
#         x=0.5,
#         xanchor="center"
#     ),
#     xaxis=dict(
#         title_text="Date",
#         tickangle=-45,
#         showticklabels=False  # This hides the date labels on the x-axis
#     ),
#     yaxis=dict(title_text=f"{param.capitalize()}"),
#     margin=dict(l=50, r=50, t=60, b=40),
#     height=400,
# )


#     st.plotly_chart(fig, use_container_width=True)

def consomation(df,param):
    st.markdown(f"<h2 style='text-align: center;'>{param[:-5]} moyen: {np.around(df[param].mean(),2)}</h2>", unsafe_allow_html=True)        
    fig = px.line(df,x="date",y=param)
    st.plotly_chart(fig,use_container_width=True,height = 200)

def consomation_energie(df,param):

    st.markdown(f"<h2 style='text-align: center;'>{param}</h2>", unsafe_allow_html=True)        
    fig = px.line(df,x="Date",y=param)
    st.plotly_chart(fig,use_container_width=True,height = 200)


        # Distribution des paramètres
    param_to_analyze = st.selectbox("Sélectionnez un paramètre pour analyser sa distribution", df.columns[1:])
    fig_hist = px.histogram(df, x=param_to_analyze, title=f"Distribution de {param_to_analyze}", nbins=20)
    st.plotly_chart(fig_hist, use_container_width=True)
    if param:
        stats = df[param].describe()

        # Créer un DataFrame propre pour les statistiques descriptives
        stats_clean = pd.DataFrame({
            "Statistique": ["Moyenne", "Médiane", "Min", "Max", "Écart-type", "1er Quartile", "3e Quartile"],
            "Valeur": [
                round(stats["mean"], 2),
                round(stats["50%"], 2),
                round(stats["min"], 2),
                round(stats["max"], 2),
                round(stats["std"], 2),
                round(stats["25%"], 2),
                round(stats["75%"], 2),
            ]
        })

        # Afficher un tableau propre
        st.write(f"**Statistiques descriptives pour {param}**")
        st.table(stats_clean)

def load_data(file_path):
    # Charger les données Excel
    return pd.read_excel(file_path, sheet_name='Feuil1')

def save_data(file_path, data):
    # Sauvegarder les données dans le fichier Excel
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        data.to_excel(writer, sheet_name='Feuil1', index=False)

def save_image(uploaded_photo, anomaly_name):
  # Sauvegarder l'image téléchargée dans un dossier local
    image_folder = "images_anomalies"
    os.makedirs(image_folder, exist_ok=True)
    image_path = os.path.join(image_folder, f"{anomaly_name}.png")
    with open(image_path, "wb") as f:
        f.write(uploaded_photo.getbuffer())
    return image_path

def download_data_with_images(file_path):
    # Télécharger le fichier Excel avec les images intégrées
    with open(file_path, "rb") as file:
        return file.read()
    
def save_data_with_image(file_path, data, image_paths):
     # Sauvegarder les données dans le fichier Excel avec les images
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        data.to_excel(writer, sheet_name='Feuil1', index=False)

    # Charger le fichier avec openpyxl pour ajouter les images
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook['Feuil1']

    # Ajouter les images dans la colonne "Images"
    for idx, img_path in enumerate(image_paths, start=2):  # Démarre à la 2ème ligne
        if img_path:
            img = XLImage(img_path)
            img.width, img.height = 100, 100  # Redimensionner l'image
            sheet.add_image(img, f"K{idx}")  # Ajouter l'image dans la colonne K

    workbook.save(file_path)

def anomali(data,data_file):

    st.title("Suivi des Anomalies Journalières")

    # Affichage des données brutes
    # st.subheader("Tableau des Anomalies")
    # st.dataframe(data)

    # Filtrage des données
    st.subheader("Filtrer les Anomalies")

    # Options de filtrage
    lieux = data['Emplacement'].unique()
    statut = data['Statut '].unique()
    Type = data['Type'].unique()
    col1, col2, col3 = st.columns(3)
    with col1:
        lieu_filtre = st.selectbox("Filtrer par lieu :", ["Tous"] + list(lieux))
    with col2:
        statut_options = st.selectbox("Filtrer par statut", ["Tous"] + list(statut))
    with col3:
        type_filtre = st.selectbox("Filtrer par type :", ["Tous"] + list(Type))

    if ((lieu_filtre != "Tous") and (statut_options != "Tous") and (type_filtre != "Tous")):
        filtered_data = data[(data["Emplacement"] == lieu_filtre) & (data['Statut '] == statut_options) & (data['Type'] == type_filtre)]
    elif lieu_filtre != "Tous":
        filtered_data = data[data["Emplacement"] == lieu_filtre]
    elif statut_options != "Tous":
        filtered_data = data[data['Statut '] == statut_options]
    elif type_filtre != "Tous":
        filtered_data = data[data['Type'] == type_filtre]
    else:
        filtered_data = data

    st.write("Anomalies après filtrage :", len(filtered_data))
    st.dataframe(filtered_data)
     
    st.subheader("Analyse des Anomalies")
    statut_counts = filtered_data['Statut '].value_counts()
    st.bar_chart(statut_counts)

    # Graphique circulaire pour la répartition des anomalies par type
    st.subheader("Répartition des Anomalies par Type")
    if not filtered_data.empty:
        type_counts = filtered_data['Type'].value_counts().reset_index()
        type_counts.columns = ['Type', 'Nombre']
        fig = px.pie(type_counts, names='Type', values='Nombre', title='Répartition des Anomalies par Type')
        fig.update_traces(textinfo='percent+label', showlegend=True)
        fig.update_layout(showlegend=True, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée à afficher pour ce filtre.")


    # Résumé Dynamique
    st.subheader("Résumé Dynamique des Anomalies")
    col1, col2, col3 = st.columns(3)

    # Total des anomalies
    total_anomalies = len(filtered_data)
    with col1:
        st.metric(label="Total Anomalies", value=total_anomalies)

    # Anomalies résolues
    resolved_anomalies = len(filtered_data[filtered_data['Statut '] == "Réalisée"])
    with col2:
        st.metric(label="Résolues", value=resolved_anomalies)

    # Pourcentage résolu
    resolved_percentage = (resolved_anomalies / total_anomalies * 100) if total_anomalies > 0 else 0
    with col3:
        st.metric(label="Pourcentage Résolu", value=f"{resolved_percentage:.1f}%")

    # Tendance des anomalies dans le temps
    st.subheader("Tendance des Anomalies dans le Temps")
    if 'Date' in filtered_data.columns:
        filtered_data['Date'] = pd.to_datetime(filtered_data['Date'])
        trend_data = filtered_data.groupby('Date').size()
        st.line_chart(trend_data)
    else:
        st.info("Les données ne contiennent pas de colonne 'Date d'ajout'.")




    # Photos (exemple avec image fictive)
    # st.subheader("Photos des Anomalies")
    # uploaded_photo = st.file_uploader("Télécharger une photo de l'anomalie :", type=["jpg", "png"])
    # if uploaded_photo:
    #     img = Image.open(uploaded_photo)
    #     st.image(img, caption="Photo téléchargée", use_column_width=True)


    # Ajout de nouvelles anomalies
    st.subheader("Ajouter une Nouvelle Anomalie")
    with st.form("nouvelle_anomalie"):
        anomalie = st.text_input("Anomalie")
        emplacement = st.text_input("Emplacement")
        cause = st.text_input("Cause")
        consequence = st.text_area("Conséquence")
        action = st.text_area("Action prise")
        type_anomalie = st.text_input("Type")
        responsable = st.text_input("Responsable")
        date_realisation = st.date_input("Date de réalisation",value=None)
        statut = st.selectbox("Statut", options=["Non réalisée", "En cours", "Réalisée"])
        commentaire = st.text_area("Commentaire")
        uploaded_photo = st.file_uploader("Télécharger une photo de l'anomalie :", type=["jpg", "png"])
        submitted = st.form_submit_button("Soumettre")

        if submitted:
            image_path = None
            if uploaded_photo:
             image_path = save_image(uploaded_photo, anomalie)
            new_entry = {
                "Date": datetime.now().date(),
                "Anomalies": anomalie,
                "Emplacement": emplacement,
                "Cause": cause,
                "Conséquence": consequence,
                "Actions à entreprendre": action,
                "Type": type_anomalie,
                "Responsable": responsable,
                "Date de réalisation": date_realisation,
                "Statut ": statut,
                "Commentaire": commentaire,
                "Image Path": image_path
            }
            data = pd.concat([data, pd.DataFrame([new_entry])], ignore_index=True)
            save_data_with_image(data_file, data, [image_path])
            st.success("Nouvelle anomalie ajoutée avec succès et enregistrée dans le fichier Excel !")
    st.subheader("Télécharger le fichier modifié")
    file_data = download_data_with_images(data_file)
    st.download_button(
        label="Télécharger le fichier",
        data=file_data,
        file_name="anomalies_modifiees.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def laboratoir(df,param,don):
  
    # df['Date'] = df['date'].astype(str)
    df[param] = df[param].astype(str).str.replace(',', '.')
    df.replace(['-'], np.nan, inplace=True)
    df[param] = pd.to_numeric(df[param], errors='coerce')
    df['Date'] = df['date'].astype(str) + " " + df['poste'].astype(str)
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
    # if param == "Conductivité(µS/cm)":
    #     fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
    #     fig.add_annotation(
    #                     x=df['date'].iloc[-1], 
    #                     y=450, 
    #                     text="la Conductivité(µS/cm) doit être inférieur ou égale à 450",  
    #                     showarrow=True, 
    #                     arrowhead=2,  
    #                     ax=0, 
    #                     ay=-40  
    #                 )
    # if param == "Cl2":
    #     fig.add_hline(y=0.1, line_dash="dash", line_color="red", line_width=2)
    #     fig.add_annotation(
    #                     x=df['date'].iloc[-1], 
    #                     y=0.1, 
    #                     text="Cl2 doit être inférieur ou égale à 0.1",  
    #                     showarrow=True, 
    #                     arrowhead=2,  
    #                     ax=0, 
    #                     ay=-40  
    #                 )
    # if param == "ORP(mV)":
    #     fig.add_hline(y=250, line_dash="dash", line_color="red", line_width=2)
    #     fig.add_hline(y=300, line_dash="dash", line_color="red", line_width=2)
    #     fig.add_annotation(
    #             x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
    #             y=250,  # Position Y (sur la ligne horizontale à 250)
    #             text="Min: 250 mV",  # Texte de l'annotation
    #             showarrow=True,  # Afficher une flèche pointant vers le point
    #             arrowhead=2,  # Type de flèche
    #             ax=0,  # Position X de la flèche par rapport au texte
    #             ay=-40  # Position Y de la flèche par rapport au texte
    #         )
    # if (param == "pH" and don =="UF FEED"):
    #     fig.add_hline(y=6.5, line_dash="dash", line_color="red", line_width=2)
    #     fig.add_hline(y=8.5, line_dash="dash", line_color="red", line_width=2)
    #     fig.add_annotation(
    #             x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
    #             y=6.5,  # Position Y (sur la ligne horizontale à 250)
    #             text="Min: 6.5",  # Texte de l'annotation
    #             showarrow=True,  # Afficher une flèche pointant vers le point
    #             arrowhead=2,  # Type de flèche
    #             ax=0,  # Position X de la flèche par rapport au texte
    #             ay=-40  # Position Y de la flèche par rapport au texte
    #         )
    # if "SDI" in param:
    #     fig.add_hline(y=3, line_dash="dash", line_color="red", line_width=2)
    #     fig.add_annotation(
    #                     x=df['date'].iloc[-1], 
    #                     y=3, 
    #                     text="SDI15  doit être inférieur ou égale à 3",  
    #                     showarrow=True, 
    #                     arrowhead=2,  
    #                     ax=0, 
    #                     ay=-40  
    #                 )
    # if (param == "NTU" and don =="UF FEED"):
    #     fig.add_hline(y=0.1, line_dash="dash", line_color="red", line_width=2)
    #     fig.add_annotation(
    #                     x=df['date'].iloc[-1], 
    #                     y=0.1, 
    #                     text="NTU doit être inférieur ou égale à 0.1",  
    #                     showarrow=True, 
    #                     arrowhead=2,  
    #                     ax=0, 
    #                     ay=-40  
    #                 )


    st.plotly_chart(fig, use_container_width=True)

def labo_oper(d1,d2,phase1,phase2,x,y):
    df = pd.DataFrame({'date':d2[phase2]['date'],x:d1[phase1][x],y:d2[phase2][y]})
    
    df.replace(0, np.nan, inplace=True)
    df.replace('/', np.nan, inplace=True)
    df.replace('-', np.nan, inplace=True)
    df.replace('CIP', np.nan, inplace=True)
    df.replace('erroné', np.nan, inplace=True)
    df.replace('en cours', np.nan, inplace=True)
    

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=df['date'], y=df[df.columns[1]], name=df.columns[1],line=dict(color='#095DBA', width=2)),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df['date'], y=df[df.columns[2]], name=df.columns[2],line=dict(color='#FF4B4A', width=2),),
        secondary_y=True,
    )

    fig.update_layout(
        title_text=f"Corellation entre {df.columns[1][:4]} et {df.columns[2][:4]}",
        title_x=0.3,
        height=600
    )

    fig.update_xaxes(title_text="Date")

    fig.update_yaxes(title_text=x, secondary_y=False)
    fig.update_yaxes(title_text=y, secondary_y=True)

    st.plotly_chart(fig, use_container_width=True)

def transform_laboratory_data(file_path, sheet_name=None):
    """
    Transforme une ou toutes les feuilles Excel de laboratoire :
    - Détection dynamique des paramètres
    - Conversion P1/P2/P3 → format long
    - Ajout des heures de poste
    - Tri par date/poste
    - Colonnes renommées par feuille
    """

    excel_file = pd.ExcelFile(file_path)
    sheet_names = [sheet_name] if sheet_name else excel_file.sheet_names

    def transform_one_sheet(sheet):
        df = pd.read_excel(file_path, sheet_name=sheet)

        # Nettoyage des colonnes
        df.columns = df.columns.str.replace(r'\n.*', '', regex=True)
        df.columns = df.columns.str.replace(r'\s+', ' ', regex=True).str.strip()

        # Détection automatique des paramètres (ex: 'T (°C)-P1', 'Ph-P2', etc.)
        param_pattern = re.compile(r"(.+)-P[1-3]")
        detected_params = set()
        for col in df.columns:
            match = param_pattern.match(col)
            if match:
                param_name = match.group(1).strip()
                detected_params.add(param_name)

        # Nettoyage : création des bons noms 'param-Pi'
        rename_dict = {}
        for param in detected_params:
            for i in range(1, 4):
                possible_names = [col for col in df.columns if f"{param}-P{i}" in col or f"{param} (mv)-P{i}" in col or f"{param} (mg/l)-P{i}" in col]
                if possible_names:
                    rename_dict[possible_names[0]] = f"{param}-P{i}"

        df.rename(columns=rename_dict, inplace=True)

        # Création des sous-dataframes par point (P1, P2, P3)
        dfs = []
        for i in range(1, 4):
            cols = ['date'] + [f"{param}-P{i}" for param in detected_params if f"{param}-P{i}" in df.columns]
            if len(cols) > 1:
                sub_df = df[cols].copy()
                sub_df['point'] = f'P{i}'
                param_cols = [col.split('-')[0] for col in cols[1:]]
                renamed_cols = [f"{param}_{sheet}" for param in param_cols]
                sub_df.columns = ['date'] + renamed_cols + ['point']
                sub_df['source'] = sheet
                dfs.append(sub_df)

        result = pd.concat(dfs, ignore_index=True)

        # Ajouter les horaires de poste
        poste_mapping = {'P1': '02:00:00', 'P2': '10:00:00', 'P3': '18:00:00'}
        result['poste'] = result['point'].map(poste_mapping)

        return result

    # Fusion de toutes les feuilles sélectionnées
    combined_df = pd.concat([transform_one_sheet(sheet) for sheet in sheet_names], ignore_index=True)

    # Format & tri
    combined_df['poste'] = pd.to_datetime(combined_df['poste'], format='%H:%M:%S').dt.time
    combined_df['date'] = pd.to_datetime(combined_df['date'], errors='coerce')
    combined_df.sort_values(by=['date', 'poste'], inplace=True)
    combined_df.reset_index(drop=True, inplace=True)

    # Colonnes : date, poste, puis tout le reste
    cols_order = ['date', 'poste'] + [col for col in combined_df.columns if col not in ['date', 'poste']]
    return combined_df[cols_order]

