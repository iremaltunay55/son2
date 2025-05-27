# Python 3.12 base image kullan
FROM python:3.12-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıklarını kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Port'u expose et
EXPOSE 8080

# Environment variables
ENV FLASK_ENV=production
ENV FLASK_DEBUG=False
ENV PORT=8080

# Uygulamayı başlat
CMD ["python", "app_swagger_fixed.py"]
