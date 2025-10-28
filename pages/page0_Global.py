import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from utils.utilitaires import display_logo



# Configuration de la page
st.set_page_config(layout="centered")


# Afficher le logo
display_logo()







# transformation des données

data_elec_mois  = st.session_state["data_elec_mois"]
data_gaz_mois   = st.session_state["data_gaz_mois"]


data_elec_mois = data_elec_mois[data_elec_mois.index>='2023-01-01']
data_gaz_mois = data_gaz_mois[data_gaz_mois.index>='2023-01-01']


data_elec_year = data_elec_mois.resample('YS').sum()
data_gaz_year  = data_gaz_mois.resample('YS').sum()

mois_elec = data_elec_mois.index.strftime("%b %Y")
mois_gaz  = data_gaz_mois.index.strftime("%b %Y")

year_elec = data_elec_year.index.strftime("%Y")
year_gaz  = data_gaz_year.index.strftime("%Y")


# Température de base (18°C)
T_base = 18

# Calcul des DJU
data_meteo_jour = st.session_state["data_meteo_jour"]
data_meteo_jour = data_meteo_jour[data_meteo_jour.index>='2023-01-01']

T_moyenne = (data_meteo_jour['temperature_2m_min'] + data_meteo_jour['temperature_2m_max']) / 2
data_meteo_jour = data_meteo_jour.assign(DJU=lambda x: (T_base - T_moyenne).clip(lower=0))

dju_month = data_meteo_jour['DJU'].resample('MS').sum()
dju_year  = data_meteo_jour['DJU'].resample('YS').sum()
mois_dju  = dju_month.index.strftime("%b %Y")
year_dju  = dju_year.index.strftime("%Y")



# Calcul des variation de consommations annuelles à la date de consultation du rapport

data_elec_jour  = st.session_state["data_elec_jour"]
last_date_with_data_elec =  data_elec_jour.index[-1]
jour_mois = last_date_with_data_elec.strftime("%m-%d")  # 
data_elec_jour['mois_jour'] = data_elec_jour.index.strftime("%m-%d")
conso_filtre = data_elec_jour[data_elec_jour['mois_jour'] <= jour_mois]


conso_filtre = conso_filtre.assign(annee=
    lambda x: x.index.year
)

cumul_par_annee = conso_filtre.groupby('annee')['value'].sum()
annee_en_cours   = int(cumul_par_annee.index[-1])
annee_precedente = int(cumul_par_annee.index[-2])
conso_annee_courante_elec  = cumul_par_annee.loc[annee_en_cours]
conso_annee_precedente_elec = cumul_par_annee.loc[annee_precedente]


data_gaz_jour = st.session_state["data_gaz_jour"]
last_date_with_data_gaz =  data_gaz_jour.index[-1]
jour_mois = last_date_with_data_gaz.strftime("%m-%d")  # "05-15"
data_gaz_jour['mois_jour'] = data_gaz_jour.index.strftime("%m-%d")
conso_filtre = data_gaz_jour[data_gaz_jour['mois_jour'] <= jour_mois]

conso_filtre = conso_filtre.assign(annee=
    lambda x: x.index.year
)

cumul_par_annee = conso_filtre.groupby('annee')['energie'].sum()
annee_en_cours   = int(cumul_par_annee.index[-1])
annee_precedente = int(cumul_par_annee.index[-2])
conso_annee_courante_gaz  = cumul_par_annee.loc[annee_en_cours]
conso_annee_precedente_gaz = cumul_par_annee.loc[annee_precedente]



tab_annuel, tab_mois = st.tabs(["Consommation annuelle", "Historique mensuel"])

with tab_annuel:
 
    variation_elec = (conso_annee_courante_elec - conso_annee_precedente_elec) / conso_annee_precedente_elec * 100
    variation_gaz = (conso_annee_courante_gaz  - conso_annee_precedente_gaz ) / conso_annee_precedente_gaz  * 100

    # Deux colonnes
    col1, col2 = st.columns(2)

    st.markdown("""
        <style>
        /* Couleur et taille du label metric */
        [data-testid="stMetricLabel"] {
            font-size: 40px !important;
            color: #575656;
            font-weight: 600;
        }
        /* Couleur du texte de la valeur principale */
        [data-testid="stMetricValue"] {
            font-size: 26px !important;
            color:#575656;
        }
        </style>""", unsafe_allow_html=True)
        
        # Dans ton script Streamlit
    st.markdown(
        """
        <style>
        .reportview-container .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .stMetric {
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


    # Première métrique : consommation
    col1.metric(
        label="Electricité",
        value=f"{int(conso_annee_courante_elec)} kWh",
        delta=f"{variation_elec:+.1f} % par rapport à {annee_precedente} le " + last_date_with_data_elec.strftime("%d %b"),
        delta_color="inverse"  # vert si baisse, rouge si hausse
    )



    # Deuxième métrique : dépense
    col2.metric(
        label="Gaz",
        value=f"{int(conso_annee_courante_gaz)} kWh",
        delta=f"{variation_gaz:+.1f} % par rapport à {annee_precedente} le " + last_date_with_data_gaz.strftime("%d %b"),
        delta_color="inverse"  # vert si baisse, rouge si hausse
    )



    # --- Création du graphique ---
    fig_year = go.Figure()

    fig_year.add_trace(go.Bar(
        x=year_elec,
        y=data_elec_year,
        name="Electricité",
        marker_color="steelblue",
        yaxis="y1"
    ))

    fig_year.add_trace(go.Bar(
        x=year_gaz,
        y=data_gaz_year,
        name="Gaz",
        marker_color="darkorange",
        yaxis="y1"
    ))

    # DJU (axe secondaire)
    fig_year.add_trace(go.Scatter(
        x=year_dju,
        y=dju_year,
        name="DJU",
        mode="lines+markers",
        line=dict(color="mediumseagreen", width=2,dash="dot"),
        marker=dict(size=10),
        yaxis="y2"
    ))

    st.markdown(
        """
        <style>
        .dju-tooltip {
            position: relative;
            display: inline-block;
            border-bottom: 1px dotted black;
        }
        .dju-tooltip .tooltiptext {
            visibility: hidden;
            width: 200px;
            background-color: #555;
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 5px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -100px;
            opacity: 0;
            transition: opacity 0.3s;
        }
        .dju-tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
        /* Ajout d'une marge inférieure réduite pour le paragraphe */
        p.custom-title {
            margin-bottom: 5px !important;  /* Réduit l'espace sous le titre */
            font-weight: bold;
        }
        </style>
        <p class="custom-title"><strong>Historique consommation annuelle et <span class="dju-tooltip">DJU<span class="tooltiptext">Les DJU (Degrés-Jours Unifiés) mesurent l'écart entre la température extérieure et 18°C. Plus les DJU sont élevés, plus il a fait froid.</span></span>(*)</strong></p>
        """,
        unsafe_allow_html=True
    )


    # --- Mise en page ---
    fig_year.update_layout(
        barmode="group",
        yaxis=dict(
            title=dict(text="Consommation (kWh)", font=dict(color="steelblue")),
            tickfont=dict(color="steelblue")
        ),
        yaxis2=dict(
            title=dict(text="DJU", font=dict(color="mediumseagreen")),
            tickfont=dict(color="mediumseagreen"),
            overlaying="y",
            side="right"
        ),
        # Ces deux paramètres doivent être ici, au niveau du layout global 
        bargap=0.2,            # espace entre groupes de barres
        bargroupgap=0.05,      # espace entre barres d’un même groupe
        template="simple_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.0,
            xanchor="center",
            x=0.2
        )
    )

    st.plotly_chart(fig_year, use_container_width=True)



with tab_mois:

    # --- Création du graphique ---
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=mois_elec,
        y=data_elec_mois,
        name="Electricité",
        marker_color="steelblue",
        yaxis="y1"
    ))

    fig.add_trace(go.Bar(
        x=mois_gaz,
        y=data_gaz_mois,
        name="Gaz",
        marker_color="darkorange",
        yaxis="y1"
    ))


    # DJU (axe secondaire)
    fig.add_trace(go.Scatter(
        x=mois_dju,
        y=dju_month,
        name="DJU",
        mode="lines+markers",
        line=dict(color="mediumseagreen", width=2,dash="dot"),
        marker=dict(size=6),
        yaxis="y2"
    ))
    # --- Mise en page ---
    fig.update_layout(
        barmode="group",
        title=dict(text="Consommation mensuelle et DJU", x=0.1),
        yaxis=dict(
            title=dict(text="Consommation (kWh)", font=dict(color="steelblue")),
            tickfont=dict(color="steelblue")
        ),
        yaxis2=dict(
            title=dict(text="DJU", font=dict(color="mediumseagreen")),
            tickfont=dict(color="mediumseagreen"),
            overlaying="y",
            side="right"
        ),
        # Ces deux paramètres doivent être ici, au niveau du layout global
        bargap=0.2,            # espace entre groupes de barres
        bargroupgap=0.05,      # espace entre barres d’un même groupe
        template="simple_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.0,
            xanchor="center",
            x=0.2
        )
    )


    st.plotly_chart(fig, use_container_width=True)

  
