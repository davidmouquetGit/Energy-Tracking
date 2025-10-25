import pandas as pd
import streamlit as st
import numpy as np

def predict_conso_mensuelles(model_obj:dict, 
                             typeenergie:str):
    
    if typeenergie not in ["elec","gaz"]:
        print("Erreur: Le type d'énergie doit etre 'elec' ou 'gaz")
        return None
    
    data_dju_mois   = st.session_state["data_dju_mois"]
    data_occup_mois = st.session_state["data_occup_mois"]
    data_occup_mois.name = 'presence'    

    data_model_mois = pd.concat([data_dju_mois,data_occup_mois], axis=1)
    data_model_mois.dropna(inplace=True)
    features_name = model_obj['x_train'].columns
    df_X = data_model_mois[features_name]


    date_debut = model_obj['x_train'].index[0]
    df_X = df_X[df_X.index>=date_debut]
    y_pred = model_obj['model'].predict(df_X)

    sigma2  = model_obj['sigma2 ']
    XtX_inv = model_obj['XtX_inv']
    t_val   = model_obj['t_val']

    
    # facteur d'incertitude pour chaque prédiction

    X = df_X.values  # matrice des features
    n = X.shape[0]
    X_design = np.hstack([np.ones((n, 1)), X])
    # Erreur standard de la prédiction
    pred_var = np.sum(X_design @ XtX_inv * X_design, axis=1)
    interval = t_val * np.sqrt(sigma2 * (1 + pred_var))

    # bornes de l'IC
    lower = y_pred - interval
    upper = y_pred + interval

    modele_mois = pd.DataFrame(index=df_X.index,data = {"value":y_pred,"lower":lower,"upper":upper})

    modele_mois['value'] = modele_mois['value'].apply(lambda v: 0.0 if v<0.0 else v)
    modele_mois['lower'] = modele_mois['lower'].apply(lambda v: 0.0 if v<0.0 else v)

    if typeenergie == "elec":
        st.session_state["modele_elec_mois"] = modele_mois

    if typeenergie == "gaz":
        st.session_state["modele_gaz_mois"]  = modele_mois
