import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Titre de l'application
st.title("Saisie de consommations journalières (comme Excel)")

# Initialisation du DataFrame en session_state
if 'data' not in st.session_state:
    # On initialise avec 3 lignes vides par défaut
    dates = [datetime.today().date() - timedelta(days=i) for i in range(2, -1, -1)]
    st.session_state.data = pd.DataFrame({'Date': dates, 'Valeur': [0.0, 0.0, 0.0]})

# Affichage et édition du tableau avec comportement "Excel-like"
st.write("### Tableau de saisie (appuyez sur `Tab` ou `Entrée` pour ajouter une ligne)")
edited_data = st.data_editor(
    st.session_state.data,
    num_rows="dynamic",  # Permet d'ajouter/supprimer des lignes dynamiquement
    key="data_editor",
    hide_index=True,     # Cache l'index pour un affichage plus propre
    use_container_width=True,
    column_config={
        "Date": st.column_config.DateColumn(
            "Date",
            min_value=datetime(2020, 1, 1).date(),
            max_value=datetime(2025, 12, 31).date(),
            format="DD/MM/YYYY",
        ),
        "Valeur": st.column_config.NumberColumn(
            "Valeur (kWh)",
            format="%.2f",
        )
    }
)

# Mise à jour du DataFrame avec les modifications
st.session_state.data = edited_data

# Affichage du DataFrame final
st.write("### Données saisies")
st.dataframe(st.session_state.data)

# Option : bouton pour réinitialiser
if st.button("Réinitialiser"):
    st.session_state.data = pd.DataFrame(columns=['Date', 'Valeur'])
    st.rerun()

# Option : bouton pour exporter en CSV
if st.button("Exporter en CSV"):
    st.session_state.data.to_csv("consommations.csv", index=False)
    st.success("Fichier exporté avec succès !")
