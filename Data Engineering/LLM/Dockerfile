# Usa una imagen base ligera de Python
FROM python:3.10-slim

# Establece directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema necesarias para psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia los archivos de dependencias
COPY requirements.txt .

# Instala dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el proyecto
COPY . .

# Variables de entorno (puedes sobreescribirlas en docker-compose o con -e)
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=5000

# Expone el puerto
EXPOSE 5000

# Comando para iniciar la aplicación
CMD ["python", "app.py"]
