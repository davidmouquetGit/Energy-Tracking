import pandas as pd
import plotly.graph_objects as go
import streamlit as st



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
    title=dict(text="Consommation annuelle et DJU", x=0.1),
    xaxis=dict(title="Mois"),
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
    # Ces deux paramètres doivent être ici, au niveau du layout global 👇
    bargap=0.2,            # espace entre groupes de barres
    bargroupgap=0.05,      # espace entre barres d’un même groupe
    template="plotly_white",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.0,
        xanchor="center",
        x=0.2
    )
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


# --- Mise en page ---
fig_year.update_layout(
    barmode="group",
    title=dict(text="Consommation annuelle et DJU", x=0.1),
    xaxis=dict(title="Mois"),
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
    template="plotly_white",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.0,
        xanchor="center",
        x=0.2
    )
)









st.plotly_chart(fig, use_container_width=True)

st.plotly_chart(fig_year, use_container_width=True)
  
