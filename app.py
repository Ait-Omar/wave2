import streamlit as st
import pandas as pd
from PIL import Image
import base64
from io import BytesIO
import plotly.express as px
import json
from datetime import datetime
import numpy as np






def image_to_base64(image_path):
    img = Image.open(image_path)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

logo_path1 = "static/logo.png"  
logo_base641 = image_to_base64(logo_path1)


st.sidebar.markdown(
    f"""
    <div style="text-align: center; padding-bottom: 5px;padding-top: 5px;">
        <img src="data:image/png;base64,{logo_base641}" alt="Logo" width="250">
    </div>
    """, 
    unsafe_allow_html=True
)


st.markdown(f"<h1 style='text-align: center'>Wave2</h1>", unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader("Charger les données laboratoires", type=["xlsx", "xls"])

#---------------------------------------------Chargement des données-----------------------------------------------------
if uploaded_file is None:
    st.sidebar.info("Upload a file through config")
    st.stop()

st.sidebar.markdown("<p style='text-align: center;'>Fichier téléchargé avec succès!</p>",unsafe_allow_html=True)
sheets =["SELF CLEANING","UF","RO-A","RO-B","RO-C","RO-D","PRODUCTION"]
data = {}
for sheet in sheets:
        data[sheet] = pd.read_excel(uploaded_file,sheet_name=sheet)
don = st.sidebar.radio('Phases de traitement:',
                                    [
                                        "SELF CLEANING",
                                        "UF",
                                        "RO-A",
                                        "RO-B",
                                        "RO-C",
                                        "RO-D",
                                        "PRODUCTION"
                                        ])  
df = pd.read_excel(uploaded_file,sheet_name=don)

df['date'] = pd.to_datetime(df['date'])
df['date'] = df['date'].dt.strftime('%d/%m/%Y')  # Format to 'dd/mm/yyyy'

# Start and end dates for filtering (convert back to datetime)
startDate = pd.to_datetime(df["date"], format='%d/%m/%Y').min()
endDate = pd.to_datetime(df["date"], format='%d/%m/%Y').max()

col1, col2 = st.columns((2))
with col1:
    date1 = pd.to_datetime(st.sidebar.date_input("Start Date", startDate))
with col2:
    date2 = pd.to_datetime(st.sidebar.date_input("End Date", endDate))

# Convert back to datetime for filtering
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
df = df[(df["date"] >= date1) & (df["date"] <= date2)]

# Convert back to formatted string for display
df['date'] = df['date'].dt.strftime('%d/%m/%Y')

# Reset index before displaying the table
# df_filtered = df.reset_index(drop=False)
# df = df_filtered[df_filtered['poste']=="p1"]
# Display the table without index
st.table(df)



param = st.sidebar.selectbox(f'ordonnée', df.columns[2:]) 
st.markdown(f"<h2 style='text-align: center;'>{param}: {np.around(df[param].mean(),2)}</h2>", unsafe_allow_html=True)        
fig = px.line(df,x="date",y=param,color='poste')
st.plotly_chart(fig,use_container_width=True,height = 200)

