# =============================================================
# 📌 Dockerfile — Breast Cancer API (Optimizado en capas)
# =============================================================
#
# Este archivo define la imagen Docker necesaria para ejecutar 
# la API Flask que predice cáncer de mama (benigno/maligno).
#
# ⚙️ Flujo general:
# 1. Se usa una imagen base ligera de Python.
# 2. Se configuran variables de entorno para mejorar logs y evitar pyc.
# 3. Se establece un directorio de trabajo en el contenedor.
# 4. Se copian e instalan las dependencias desde requirements.txt.
# 5. Se copia el resto del proyecto (modelo, app, templates, etc.).
# 6. Se expone el puerto 5000 para acceder a la API.
# 7. Se define el comando de inicio que ejecuta la API Flask.
#
# ✅ Importancia:
# Gracias a este Dockerfile, la aplicación puede ejecutarse en 
# cualquier entorno de manera consistente, sin preocuparse por 
# versiones de librerías ni dependencias locales.
# =============================================================

# 1️⃣ Imagen base ligera
FROM python:3.10-slim

# 2️⃣ Configuración de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3️⃣ Directorio de trabajo
WORKDIR /app

# 4️⃣ Copiar dependencias
COPY requirements.txt .

# 5️⃣ Instalar dependencias (cacheadas si no cambia requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# 6️⃣ Copiar el resto del proyecto
COPY . .

# 7️⃣ Exponer puerto
EXPOSE 5000

# 8️⃣ Comando de inicio
CMD ["python", "app.py"]