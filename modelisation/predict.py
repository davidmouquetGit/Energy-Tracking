import pandas as pd
import streamlit as st

def predict_conso(model_obj:dict, 
                  typeenergie:str):
    

    data_gaz_mois = st.session_state["data_gaz_mois"]
  
    """
        
    data_model_mois = pd.concat([data_elec_jour['value'],data_meteo_jour['DJU'],data_occup_jour['presence']], axis=1)


    data_model_mois['presence'] = 100*data_model_mois['presence']/data_model.resample("MS").size()

    model = LinearRegression()
    x = data_model_mois[['DJU','presence']]
    y = data_model_mois['value']
    """