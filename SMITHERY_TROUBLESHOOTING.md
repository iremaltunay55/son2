# 🔧 Smithery Troubleshooting Kılavuzu

## ❌ Yaşanan Sorunlar:
1. "Could not find Dockerfile in repository"
2. "Could not find smithery.yaml in repository" 
3. "Unexpected internal error or timeout"
4. "Error type: not_mcp_server"

## 🛠️ Çözüm Adımları:

### 1️⃣ **Cache Temizleme**
- Smithery dashboard'da mevcut projeyi silin
- Tarayıcı cache'ini temizleyin (Ctrl+Shift+Delete)
- Yeni proje oluşturun

### 2️⃣ **Repository Kontrolü**
GitHub'da şu dosyaların olduğunu kontrol edin:
- ✅ `Dockerfile` (root dizinde)
- ✅ `smithery.yaml` (root dizinde)
- ✅ `requirements.txt`
- ✅ `app_swagger_fixed.py`

### 3️⃣ **Smithery'de Manuel Konfigürasyon**

Eğer otomatik tanıma çalışmazsa:

1. **New Project** → **Manual Configuration**
2. **Build Settings:**
   ```
   Build Type: Docker
   Dockerfile Path: Dockerfile
   Context: .
   ```
3. **Runtime Settings:**
   ```
   Port: 8080
   Health Check: /api/v1/health
   ```
4. **Environment Variables:**
   ```
   OPENWEATHER_API_KEY=6b2e97b1b6559436aee37b83b71412b3
   FLASK_ENV=production
   PORT=8080
   ```

### 4️⃣ **Alternatif Yaklaşım: Smithery CLI**

```bash
# Smithery CLI yükle
npm install -g @smithery/cli

# Login
smithery login

# Deploy
smithery deploy
```

### 5️⃣ **Dosya İçerikleri Kontrolü**

**Dockerfile içeriği:**
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
ENV PORT=8080
ENV FLASK_ENV=production
CMD ["python", "app_swagger_fixed.py"]
```

**smithery.yaml içeriği:**
```yaml
name: hava-durumu-api
description: "Weather API with Swagger UI"
version: "1.0.2"

build:
  type: docker
  dockerfile: Dockerfile

runtime:
  port: 8080
  health_check:
    path: /api/v1/health

environment:
  FLASK_ENV: production
  PORT: "8080"

secrets:
  - OPENWEATHER_API_KEY
```

## 🚨 **Eğer Smithery Çalışmazsa:**

### **Plan B: Render.com**
1. https://render.com
2. GitHub ile giriş
3. Repository bağla
4. Environment variables ekle
5. Deploy

### **Plan C: Railway.app**
1. https://railway.app
2. GitHub ile giriş
3. Repository seç
4. Environment variables ekle
5. Deploy

## 📞 **Smithery Destek:**
- Discord: https://discord.gg/smithery
- Docs: https://smithery.ai/docs
- GitHub: https://github.com/smithery-ai

## ✅ **Başarı Kriterleri:**
- Build başarılı
- Health check geçiyor
- API endpoint'leri erişilebilir
- Swagger UI çalışıyor

**Not:** Smithery hala beta aşamasında, sorunlar normal. Alternatif platformlar daha stabil olabilir.
