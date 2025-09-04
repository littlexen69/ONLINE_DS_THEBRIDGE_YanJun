import streamlit as st
import sys

sys.path.append("C:/Users/yanju/Online_env/REPO_PRUEBA/ONLINE_DS_THEBRIDGE_YanJun/Machine Learning/Stock_Prediction_ML/sources/")

import sources.evaluation as evaluation


st.set_page_config(page_title = "Stock Prediction", page_icon=":chart", layout = "centered")
st.title("Stock Prediction")

with st.expander("Elige una empresa"):
    opcion = st.selectbox(
        "Selecciona una empresa:",
        ["Apple", "Google", "Inditex", "Johnson & Johnson", "JPMorgan", "Tesla"]
    )

    if opcion == "Apple":
        st.image("aapl.png")
        if st.button("Predecir mañana"):
            st.write(evaluation.prediction_aapl)
    elif opcion == "Google":
        st.image("googl.png")
        if st.button("Predecir mañana"):
            st.write(evaluation.prediction_googl)
    elif opcion == "Inditex":
        st.image("itx.png")
        if st.button("Predecir mañana"):
            st.write(evaluation.prediction_itx)
    elif opcion == "Johnson & Johnson":
        st.image("jnj.png")
        if st.button("Predecir mañana"):
            st.write(evaluation.prediction_jnj)
    elif opcion == "JPMorgan":
        st.image("jpm.png")
        if st.button("Predecir mañana"):
            st.write(evaluation.prediction_jpm)
    elif opcion == "Tesla":
        st.image("tsla.png")
        if st.button("Predecir mañana"):
            st.write(evaluation.prediction_tsla)