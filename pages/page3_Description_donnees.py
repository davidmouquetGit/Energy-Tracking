import streamlit as st
import plotly.express as px
import pandas as pd


data_elec_heure = st.session_state["data_elec_heure"]
data_elec_jour  = st.session_state["data_elec_jour"]
data_elec_mois  = st.session_state["data_elec_mois"]
data_gaz_jour   = st.session_state["data_gaz_jour"]
data_gaz_mois   = st.session_state["data_gaz_mois"]
data_meteo_jour = st.session_state["data_meteo_jour"]
data_meteo_jour["text"] = (data_meteo_jour['temperature_2m_min'] + data_meteo_jour['temperature_2m_max'])/2.0



st.title("Analyse descriptive des données")

st.markdown(
    """
    <style>
    /* Réduire la largeur du selectbox */
    div[data-baseweb="select"] {
        width: 300px !important;
    }

    /* Enlever le centrage par défaut et aligner à gauche */
    .stSelectbox {
        margin-left: 0 !important;
    }

    /* Supprime le label Streamlit par défaut (déjà fait par label_visibility) */
    label[data-testid="stWidgetLabel"] {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Ligne avec selectbox alignée sur le premier graphe ---
col_select, col_empty = st.columns([1, 2])  # le selectbox prend 1/3 de la largeur
with col_select:
    variable = st.selectbox("Choix", options=["Consommation électrique (30 min.)", "Consommation électrique journalière", "Consommation gaz journalière", "T° extérieure"], label_visibility="collapsed")

match variable:
    case "Consommation électrique (30 min.)":
        df = st.session_state["data_elec_heure"]
        X = "value"

    case "Consommation électrique journalière":
        df = st.session_state["data_elec_jour"]
        X = "value"

    case "Consommation gaz journalière":
        df = st.session_state["data_gaz_jour"]
        X = "energie"

    case "T° extérieure":
        df = st.session_state["data_meteo_jour"]
        X = "text"            
        
        


# Calcul de la durée entre 2 pas de temps successif (pour voir si il y'a des données manquantes)

df['dt'] = df['horodatage']-df['horodatage'].shift(1)
df.dropna(inplace=True)
df['duree_heures'] = df['dt'].dt.total_seconds() / 3600

# --- Graphiques ---
fig_hist = px.histogram(df, x=X, nbins=20, title=f"Histogramme")
fig_box = px.box(df, y=X, title=f"Boxplot")

dict_map_unites = {
    "Consommation électrique (30 min.)": "W",
    "Consommation électrique journalière": "kWh",
    "Consommation gaz journalière": "kWh",
    "T° extérieure": "°C"
}



# Centrer les titres et ajouter les labels d’axes
fig_hist.update_layout(
    title_x=0.5,
    xaxis_title=dict_map_unites[variable],
    yaxis_title="nombre"
)

fig_box.update_layout(
    title_x=0.5,
    yaxis_title=dict_map_unites[variable],
    xaxis_title=None
)

### Visualisation des données manqantes

fig_missingdata = px.line(df,x=df.index,y="duree_heures")    

fig_missingdata.update_layout(
    title=f"Durée entre 2 pas de temps successif ({variable})",
    xaxis_title="",
    yaxis_title="Heure",
width=1000,  # Largeur en pixels
height=500)

# --- Graphes côte à côte ---
col1, col_space, col2 = st.columns([1, 0.15, 1])
with col1:
    st.plotly_chart(fig_hist, use_container_width=True)
with col2:
    st.plotly_chart(fig_box, use_container_width=True)
    
st.plotly_chart(fig_missingdata, use_container_width=True)




### Visualisation des périodes couvertes par les données






data_gaz_jour   = st.session_state["data_gaz_jour"] 
data_elec_jour  = st.session_state["data_elec_jour"] 
data_elec_heure = st.session_state["data_elec_heure"]  
data_meteo_jour = st.session_state["data_meteo_jour"]


df = pd.DataFrame({
    'Donnée': ["Consommation électrique (30 min.)", "Consommation électrique journalière", "Consommation gaz journalière", "T° extérieure"],
    'Start': [data_elec_heure.index[0], data_elec_jour.index[0], data_gaz_jour.index[0], data_meteo_jour.index[0]],
    'End': [data_elec_heure.index[-1], data_elec_jour.index[-1], data_gaz_jour.index[-1], data_meteo_jour.index[-1]]
})

# Diagramme de Gantt avec plotly
fig = px.timeline(df, x_start='Start', x_end='End', y='Donnée')
fig.update_yaxes(autorange="reversed")  # Inverser l'axe Y pour un affichage classique
fig.update_traces(marker_color='green',width=0.2)
fig.update_layout(
    title="Périodes couvertes par les données",
width=1000,  # Largeur en pixels
height=400)

# Afficher la figure dans Streamlit
st.plotly_chart(fig)
