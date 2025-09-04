# Stock Prediction — XGBoost + Streamlit

Aplicación sencilla para **predecir el precio de cierre ajustado del día siguiente** de varias acciones (Apple, Google, Inditex, Johnson & Johnson, JPMorgan y Tesla) usando *feature engineering* clásico y un modelo **XGBoostRegressor**. Incluye scripts para **descargar y procesar datos**, **entrenar y evaluar** el modelo, y una interfaz **Streamlit** para visualizar una predicción rápida.

> ⚠️ **Aviso**: Este proyecto es solo educativo. **No es asesoramiento financiero**. La predicción a un día con datos técnicos puede ser ruidosa e inestable. Úsalo bajo tu responsabilidad.

---

## 🧭 Índice

- [Arquitectura](#arquitectura)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración (API key)](#configuración-api-key)
- [Obtención y procesado de datos](#obtención-y-procesado-de-datos)
- [Entrenamiento y evaluación](#entrenamiento-y-evaluación)
- [App Streamlit](#app-streamlit)
- [Estructura de carpetas](#estructura-de-carpetas)
- [Ingeniería de características](#ingeniería-de-características)
- [Cómo añadir nuevos *tickers*](#cómo-añadir-nuevos-tickers)
- [Solución de problemas](#solución-de-problemas)
- [Licencia](#licencia)

---

## Arquitectura

- `data_processing.py`: descarga históricos diarios de EODHD para varios *tickers*, crea características y genera conjuntos **raw** y **processed**.
- `training.py`: escala características/objetivo con **MinMaxScaler**, entrena un **XGBRegressor**, realiza **walk-forward validation** y guarda modelos.
- `evaluation.py`: calcula y muestra **RMSE** y curvas *Actual vs Predicted*; expone funciones/valores para la app.
- `main.py`: **Streamlit** con un selector de empresa y botón “Predecir mañana”.

---

## Requisitos

- **Python 3.10+** (recomendado)
- Paquetes de `requirements.txt` (NumPy, Pandas, scikit-learn, XGBoost, Statsmodels, Streamlit, eodhd, etc.).

```bash
pip install -r requirements.txt
```

> Nota: XGBoost usa `tree_method="hist"` y CPU por defecto en este proyecto.

---

## Instalación

1. Clona o copia este repo.
2. (Opcional) Crea y activa un entorno virtual.
3. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```

---

## Configuración (API key)

Los datos se descargan del servicio **EODHD**. Necesitas una **API key** válida.

**Recomendado**: usa una variable de entorno en lugar de hardcodear la clave.

```python
# data_processing.py (ejemplo)
import os
from eodhd import APIClient

api = APIClient(api_key=os.getenv("EODHD_API_KEY"))
```

En tu terminal:
```bash
# macOS / Linux
export EODHD_API_KEY="TU_API_KEY"

# Windows PowerShell
$env:EODHD_API_KEY="TU_API_KEY"
```

---

## Obtención y procesado de datos

Ejecuta:

```bash
python data_processing.py
```

Qué hace:
- Descarga históricos diarios desde **2010-01-01** para: `AAPL.US, GOOGL.US, TSLA.US, JNJ.US, JPM.US, ITX.MC`.
- Guarda CSV en `data/raw/` (recomendado) y genera `data/processed/*.csv` con las features y la variable `target` (precio ajustado del día siguiente).

> 💡 **Rutas**: En el código original se usan rutas relativas del tipo `../data/...`. Si ejecutas los scripts desde la carpeta raíz del proyecto, se recomienda cambiar a `./data/...` para evitar confusiones (ver sección *Solución de problemas*).

---

## Entrenamiento y evaluación

Entrena y valida con *walk-forward*:

```bash
python training.py
```

- Escala X e y con `MinMaxScaler`.
- Entrena `XGBRegressor(n_estimators=1000, tree_method="hist", device="cpu")`.
- Realiza **walk-forward validation** (predice paso a paso sobre el último 20% de datos).
- Calcula **RMSE de test** y guarda modelos en `models/*.json`.

Evalúa y visualiza:

```bash
python evaluation.py
```

- Imprime **RMSE de *train* y *test***.
- Muestra gráficos *Actual vs Predicted* con `matplotlib`.
- Calcula una **predicción para el día siguiente** usando la última fila disponible de cada *ticker*.

---

## App Streamlit

Ejecuta la app en alguna terminal de Windows (Powershell, cmd,...):

```bash
streamlit run main.py
```

La interfaz permite elegir entre **Apple, Google, Inditex, Johnson & Johnson, JPMorgan y Tesla** y obtener la **predicción del día siguiente**.

### Recursos de imagen
El script espera ficheros de logo/imagen en el mismo directorio que `main.py` con estos nombres:
```
aapl.png  googl.png  itx.png  jnj.png  jpm.png  tsla.png
```
Colócalos o elimina las llamadas `st.image(...)` si no los necesitas.

### Nota sobre *imports* en `main.py`
El archivo original usa un `sys.path.append(...)` con una **ruta absoluta de Windows** y `import sources.evaluation`. Para un entorno portátil, sustituye por **imports relativos** si `evaluation.py` está en la misma carpeta:

```python
# main.py (recomendado)
import evaluation  # y usa evaluation.prediction_aapl, etc.
```

---

## Estructura de carpetas

Sugerencia de estructura (tras ejecutar los scripts):

```
project/
├─ data/
│  ├─ raw/
│  │  ├─ AAPL.US.csv
│  │  ├─ GOOGL.US.csv
│  │  └─ ...
│  └─ processed/
│     ├─ df_aapl.csv
│     ├─ df_googl.csv
│     └─ ...
├─ models/
│  ├─ aapl_model.json
│  ├─ googl_model.json
│  └─ ...
├─ main.py
├─ data_processing.py
├─ training.py
├─ evaluation.py
├─ requirements.txt
└─ README.md
```

> Los ficheros `*.pyc` son artefactos compilados y pueden ignorarse o eliminarse.

---

## Ingeniería de características

Para cada *ticker* se generan, entre otras, las siguientes *features*:

- Diferencias: `close_diff_1`, `adjusted_close(-1)` (lag 1).
- Calendario: `dayofweek, quarter, month, year, dayofyear, dayofmonth, weekofyear`.
- Medias móviles: `SMA(13)`, `EMA(9)`.
- Tendencia: `MACD` (EMA 24 – EMA 52).
- Volatilidad bandas de Bollinger (10): diferencia `Upper_Band - Lower_Band`.
- Rango diario: `H_L_diff = high - low`.
- **Target**: `target = adjusted_close.shift(-1)` (valor del día siguiente).

> Nota: La implementación del RSI usa una razón `ema_up/ema_down` como proxy. Si buscas el RSI clásico (0–100), puedes convertirla con la fórmula estándar: `100 - (100 / (1 + RS))`.

---

## Cómo añadir nuevos *tickers*

1. Añade el símbolo a `TICKERS` en `data_processing.py` (formato EODHD, p. ej. `MSFT.US`).
2. Vuelve a ejecutar `python data_processing.py` para generar los CSV.
3. Asegúrate de que `training.py` y `evaluation.py` cargan y tratan esos nuevos `df_*` (sigue el patrón existente).
4. (Opcional) Añade el nombre y el logo en `main.py` para que aparezca en la app.

---

## Solución de problemas

- **ImportError en `main.py` por ruta absoluta**  
  Cambia a imports relativos: `import evaluation` o reestructura los módulos en un paquete.

- **Rutas `../data/...`**  
  Si ejecutas desde la raíz del proyecto, sustituye `../data/...` por `./data/...` en los scripts, o lanza los scripts desde la carpeta adecuada.

- **Faltan imágenes**  
  La app llama a `st.image("aapl.png")`, etc. Coloca los ficheros o elimina esas líneas.

- **Sin API key / 403**  
  Define `EODHD_API_KEY` en tus variables de entorno.

- **Predicciones inestables**  
  Ajusta *features*, tamaño de ventana, `n_estimators`, o cambia a un *split* temporal más robusto. Considera semilla aleatoria y *early stopping*.

---

## Licencia

Indica aquí la licencia del proyecto (por ejemplo, MIT).

