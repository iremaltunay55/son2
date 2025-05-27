# 🚀 Smithery'de Hava Durumu API'si Deployment Kılavuzu

## 📋 Gerekli Dosyalar
✅ `app_swagger_fixed.py` - Ana uygulama
✅ `requirements.txt` - Python bağımlılıkları
✅ `Procfile` - Smithery başlatma komutu
✅ `runtime.txt` - Python versiyonu
✅ `.env` - Environment variables (API anahtarı)

## 🔧 Smithery'de Deployment Adımları

### 1️⃣ **Proje Dosyalarını Hazırlayın**
```bash
# Tüm dosyaların mevcut olduğunu kontrol edin
ls -la
```

### 2️⃣ **Smithery'de Yeni Proje Oluşturun**
- Smithery dashboard'a gidin
- "New Project" butonuna tıklayın
- Proje adını girin: `hava-durumu-api`

### 3️⃣ **Dosyaları Upload Edin**
Aşağıdaki dosyaları Smithery'ye yükleyin:
- `app_swagger_fixed.py`
- `requirements.txt`
- `Procfile`
- `runtime.txt`
- `.env` (API anahtarı ile)

### 4️⃣ **Environment Variables Ayarlayın**
Smithery dashboard'da Environment Variables bölümünde:
```
OPENWEATHER_API_KEY=your_actual_api_key_here
FLASK_DEBUG=False
PORT=8080
```
**ÖNEMLİ:** Gerçek API anahtarınızı buraya girin!

### 5️⃣ **Deploy Edin**
- "Deploy" butonuna tıklayın
- Build loglarını takip edin

## 🌐 Deployment Sonrası Erişim

### API Endpoint'leri:
- **Ana Sayfa:** `https://your-app.smithery.io/api/v1/`
- **Swagger UI:** `https://your-app.smithery.io/swagger/`
- **Hava Durumu:** `https://your-app.smithery.io/api/v1/weather?city=Istanbul`

### Test Komutları:
```bash
# Ana sayfa testi
curl https://your-app.smithery.io/api/v1/

# Hava durumu testi
curl "https://your-app.smithery.io/api/v1/weather?city=Istanbul"

# Swagger UI
# Tarayıcıda: https://your-app.smithery.io/swagger/
```

## 🔍 Troubleshooting

### Build Hatası Alırsanız:
1. `requirements.txt` dosyasını kontrol edin
2. Python versiyonunu kontrol edin (`runtime.txt`)
3. Environment variables'ları kontrol edin

### API Çalışmıyorsa:
1. Logs'ları kontrol edin
2. API anahtarının doğru olduğunu kontrol edin
3. Port konfigürasyonunu kontrol edin

### Swagger UI Açılmıyorsa:
1. `/swagger/` endpoint'ine direkt erişim deneyin
2. Browser console'da hata mesajlarını kontrol edin

## 📊 Beklenen Yanıt Formatı

```json
{
  "success": true,
  "city": "İstanbul",
  "country": "TR",
  "message": "İstanbul (TR)'da hava sıcaklığı 18°C (hissedilen 17°C), nem oranı %63, rüzgar hızı 18.5 km/h ve hava durumu: Parçalı Az Bulutlu.",
  "details": {
    "temperature": 18,
    "feels_like": 17,
    "humidity": 63,
    "wind_speed_kmh": 18.5,
    "description": "Parçalı Az Bulutlu",
    "icon": "03d"
  }
}
```

## 🎯 Başarı Kriterleri

✅ Build başarılı
✅ API endpoint'leri erişilebilir
✅ Swagger UI çalışıyor
✅ Hava durumu verileri alınıyor
✅ Türkçe yanıtlar doğru

## 📞 Destek

Sorun yaşarsanız:
1. Smithery logs'larını kontrol edin
2. API anahtarının aktif olduğunu doğrulayın
3. Network bağlantısını test edin

**Başarılı deployment sonrası API'niz 7/24 erişilebilir olacak!** 🌤️
