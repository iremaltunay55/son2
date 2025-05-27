import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Ortam değişkenlerini yükle
load_dotenv()

app = Flask(__name__)

# API anahtarını güvenli şekilde al
API_KEY = os.getenv('OPENWEATHER_API_KEY')

if not API_KEY:
    raise ValueError("OPENWEATHER_API_KEY ortam değişkeni bulunamadı! .env dosyasını kontrol edin.")

@app.route('/')
def home():
    """Ana sayfa - API kullanım bilgileri"""
    return jsonify({
        "message": "Hava Durumu API'sine hoş geldiniz!",
        "kullanim": {
            "endpoint": "/weather",
            "method": "GET",
            "parametre": "city (şehir ismi)",
            "ornek": "/weather?city=Istanbul"
        }
    })

@app.route('/weather', methods=['GET'])
def get_weather():
    """Şehir için hava durumu bilgilerini getir"""
    city = request.args.get('city')

    # Şehir ismi kontrolü
    if not city:
        return jsonify({
            "error": "Lütfen geçerli bir şehir ismi giriniz.",
            "ornek": "/weather?city=Istanbul"
        }), 400

    # Şehir ismini temizle
    city = city.strip()
    if len(city) < 2:
        return jsonify({
            "error": "Şehir ismi en az 2 karakter olmalıdır."
        }), 400

    try:
        # OpenWeather API'ye istek gönder
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric',  # Celsius için
            'lang': 'tr'        # Türkçe açıklamalar için
        }

        response = requests.get(url, params=params, timeout=10)

        # API yanıt kontrolü
        if response.status_code == 404:
            return jsonify({
                "error": f"'{city}' şehri bulunamadı. Lütfen şehir ismini kontrol edin."
            }), 404
        elif response.status_code == 401:
            return jsonify({
                "error": "API anahtarı geçersiz."
            }), 401
        elif response.status_code != 200:
            return jsonify({
                "error": f"Hava durumu servisi hatası: {response.status_code}"
            }), 500

        # JSON verisini çözümle
        data = response.json()

        # Hava durumu bilgilerini çıkar
        weather_desc = data['weather'][0]['description'].title()
        temp = round(data['main']['temp'])
        humidity = data['main']['humidity']
        wind_speed = round(data['wind']['speed'] * 3.6, 1)  # m/s'den km/h'ye çevir
        feels_like = round(data['main']['feels_like'])

        # Şehir ismini düzelt (API'den gelen doğru isim)
        city_name = data['name']
        country = data['sys']['country']

        # Türkçe yanıt oluştur
        message = (f"{city_name} ({country})'da hava sıcaklığı {temp}°C "
                  f"(hissedilen {feels_like}°C), nem oranı %{humidity}, "
                  f"rüzgar hızı {wind_speed} km/h ve hava durumu: {weather_desc}.")

        result = {
            "success": True,
            "city": city_name,
            "country": country,
            "message": message,
            "details": {
                "temperature": temp,
                "feels_like": feels_like,
                "humidity": humidity,
                "wind_speed_kmh": wind_speed,
                "description": weather_desc,
                "icon": data['weather'][0]['icon']
            }
        }

        return jsonify(result)

    except requests.exceptions.Timeout:
        return jsonify({
            "error": "Hava durumu servisi yanıt vermiyor. Lütfen daha sonra tekrar deneyin."
        }), 504
    except requests.exceptions.ConnectionError:
        return jsonify({
            "error": "İnternet bağlantısı sorunu. Lütfen bağlantınızı kontrol edin."
        }), 503
    except Exception as e:
        return jsonify({
            "error": f"Beklenmeyen bir hata oluştu: {str(e)}"
        }), 500

@app.route('/weather/<city>', methods=['GET'])
def get_weather_by_path(city):
    """URL path'i ile şehir hava durumu (alternatif endpoint)"""
    # Query parametresi olarak işle
    request.args = request.args.copy()
    request.args = request.args.to_dict()
    request.args['city'] = city

    # Ana weather fonksiyonunu çağır
    return get_weather()

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint bulunamadı.",
        "available_endpoints": ["/", "/weather", "/weather/<city>"]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Sunucu hatası oluştu."
    }), 500

if __name__ == '__main__':
    port = 5001  # Farklı port kullan
    print("🌤️  Hava Durumu API'si başlatılıyor...")
    print(f"📍 Ana sayfa: http://localhost:{port}")
    print(f"🌡️  Hava durumu: http://localhost:{port}/weather?city=Istanbul")
    print("🔄 Çıkmak için Ctrl+C")

    app.run(
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true',
        host='0.0.0.0',
        port=port
    )
