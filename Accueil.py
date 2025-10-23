import streamlit as st
from gestionbdd.getdata import get_data




global_page = st.Page("pages/page0_Global.py", title="Global")
elec_page = st.Page("pages/page1_Electricite.py", title="Electricité")
gaz_page  = st.Page("pages/page2_Gaz_naturel.py", title="Gaz naturel")
data_page  = st.Page("pages/page3_Description_donnees.py", title="Description données")
import_page  = st.Page("pages/page4_Import_donnees.py", title="Import données")


# Chargement des données stockées dans PostGres


data_elec_heure = get_data(source = "elec_hour")
data_elec_jour  = get_data(source = "elec_jour")
data_gaz_jour   = get_data(source = "gaz_jour")
data_meteo_jour = get_data(source = "meteo_jour")
        
data_elec_mois  = data_elec_jour['value'].resample("MS").sum()
data_gaz_mois   = data_gaz_jour['energie'].resample("MS").sum()

st.session_state["data_elec_heure"] = data_elec_heure
st.session_state["data_elec_jour"]  = data_elec_jour 
st.session_state["data_gaz_jour"]   = data_gaz_jour
st.session_state["data_meteo_jour"] = data_meteo_jour
st.session_state["data_elec_mois"]  = data_elec_mois
st.session_state["data_gaz_mois"]   = data_gaz_mois


pg = st.navigation([global_page,elec_page, gaz_page,data_page, import_page])
st.set_page_config(
    page_title="Acueil",
    page_icon=""
)

pg.run()