# 🌤️ Hava Durumu API Asistanı

Bu proje, OpenWeather API kullanarak şehirlerin güncel hava durumu bilgilerini sağlayan profesyonel bir Flask web servisidir.

## 🚀 Özellikler

- ✅ Güncel hava durumu bilgileri (sıcaklık, nem, rüzgar hızı)
- ✅ Türkçe hava durumu açıklamaları
- ✅ Hissedilen sıcaklık bilgisi
- ✅ **Swagger UI ile interaktif API dokümantasyonu**
- ✅ Kapsamlı hata yönetimi
- ✅ Güvenli API anahtarı saklama
- ✅ RESTful API tasarımı
- ✅ İki farklı endpoint formatı (query ve path parametresi)

## 📋 Gereksinimler

- Python 3.7+
- OpenWeather API anahtarı (ücretsiz)

## 🛠️ Kurulum

1. **Bağımlılıkları yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

2. **API anahtarını ayarlayın:**
   ```bash
   # .env.example dosyasını kopyalayın
   cp .env.example .env

   # .env dosyasını düzenleyin ve API anahtarınızı girin
   # OPENWEATHER_API_KEY=your_actual_api_key_here
   ```
   - [OpenWeather](https://openweathermap.org/api) sitesinden ücretsiz API anahtarı alın
   - API anahtarını `.env` dosyasına yapıştırın

3. **Swagger UI'lı uygulamayı başlatın:**
   ```bash
   python app_swagger.py
   ```

4. **Tarayıcıda test edin:**
   - **Swagger UI (Önerilen):** http://localhost:5001/swagger/
   - Ana sayfa: http://localhost:5001/api/v1/
   - Hava durumu: http://localhost:5001/api/v1/weather?city=Istanbul

## 🌐 API Kullanımı

### 📚 Swagger UI (Önerilen)
En kolay yol: **http://localhost:5001/swagger/** adresini ziyaret edin!
- İnteraktif API dokümantasyonu
- Canlı test örnekleri
- Otomatik kod örnekleri
- Detaylı parametre açıklamaları

### Ana Endpoint'ler
```
GET /api/v1/weather?city=<şehir_ismi>  # Query parametresi
GET /api/v1/weather/<şehir_ismi>       # Path parametresi
```

### Örnekler

**İstanbul için hava durumu (Query):**
```bash
curl "http://localhost:5001/api/v1/weather?city=Istanbul"
```

**Ankara için hava durumu (Path):**
```bash
curl "http://localhost:5001/api/v1/weather/Ankara"
```

**Uluslararası şehir:**
```bash
curl "http://localhost:5001/api/v1/weather?city=London"
```

### Yanıt Formatı

**Başarılı yanıt:**
```json
{
  "success": true,
  "city": "Istanbul",
  "country": "TR",
  "message": "Istanbul (TR)'da hava sıcaklığı 22°C (hissedilen 24°C), nem oranı %65, rüzgar hızı 15.5 km/h ve hava durumu: Açık.",
  "details": {
    "temperature": 22,
    "feels_like": 24,
    "humidity": 65,
    "wind_speed_kmh": 15.5,
    "description": "Açık",
    "icon": "01d"
  }
}
```

**Hata yanıtı:**
```json
{
  "error": "Lütfen geçerli bir şehir ismi giriniz."
}
```

## 🔧 Konfigürasyon

`.env` dosyasında aşağıdaki ayarları yapabilirsiniz:

```env
OPENWEATHER_API_KEY=your_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

## 🛡️ Güvenlik

- ✅ API anahtarı `.env` dosyasında güvenli şekilde saklanır
- ✅ `.gitignore` ile hassas bilgiler GitHub'a yüklenmez
- ✅ `.env.example` dosyası ile güvenli kurulum kılavuzu
- ✅ Timeout ve hata yönetimi mevcuttur
- ⚠️ **ÖNEMLİ:** `.env` dosyasını asla GitHub'a yüklemeyin!

## 📝 Hata Kodları

- `400` - Geçersiz şehir ismi
- `404` - Şehir bulunamadı
- `401` - Geçersiz API anahtarı
- `503` - Bağlantı sorunu
- `504` - Timeout
- `500` - Sunucu hatası

## 🧪 Test

### Swagger UI ile Test (Önerilen)
1. **http://localhost:5001/swagger/** adresini açın
2. İstediğiniz endpoint'i seçin
3. "Try it out" butonuna tıklayın
4. Şehir ismini girin ve "Execute" yapın

### Otomatik Test Scripti
```bash
# Swagger API testleri
python test_swagger.py

# Eski API testleri
python test_weather.py
```

### Manuel Test
```bash
# Geçerli şehir (Query)
curl "http://localhost:5001/api/v1/weather?city=Istanbul"

# Geçerli şehir (Path)
curl "http://localhost:5001/api/v1/weather/Ankara"

# Geçersiz şehir
curl "http://localhost:5001/api/v1/weather?city=GeçersizŞehir"

# Boş parametre
curl "http://localhost:5001/api/v1/weather"
```

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📞 İletişim

Sorularınız için issue açabilirsiniz.

---

**Not:** API anahtarınızı asla public repository'lerde paylaşmayın!
