import streamlit as st
import json
import numpy as np
import pandas as pd
import os

st.set_page_config(page_title="Stock Prediction", page_icon=":chart:", layout="centered")
st.title("Stock Prediction")

BASE_DIR = os.path.dirname(__file__)
MODELS_DIR = os.path.join(BASE_DIR, "..", "models")

def cargar_modelo_json(nombre):
    with open(os.path.join(MODELS_DIR, f"{nombre}_model.json"), "r") as f:
        return json.load(f)

def predecir_lineal(modelo_json: dict, features_actuales: pd.Series) -> float:
    # Asegura orden de features
    names = modelo_json["feature_names"]
    x = features_actuales.reindex(names).astype(float).values
    coef = np.array(modelo_json["coef"], dtype=float)
    intercept = float(modelo_json.get("intercept", 0.0))
    return float(np.dot(x, coef) + intercept)

# Ejemplo: cargar tus modelos
modelos = {
    "Apple": cargar_modelo_json("aapl"),
    "Google": cargar_modelo_json("googl"),
    "Inditex": cargar_modelo_json("itx"),
    "Johnson & Johnson": cargar_modelo_json("jnj"),
    "JPMorgan": cargar_modelo_json("jpm"),
    "Tesla": cargar_modelo_json("tsla"),
}

with st.expander("Elige una empresa"):
    opcion = st.selectbox(
        "Selecciona una empresa:",
        list(modelos.keys())
    )
    st.image({
        "Apple": "aapl.png",
        "Google": "googl.png",
        "Inditex": "itx.png",
        "Johnson & Johnson": "jnj.png",
        "JPMorgan": "jpm.png",
        "Tesla": "tsla.png"
    }[opcion])

    # TODO: aquí debes construir las features del último día disponible
    # EJEMPLO DE JUGUETE: reemplaza este dict con tus features reales
    features_hoy = {
        "ret_1d": 0.002,
        "rsi": 55.0,
        "vol": 1.2
    }
    features_hoy = pd.Series(features_hoy)

    if st.button("Predecir mañana"):
        modelo_json = modelos[opcion]
        try:
            y_pred = predecir_lineal(modelo_json, features_hoy)
            st.metric("Predicción para mañana", f"{y_pred:.4f}")
        except KeyError as e:
            st.error(f"Falta la feature '{e.args[0]}' en las variables de entrada.")
        except Exception as e:
            st.exception(e)
