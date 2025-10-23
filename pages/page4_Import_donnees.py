import streamlit as st
import pandas as pd

# -------------------------
# Config
# -------------------------

tab_grdf, tab_enedis = st.tabs(["Données GRDF", "Données ENEDIS"])

with tab_grdf:

    MANDATORY_COLUMNS = [
        'Date de relevé',
        'Volume consommé (m3)',
        'Energie consommée (kWh)',
        'Coefficient de conversion',
        'Température locale (°C)'
    ]

    st.title("📊 Import de données GRDF")

    # -------------------------
    # Initialisation session_state
    # -------------------------
    if "df_grdf" not in st.session_state:
        st.session_state.df_grdf = None
    if "show_format_grdf" not in st.session_state:
        st.session_state.show_format_grdf = False
    if "import_button_active_grdf" not in st.session_state:
        st.session_state.import_button_active_grdf = False
    if "imported_grdf" not in st.session_state:
        st.session_state.imported_grdf = False

    # -------------------------
    # Layout uploader + bouton "Voir format" côte à côte
    # -------------------------
    col_upload, col_format = st.columns([3, 1])
    with col_upload:
        uploaded_file = st.file_uploader(
            "Déposez votre fichier Excel ici",
            type=["xlsx", "xls"],
            accept_multiple_files=False,
            key="file_uploader_grdf"
        )
    with col_format:
        if st.button("Format GRDF"):
            st.session_state.show_format_grdf = not st.session_state.show_format_grdf
        if st.session_state.show_format_grdf:
            st.image("images/format fichier GRDF.png", caption="Exemple de format attendu", width='stretch')

    # -------------------------
    # Réinitialisation de l'état d'import UNIQUEMENT si un NOUVEAU fichier est sélectionné
    # -------------------------
    if uploaded_file is not None and uploaded_file != st.session_state.get("last_uploaded_file"):
        st.session_state.imported_grdf = False
        st.session_state.last_uploaded_file = uploaded_file

    # -------------------------
    # Lecture, validation et affichage du fichier
    # -------------------------
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file, sheet_name=0, skiprows=8, usecols="B:H")
            missing_cols = [c for c in MANDATORY_COLUMNS if c not in df.columns]
            if missing_cols:
                st.error(f"Colonnes manquantes : {', '.join(missing_cols)}")
                st.session_state.df_grdf = None
                st.session_state.import_button_active_grdf = False
            else:
                st.session_state.df_grdf = df
                st.session_state.import_button_active_grdf = True
        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier : Vérifier le format du fichier excel")
            st.session_state.df_grdf = None
            st.session_state.import_button_active_grdf = False

    # -------------------------
    # Affichage dynamique avec placeholder
    # -------------------------


    def import_data():
        from gestionbdd.db import SessionLocal
        from gestionbdd.crud import insert_data_conso_gaz_jour
        from gestionbdd.getdata import get_data

        db = SessionLocal()
        df_newdata_gaz = st.session_state.df_grdf.copy()
        df_newdata_gaz = df_newdata_gaz[['Date de relevé', 'Volume consommé (m3)', 'Energie consommée (kWh)', 'Coefficient de conversion', 'Température locale (°C)']]
        df_newdata_gaz.columns = ['horodatage', 'volume', 'energie','pci','text']
        df_newdata_gaz['horodatage']=pd.to_datetime(df_newdata_gaz['horodatage'], format='%d/%m/%Y')
        result_import = insert_data_conso_gaz_jour(db, df_newdata_gaz)
        if result_import != "OK":
            st.error(f"Erreur lors de l'intégration des données : {result_import}")
        else:
            st.success("Données importées avec succès dans la base Postgres !")

            # On met à jour  le dataframe dans streamlit
            data_gaz_jour   = get_data(source = "gaz_jour")
            st.session_state["data_gaz_jour"]   = data_gaz_jour
            data_gaz_mois   = data_gaz_jour['energie'].resample("MS").sum()
            st.session_state["data_gaz_mois"]   = data_gaz_mois



    table_placeholder = st.empty()

    if st.session_state.df_grdf is not None:
        with table_placeholder.container():
            st.dataframe(st.session_state.df_grdf, width='stretch')
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Importer", disabled=not st.session_state.import_button_active_grdf):
                    if not st.session_state.imported_grdf:
                        import_data()
                        st.session_state.imported_grdf = True
                    else:
                        st.error("Les données ont déjà été importées.")
            with col2:
                pass  # Placeholder vide pour garder l'alignement

    else:
        st.info("📥 Veuillez importer un fichier Excel pour commencer.")

with tab_enedis:

    import streamlit as st
    import pandas as pd
    import os
    
    # -------------------------
    # Config
    # -------------------------


    MANDATORY_COLUMNS = [
        'Date',
        'Valeur (en kWh)'
    ]

    st.title("📊 Import de données Enedis")

    # -------------------------
    # Initialisation session_state
    # -------------------------
    if "df_enedis" not in st.session_state:
        st.session_state.df_enedis = None
    if "show_format" not in st.session_state:
        st.session_state.show_format = False
    if "import_button_active" not in st.session_state:
        st.session_state.import_button_active = False
    if "imported" not in st.session_state:
        st.session_state.imported = False

    # -------------------------
    # Layout uploader + bouton "Voir format" côte à côte
    # -------------------------
    col_upload, col_format = st.columns([3, 1])
    with col_upload:
        uploaded_file = st.file_uploader(
            "Déposez votre fichier Excel ici",
            type=["xlsx", "xls"],
            accept_multiple_files=False,
            key="file_uploader_enedis"
        )
    with col_format:
        if st.button("Format ENEDIS"):
            st.session_state.show_format = not st.session_state.show_format
        if st.session_state.show_format:
            st.image("images/format fichier ENEDIS.png", caption="Exemple de format attendu", width='stretch')

    # -------------------------
    # Réinitialisation de l'état d'import UNIQUEMENT si un NOUVEAU fichier est sélectionné
    # -------------------------
    if uploaded_file is not None and uploaded_file != st.session_state.get("last_uploaded_file"):
        st.session_state.imported = False
        st.session_state.last_uploaded_file = uploaded_file

    # -------------------------
    # Lecture, validation et affichage du fichier
    # -------------------------
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file, sheet_name='Export Consommation Quotidienne', skiprows=13, usecols="B:C")
            missing_cols = [c for c in MANDATORY_COLUMNS if c not in df.columns]
            if missing_cols:
                st.error(f"Colonnes manquantes : {', '.join(missing_cols)}")
                st.session_state.df_enedis = None
                st.session_state.import_button_active = False
            else:
                st.session_state.df_enedis = df
                st.session_state.import_button_active = True
        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier : {e}")
            st.session_state.df_enedis = None
            st.session_state.import_button_active = False

    # -------------------------
    # Affichage dynamique avec placeholder
    # -------------------------


    def import_data():
        from gestionbdd.db import SessionLocal
        from gestionbdd.crud import insert_data_conso_jour
        from gestionbdd.getdata import get_data

        db = SessionLocal()
        df_newdata_elec = st.session_state.df_enedis.copy()
        df_newdata_elec.columns = ['horodatage', 'value']
        df_newdata_elec['horodatage']=pd.to_datetime(df_newdata_elec['horodatage'], format='%d/%m/%Y')
        result_import = insert_data_conso_jour(db, df_newdata_elec)
        if result_import != "OK":
            st.error(f"Erreur lors de l'intégration des données : {result_import}")
        else:
            st.success("Données importées avec succès dans la base Postgres !")
            # On met à jour  le dataframe dans streamlit
            data_elec_jour   = get_data(source = "elec_jour")
            st.session_state["data_elec_jour"]   = data_elec_jour
            data_elec_mois   = data_elec_jour['value'].resample("MS").sum()
            st.session_state["data_elec_mois"]   = data_elec_mois
    





    table_placeholder = st.empty()

    if st.session_state.df_enedis is not None:
        with table_placeholder.container():
            st.dataframe(st.session_state.df_enedis, width='stretch')
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Importer", disabled=not st.session_state.import_button_active):
                    if not st.session_state.imported:
                        import_data()
                        st.session_state.imported = True
                    else:
                        st.error("Les données ont déjà été importées.")
            with col2:
                pass  # Placeholder vide pour garder l'alignement

    else:
        st.info("📥 Veuillez importer un fichier Excel pour commencer.")
