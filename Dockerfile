# Usamos la imagen base de Python
FROM python:3.12-slim

# Establecemos el directorio de trabajo
WORKDIR /app

# Instalamos Poetry
RUN pip install --no-cache-dir "poetry"

# Copiamos los archivos de configuración de Poetry y dependencias
COPY . .
# COPY pyproject.toml poetry.lock /app/

# Instalamos las dependencias del proyecto
RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

# Copiamos todo el código fuente del proyecto

# Exponemos el puerto que usará la aplicación
EXPOSE 8000

# Comando para iniciar Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
