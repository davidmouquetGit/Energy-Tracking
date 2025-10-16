import streamlit as st
import time
import numpy as np
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
import os
# Charger le fichier .env
load_dotenv()


st.set_page_config(page_title="Consommation d'électricité")

st.markdown("# Electricité")
st.sidebar.header(" Electricité")
#st.write("Visualisation de la consommation d'électricité")


tabh, tabd, tabm = st.tabs(["Courbe de charge horaire", "Consommation Jour", "Consommation Mois"])




@st.cache_data
def get_conso_horaire_data():
   
    DB_URL = os.getenv("DB_URL")
    engine = create_engine(DB_URL)
    # Lire un DataFrame
    df = pd.read_sql("SELECT timestamp, value FROM courbecharge", engine)
    df.index = df['timestamp']

    return df



@st.cache_data
def get_conso_jour_data():
   
    DB_URL = os.getenv("DB_URL")
    engine = create_engine(DB_URL)
    # Lire un DataFrame
    df = pd.read_sql("SELECT timestamp, conso_kwh FROM consojour", engine)
    df.index = df['timestamp']

    return df



with tabh:

    try:
        
        import plotly.express as px

        
        #st.header("Courbe de charge horaire")
        #st.line_chart(data["value"])

        data_horaire = get_conso_horaire_data()
        #st.header("Série temporelle avec Plotly")
        fig = px.line(data_horaire, 
                    x=data_horaire.index, 
                    y="value")    

        fig.update_layout(
            title="Consommation électrique horaire",
            xaxis_title="",
            yaxis_title="Consommation (W)",
        width=1000,  # Largeur en pixels
        height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    except:
        st.error(
            """
            **Erreur lors de la connexion à postgresql**
            Connection error
        """)

with tabd:
    st.header("Consommations journalières")
    data_jour = get_conso_jour_data()
    data_jour

with tabm:
    st.header("Consommations mensuelles")