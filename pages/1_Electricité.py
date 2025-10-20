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
    df = pd.read_sql("SELECT horodatage, value FROM conso_heure_elec", engine)
    df.index = df['horodatage']

    return df



@st.cache_data
def get_conso_jour_data():
   
    DB_URL = os.getenv("DB_URL")
    engine = create_engine(DB_URL)
    # Lire un DataFrame
    df = pd.read_sql("SELECT horodatage, value FROM conso_jour_elec", engine)
    df.index = df['horodatage']

    return df

data_jour = get_conso_jour_data()
data_mois = data_jour['value'].resample("1M").sum()

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
    

    try:
        
        import plotly.express as px

        

        #data_jour = get_conso_jour_data()
        fig = px.line(data_jour, 
                    x=data_jour.index, 
                    y="value")    

        fig.update_layout(
            title="Consommation électrique journalière ",
            xaxis_title="",
            yaxis_title="Consommation (kWh)",
        width=1000,  # Largeur en pixels
        height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    except:
        st.error(
            """
            **Erreur lors de la connexion à postgresql**
            Connection error
        """)


with tabm:
    

    try:
        
        import pandas as pd
        import plotly.express as px


        # Création du graphique en barres
        fig = px.bar(data_mois,
                    x=data_mois.index,
                    y=data_mois.values,
                    title='Consommation mensuelle',
                    #labels={'Consommation': 'Consommation (kWh)', 'Date': 'Mois'},
                    color_discrete_sequence=['#1f77b4'])

        # Personnalisation de l'affichage des dates
        fig.update_xaxes(
            tickformat='%b %Y',  # Affiche le mois et l'année
            tickangle=45,        # Incline les étiquettes pour une meilleure lisibilité
            dtick='M1'           # Affiche une étiquette par mois
        )


        st.plotly_chart(fig, use_container_width=True)
    
    except:
        st.error(
            """
            **Erreur lors de la connexion à postgresql**
            Connection error
        """)



