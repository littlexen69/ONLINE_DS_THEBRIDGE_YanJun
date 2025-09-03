import streamlit as st
import sys

sys.path.append("C:/Users/yanju/Online_env/REPO_PRUEBA/ONLINE_DS_THEBRIDGE_YanJun/Machine Learning/Stock_Prediction_ML")

from src import data_processing, training

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
            predict_aapl = training.xgb_prediction(data_processing.df_aapl.values, training.last_row_aapl.values[0][:-1])
            st.write(predict_aapl)
    elif opcion == "Google":
        st.image("googl.png")
        if st.button("Predecir mañana"):
            predict_googl = training.xgb_prediction(data_processing.df_googl.values, training.last_row_googl.values[0][:-1])
            st.write(predict_googl)
    elif opcion == "Inditex":
        st.image("itx.png")
        if st.button("Predecir mañana"):
            predict_itx = training.xgb_prediction(data_processing.df_itx.values, training.last_row_itx.values[0][:-1])
            st.write(predict_itx)
    elif opcion == "Johnson & Johnson":
        st.image("jnj.png")
        if st.button("Predecir mañana"):
            predict_jnj = training.xgb_prediction(data_processing.df_jnj.values, training.last_row_jnj.values[0][:-1])
            st.write(predict_jnj)
    elif opcion == "JPMorgan":
        st.image("jpm.png")
        if st.button("Predecir mañana"):
            predict_jpm = training.xgb_prediction(data_processing.df_jpm.values, training.last_row_jpm.values[0][:-1])
            st.write(predict_jpm)
    elif opcion == "Tesla":
        st.image("tsla.png")
        if st.button("Predecir mañana"):
            predict_tsla = training.xgb_prediction(data_processing.df_tsla.values, training.last_row_tsla.values[0][:-1])
            st.write(predict_tsla)