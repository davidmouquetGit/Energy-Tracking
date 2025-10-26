import streamlit as st
from dotenv import load_dotenv
import pandas as pd
# Charger le fichier .env
import plotly.graph_objects as go
from datetime import datetime, timedelta

load_dotenv()


st.set_page_config(page_title="Consommation d'électricité")

st.markdown("# Electricité")
st.sidebar.header(" Electricité")
#st.write("Visualisation de la consommation d'électricité")


tabh, tabd, tabm = st.tabs(["Courbe de charge horaire", "Consommation Jour", "Consommation Mois"])


data_elec_heure = st.session_state["data_elec_heure"]
data_elec_jour  = st.session_state["data_elec_jour"]
data_elec_mois  = st.session_state["data_elec_mois"]
modele_elec_mois = st.session_state["modele_elec_mois"]


with tabh:

    st.markdown("##### Consommation électrique horaire")

    try:
        
        import plotly.express as px

    
        fig = px.line(data_elec_heure, 
                    x=data_elec_heure.index, 
                    y="value")    

        fig.update_layout(
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

    st.markdown("##### Profil horaire pour chaque jour de la semaine sur une période définie")

    from datetime import date
    # --- Définition de la plage totale ---
    min_date = data_elec_heure.index.min().date()
    max_date = data_elec_heure.index.max().date()

    # --- Slider avec plage initiale ---
    selected_range = st.slider(
        "Choisissez une période (au moins 7 jours) :",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="DD/MM/YYYY"
    )

    start_date, end_date = selected_range


    # --- Vérifie la contrainte (au moins 7 jours) ---
    if (end_date - start_date).days < 7:
        st.error("La période doit contenir **au moins 7 jours**.")
        st.stop()

    # --- Fonction de calcul des profils horaire moyens par jour de la semaine ---
    @st.cache_data
    def compute_profils(start_date, end_date):
        
        df = data_elec_heure[(data_elec_heure.index>=pd.to_datetime(start_date)) & (data_elec_heure.index<=pd.to_datetime(end_date))]        
        df = df['value'].resample("1h").mean().to_frame()
        # 1. Extraire le jour de la semaine et l'heure
        df['jour_semaine'] = df.index.day_name()  # ou df.index.dayofweek pour un entier (0=lundi, 6=dimanche)
        df['heure'] = df.index.hour

        # 2. Grouper par jour de la semaine et par heure, puis calculer la moyenne
        moyennes = df.groupby(['jour_semaine', 'heure'])['value'].mean().reset_index()

        # 3. Pivoter pour obtenir les jours en index et les heures en colonnes
        resultat = moyennes.pivot(index='jour_semaine', columns='heure', values='value')
        jours_ordre = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        resultat = resultat.reindex(jours_ordre)
        # On renomme les noms des jours en français
        resultat.index = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']


        return resultat


    df_profils_horaire_hebdo = compute_profils(start_date, end_date)


    # Liste des labels pour les heures (0h, 1h, ..., 23h)
    heures_labels = [f"{h}h" for h in range(24)]

    heatmap = go.Figure(data=go.Heatmap(
            z=df_profils_horaire_hebdo.values,
            x=heures_labels,  # Utilise les labels personnalisés pour l'axe X
            y=df_profils_horaire_hebdo.index.to_list(),
            colorscale='Viridis',
            colorbar=dict(
                title="W"  # Ajoute l'unité "W" à la barre de couleur
            )
    ))

   

    st.plotly_chart(heatmap, use_container_width=True)





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
        import numpy as np
        import plotly.graph_objects as go

        error_y = dict(
        type='data',
        symmetric=False,
        array = modele_elec_mois["upper"] - modele_elec_mois["value"],  # distance au-dessus
        arrayminus = modele_elec_mois["value"] - modele_elec_mois["lower"],  # distance en dessous
        thickness=1.5,
        width=3,
        color='rgba(0,0,0,0.6)')


        # --- Création du graphique ---
        fig = go.Figure()

        # Série 1 avec barres d’erreur
        fig.add_trace(go.Bar(
            x=modele_elec_mois.index,
            y=modele_elec_mois["value"],
            name="Modèle avec incertitude",
            error_y=error_y,
            marker_color='lightgray'
        ))

        # Série 2 simple
        fig.add_trace(go.Bar(
            x=data_elec_mois.index,
            y=data_elec_mois.values,
            name="Consommation mensuelle",
            marker_color='dodgerblue'
        ))

        # --- Mise en forme ---
        fig.update_layout(
            title="Consommations mensuelles d’électricité",
            xaxis_title="Mois",
            yaxis_title="Consommation (kWh)",
            barmode='group',  # groupé côte à côte
            template='plotly_white',
            hovermode='x unified',
            legend=dict(
                title=None,
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            )
        )



        st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"Erreur lors du graphe {e}")



