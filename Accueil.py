
import streamlit as st
import pandas as pd
from PIL import Image
import base64
from io import BytesIO
import plotly.express as px
import json
from datetime import datetime
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Station de Dessalement Wave 2 - Jorf Lasfar", 
    page_icon="🌊", 
    layout="wide"
)

# Fonction pour convertir une image en base64
def image_to_base64(image_path):
    img = Image.open(image_path)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

# Charger le logo
logo_path1 = "static/logo.png"  
logo_base641 = image_to_base64(logo_path1)

# CSS pour ajouter des animations et un design personnalisé
st.markdown(
    """
    <style>
        body {
            background-color: #f7f9fc;
        }
        h1 {
            font-family: 'Arial', sans-serif;
            color: #2c3e50;
            font-size: 48px;
            animation: fadeIn 2s ease-in-out;
        }
        h2, h3 {
            font-family: 'Arial', sans-serif;
            color: #34495e;
            animation: slideIn 1s ease-in-out;
        }
        .footer {
            font-size: 14px;
            color: #7f8c8d;
            text-align: center;
            padding-top: 40px;
            padding-bottom: 20px;
        }
        .logo-container {
            text-align: center;
            animation: scaleIn 2s ease-in-out;
        }
        .description {
            font-size: 18px;
            line-height: 1.6;
            color: #2c3e50;
            margin-bottom: 30px;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes slideIn {
            from { transform: translateX(-50px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes scaleIn {
            from { transform: scale(0.8); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }
        .button-container {
            text-align: center;
            margin-top: 20px;
        }
        .stButton button {
            background-color: #2980b9;
            color: white;
            border: none;
            font-size: 16px;
            padding: 10px 20px;
            border-radius: 8px;
            transition: all 0.3s ease-in-out;
        }
        .stButton button:hover {
            background-color: #1abc9c;
            transform: translateY(-2px);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Titre principal
st.markdown(f"<h1 style='text-align: center;'>Station de Dessalement Wave 2 - Jorf Lasfar</h1>", unsafe_allow_html=True)

# Logo avec animation
st.markdown(
    f"""
    <div class="logo-container">
        <img src="data:image/png;base64,{logo_base641}" alt="Logo" width="200">
    </div>
    """,
    unsafe_allow_html=True
)

# Sous-titre
st.markdown("<h2 style='text-align: center;'>Bienvenue sur l'interface dédiée à la station de dessalement Wave 2</h2>", unsafe_allow_html=True)

# Description
st.markdown(
    """
    <div class="description">
        <p>La station de dessalement Wave 2 de Jorf Lasfar est une infrastructure essentielle pour répondre 
        aux besoins croissants en eau potable et industrielle au Maroc. Ce projet utilise des technologies 
        innovantes pour offrir une production durable et efficace.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Points clés
st.markdown(
    """
    <h3>🚀 Ce que vous trouverez sur cette interface :</h3>
    <ul>
        <li>Suivi en temps réel des performances opérationnelles (débits, consommation énergétique, etc.).</li>
        <li>Données historiques et analyses pour comprendre les tendances de production.</li>
        <li>Documentation technique pour explorer les spécifications des équipements et des processus.</li>
    </ul>
    """,
    unsafe_allow_html=True
)

# Objectifs de la station
st.markdown(
    """
    <h3>🌍 Mission de Wave 2</h3>
    <p>- Fournir une solution durable au stress hydrique dans la région.</p>
    <p>- Répondre aux besoins en eau potable des zones avoisinantes, notamment Casablanca et El Jadida.</p>
    <p>- Minimiser l'impact environnemental grâce à des technologies avancées.</p>
    """,
    unsafe_allow_html=True
)



# Footer
st.markdown(
    """
    <div class="footer">
        © 2025 Station de Dessalement Wave 2 - Jorf Lasfar | Interface développée par DIPS
    </div>
    """,
    unsafe_allow_html=True
)


