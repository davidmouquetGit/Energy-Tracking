import streamlit as st

tab1, tab2 = st.tabs(["Analyse", "Configuration"])

with tab1:
    st.header("Analyse des données")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Graphique 1")
        st.bar_chart([10, 20, 30, 40])
    with col2:
        st.write("Graphique 2")
        st.line_chart([1, 3, 2, 5])

with tab2:
    st.header("Configuration")
    with st.expander("Paramètres avancés"):
        option = st.selectbox("Choisir une option", ["Option 1", "Option 2"])
        st.write(f"Option sélectionnée : {option}")
