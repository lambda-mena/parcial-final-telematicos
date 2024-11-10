# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libmariadb-dev-compat \
    libmariadb-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copiar los archivos de la aplicación
COPY . /app

# Instalar dependencias de Python
RUN pip install --upgrade pip
RUN pip install Flask==2.3.3 flask-cors Flask-MySQLdb Flask-SQLAlchemy

# Exponer el puerto en el que la aplicación correrá
EXPOSE 5000

# Ejecutar la aplicación
CMD ["python", "webapp/run.py"]
