import streamlit as st
from gestionbdd.getdata import get_data
from modelisation.predict import predict_conso_mensuelles
from joblib import load
import os


global_page = st.Page("pages/page0_Global.py", title="Global")
elec_page = st.Page("pages/page1_Electricite.py", title="Electricité")
gaz_page  = st.Page("pages/page2_Gaz_naturel.py", title="Gaz naturel")
data_page  = st.Page("pages/page3_Description_donnees.py", title="Description données")
import_page  = st.Page("pages/page4_Import_donnees.py", title="Import données")


# Chargement des données

data_path = os.path.join(os.path.dirname(__file__), "data", "data.joblib")
data_obj  = load(data_path)

for srce, df in data_obj.items():
    st.session_state[srce] = df


# Chargement des modèles 
model_path_elec = os.path.join(os.path.dirname(__file__), "ml_models", "model-elec-mois.joblib")
model_path_gaz  = os.path.join(os.path.dirname(__file__), "ml_models", "model-gaz-mois.joblib")


model_elec_obj = load(model_path_elec)
model_gaz_obj = load(model_path_gaz)

predict_conso_mensuelles(model_obj=model_elec_obj,typeenergie="elec")
predict_conso_mensuelles(model_obj=model_gaz_obj,typeenergie="gaz")



pg = st.navigation([global_page,elec_page, gaz_page,data_page, import_page])
st.set_page_config(
    page_title="Accueil",
    page_icon=":chart_with_upwards_trend:"
)

pg.run()