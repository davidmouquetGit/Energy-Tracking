import streamlit as st
import time
import numpy as np
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
import os
import io  # Nécessaire pour la création du buffer de téléchargement
# Charger le fichier .env
load_dotenv()


st.set_page_config(page_title="Consommation d'électricité")

st.markdown("# Electricité")
st.sidebar.header(" Electricité")
#st.write("Visualisation de la consommation d'électricité")


tabh, tabd, tabm = st.tabs(["Courbe de charge horaire", "Consommation Jour", "Consommation Mois"])


data_elec_heure = st.session_state["data_elec_heure"]
data_elec_jour  = st.session_state["data_elec_jour"]
data_elec_mois  = st.session_state["data_elec_mois"]



with tabh:

    try:
        
        import plotly.express as px

    
        fig = px.line(data_elec_heure, 
                    x=data_elec_heure.index, 
                    y="value")    

        fig.update_layout(
            title="Consommation électrique horaire",
            xaxis_title="",
            yaxis_title="Consommation (W)",
        width=1000,  # Largeur en pixels
        height=500)
        st.plotly_chart(fig, use_container_width=True)

         # Ajout des boutons de téléchargement
        col1, col2 = st.columns(2)
        with col1:
            buffer_csv = io.BytesIO()
            data_elec_heure.to_csv(buffer_csv, index=True)
            buffer_csv.seek(0)
            st.download_button(
                label="💾 Télécharger en CSV",
                data=buffer_csv,
                file_name="conso_horaire.csv",
                mime="text/csv"
            )
        with col2:
            buffer_excel = io.BytesIO()
            data_elec_heure.to_excel(buffer_excel, index=True)
            buffer_excel.seek(0)
            st.download_button(
                label="💾 Télécharger en Excel",
                data=buffer_excel,
                file_name="conso_horaire.xlsx",
                mime="application/vnd.ms-excel"
            )
    
    except:
        st.error(
            """
            **Erreur lors de la connexion à postgresql**
            Connection error
        """)

with tabd:
    

    try:
        
        import plotly.express as px

        

        #data_elec_jour = get_conso_jour_data()
        fig = px.line(data_elec_jour, 
                    x=data_elec_jour.index, 
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
        fig = px.bar(data_elec_mois,
                    x=data_elec_mois.index,
                    y=data_elec_mois.values,
                    title='Consommation mensuelle',
                    #labels={'Consommation': 'Consommation (kWh)', 'Date': 'Mois'},
                    color_discrete_sequence=['#1f77b4'])

        # Personnalisation de l'affichage des dates
        fig.update_xaxes(
            tickformat='%b %Y',  # Affiche le mois et l'année
            tickangle=45,        # Incline les étiquettes pour une meilleure lisibilité
            dtick='M1'           # Affiche une étiquette par mois
        )

        fig.update_layout(
            title="Consommation électrique mensuelle ",
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



