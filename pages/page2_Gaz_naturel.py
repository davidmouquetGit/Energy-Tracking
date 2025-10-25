import streamlit as st

st.set_page_config(page_title="Consommation gaz")

st.markdown("# Gaz naturel")
st.sidebar.header(" Gaz naturel")
st.write("Visualisation de la consommation de gaz naturel")


tabd, tabm = st.tabs(["Consommation Jour", "Consommation Mois"])


data_gaz_jour = st.session_state["data_gaz_jour"]
data_gaz_mois = st.session_state["data_gaz_mois"]
modele_gaz_mois = st.session_state["modele_gaz_mois"]

with tabd:
    

    try:
        
        import plotly.express as px

        

        #data_gaz_jour = get_conso_jour_data()
        fig = px.line(data_gaz_jour, 
                    x=data_gaz_jour.index, 
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
        import numpy as np
        import plotly.graph_objects as go

        error_y = dict(
        type='data',
        symmetric=False,
        array = modele_gaz_mois["upper"] - modele_gaz_mois["value"],  # distance au-dessus
        arrayminus = modele_gaz_mois["value"] - modele_gaz_mois["lower"],  # distance en dessous
        thickness=1.5,
        width=3,
        color='rgba(0,0,0,0.6)')


        # --- Création du graphique ---
        fig = go.Figure()

        # Série 1 avec barres d’erreur
        fig.add_trace(go.Bar(
            x=modele_gaz_mois.index,
            y=modele_gaz_mois["value"],
            name="Modèle avec incertitude",
            error_y=error_y,
            marker_color='lightgray'
        ))

        # Série 2 simple
        fig.add_trace(go.Bar(
            x=data_gaz_mois.index,
            y=data_gaz_mois.values,
            name="Consommation mensuelle",
            marker_color="#b4801f"
        ))

        # --- Mise en forme ---
        fig.update_layout(
            title="Consommations mensuelles gaz",
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

