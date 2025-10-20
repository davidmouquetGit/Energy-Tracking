import streamlit as st
import time
import numpy as np
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
import os
st.set_page_config(page_title="Consommation gaz")

st.markdown("# Gaz naturel")
st.sidebar.header(" Gaz naturel")
st.write("Visualisation de la consommation de gaz naturel")


tabd, tabm = st.tabs(["Consommation Jour", "Consommation Mois"])





@st.cache_data
def get_conso_jour_data():
   
    DB_URL = os.getenv("DB_URL")
    engine = create_engine(DB_URL)
    # Lire un DataFrame
    df = pd.read_sql("SELECT horodatage, energie FROM conso_jour_gaz", engine)
    df.index = df['horodatage']

    return df

data_jour = get_conso_jour_data()
data_mois = data_jour['energie'].resample("1M").sum()


with tabd:
    

    try:
        
        import plotly.express as px

        

        #data_jour = get_conso_jour_data()
        fig = px.line(data_jour, 
                    x=data_jour.index, 
                    y="energie")    
        fig.update_traces(line_color="#b4801f")

        fig.update_layout(
            title="Consommation gaz journalière ",
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
                    title='Consommation gaz mensuelle',
                    #labels={'Consommation': 'Consommation (kWh)', 'Date': 'Mois'},
                    color_discrete_sequence=["#b4801f"])

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


