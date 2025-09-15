# 📊 INVE\$TKING -- Asistente Financiero

Aplicación web con backend en **Flask** y frontend en **HTML +
TailwindCSS**, que ofrece un asistente conversacional dividido en tres
roles educativos sobre finanzas:

-   💡 **Finanzas Personales** (presupuesto, ahorro, deudas, hábitos).
-   📈 **Mercados Financieros** (acciones, bonos, ETFs,
    diversificación).
-   🏠 **Bienes Reales y Alternativos** (inmuebles, negocios, materias
    primas y cripto).

Todas las preguntas y respuestas se almacenan en una base de datos
PostgreSQL para su posterior consulta o análisis.

------------------------------------------------------------------------

## ⚙️ Tecnologías

-   **Backend**: Flask + Flask-CORS\
-   **Frontend**: HTML + TailwindCSS + JavaScript\
-   **LLM API**: [Groq](https://groq.com/)\
-   **Base de datos**: PostgreSQL\
-   **Contenedor**: Docker

------------------------------------------------------------------------

## 📂 Estructura del proyecto

    .
    ├── app.py              # Servidor Flask (endpoints y routing)
    ├── funciones.py        # Lógica de conexión a Groq + DB
    ├── variables.py        # Configuración de DB y clave API (⚠️ sensible)
    ├── index_3.html        # Interfaz web del chat
    ├── requirements.txt    # Dependencias de Python
    ├── Dockerfile          # Imagen de la app
    └── funciones.cpython-310.pyc / variables.cpython-310.pyc  # Bytecode (ignorar)

------------------------------------------------------------------------

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio

``` bash
git clone https://github.com/tuusuario/investking.git
cd investking
```

### 2. Crear entorno virtual e instalar dependencias

``` bash
python -m venv venv
source venv/bin/activate   # en Linux/Mac
venv\Scripts\activate      # en Windows

pip install -r requirements.txt
```

### 3. Configurar variables de entorno

En `variables.py` ya está configurado un ejemplo, pero en producción es
recomendable usar un archivo **.env**:

``` env
KEY_GROQ=tu_api_key_aqui
DB_HOST=...
DB_USER=...
DB_PASSWORD=...
DB_NAME=...
DB_PORT=5432
```

> ⚠️ **No subas tus claves reales a repositorios públicos**.

### 4. Ejecutar el servidor Flask

``` bash
python app.py
```

El backend quedará disponible en:\
👉 `http://127.0.0.1:5000`

Abre en el navegador `index_3.html` para probar el chat.

------------------------------------------------------------------------

## 🐳 Uso con Docker

### 1. Construir la imagen

``` bash
docker build -t investking .
```

### 2. Ejecutar el contenedor

``` bash
docker run -p 5000:5000 --env-file .env investking
```

------------------------------------------------------------------------

## 🖥️ Endpoints

-   `GET /` → Renderiza la interfaz web (`index_3.html`)\
-   `POST /t1` → Finanzas Personales\
-   `POST /t2` → Mercados Financieros\
-   `POST /t3` → Bienes Reales y Alternativos

Ejemplo de request:

``` json
POST /t1
{
  "question": "¿Cómo hago un presupuesto mensual?"
}
```

Respuesta:

``` json
{
  "question": "¿Cómo hago un presupuesto mensual?",
  "response": "Para comenzar, define tus ingresos fijos..."
}
```

------------------------------------------------------------------------

## 🛡️ Notas importantes

-   Este proyecto es **educativo**: no constituye asesoramiento
    financiero profesional.\
-   Cambia las claves de API y contraseñas de `variables.py` antes de
    desplegar en producción.\
-   Asegúrate de que la base de datos PostgreSQL tenga creada la tabla:

``` sql
CREATE TABLE preguntas_respuestas (
    id SERIAL PRIMARY KEY,
    pregunta TEXT,
    respuesta TEXT,
    fecha TIMESTAMP
);
```

------------------------------------------------------------------------

## 📌 Pendientes / Mejoras

-   [ ] Mover configuración sensible a `.env`\
-   [ ] Añadir autenticación de usuarios\
-   [ ] Implementar historial de chat en el frontend\
-   [ ] Desplegar en la nube (Heroku, AWS, etc.)
