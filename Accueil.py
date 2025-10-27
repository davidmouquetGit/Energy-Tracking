import streamlit as st
from gestionbdd.getdata import get_data
from modelisation.predict import predict_conso_mensuelles
from joblib import load


# CSS personnalisé pour la sidebar
st.markdown(
    """
    <style>
    section[data-testid="stSidebar"] {
        background-color: #f0f8ff;
        border-right: 1px solid #d1e7f5;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Définition des pages
global_page = st.Page("pages/page0_Global.py", title="Global", icon="🌍")
elec_page = st.Page("pages/page1_Electricite.py", title="Électricité", icon="⚡")
gaz_page = st.Page("pages/page2_Gaz_naturel.py", title="Gaz naturel", icon="🔥")
data_page = st.Page("pages/page3_Description_donnees.py", title="Description données", icon="📝")
import_page = st.Page("pages/page4_Import_donnees.py", title="Import données", icon="📤")

# Configuration de la navigation
pg = st.navigation([global_page, elec_page, gaz_page, data_page, import_page])

# Contenu de la sidebar
with st.sidebar:

    st.markdown("<p style='color: #666666; font-size: 12px;'>EnergyTrack © 2025</p>", unsafe_allow_html=True)

# Chargement des données stockées dans PostGres


data_elec_heure = get_data(source = "elec_hour")
data_elec_jour  = get_data(source = "elec_jour")
data_gaz_jour   = get_data(source = "gaz_jour")
data_meteo_jour = get_data(source = "meteo_jour")
data_occup_jour = get_data(source = "occup_jour")
        
data_elec_mois  = data_elec_jour['value'].resample("MS").sum()
data_gaz_mois   = data_gaz_jour['energie'].resample("MS").sum()

data_occup_jour['presence'] = data_occup_jour['presence'].apply(lambda o: 1.0 if o=="oui" else 0.0)
data_occup_mois             = 100*data_occup_jour['presence'].resample("MS").sum()/data_occup_jour.resample("MS").size()



T_moyenne = (data_meteo_jour['temperature_2m_min'] + data_meteo_jour['temperature_2m_max']) / 2
data_meteo_jour = data_meteo_jour.assign(DJU=lambda x: (18.0 - T_moyenne).clip(lower=0))
data_dju_mois = data_meteo_jour['DJU'].resample('MS').sum()



st.session_state["data_elec_heure"] = data_elec_heure
st.session_state["data_elec_jour"]  = data_elec_jour 
st.session_state["data_gaz_jour"]   = data_gaz_jour
st.session_state["data_meteo_jour"] = data_meteo_jour
st.session_state["data_dju_mois"]   = data_dju_mois
st.session_state["data_elec_mois"]  = data_elec_mois
st.session_state["data_gaz_mois"]   = data_gaz_mois
st.session_state["data_occup_mois"] = data_occup_mois


# Chargement des modèles 


model_elec_obj = load("ml_models/model-elec-mois.joblib")
model_gaz_obj = load("ml_models/model-gaz-mois.joblib")

predict_conso_mensuelles(model_obj=model_elec_obj,typeenergie="elec")
predict_conso_mensuelles(model_obj=model_gaz_obj,typeenergie="gaz")



pg = st.navigation([global_page,elec_page, gaz_page,data_page, import_page])
st.set_page_config(
    page_title="Accueil",
    page_icon=":chart_with_upwards_trend:"
)

pg.run()