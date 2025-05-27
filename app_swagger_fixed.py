import os
import requests
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields, reqparse
from dotenv import load_dotenv

# Ortam değişkenlerini yükle
load_dotenv()

# Flask uygulaması oluştur
app = Flask(__name__)

# Swagger UI için API oluştur
api = Api(
    app,
    version='1.0',
    title='🌤️ Hava Durumu API',
    description='OpenWeather API kullanarak şehirlerin güncel hava durumu bilgilerini sağlayan RESTful API servisi.',
    doc='/swagger/',
    prefix='/api/v1'
)

# API anahtarını güvenli şekilde al
API_KEY = os.getenv('OPENWEATHER_API_KEY')

if not API_KEY:
    raise ValueError("OPENWEATHER_API_KEY ortam değişkeni bulunamadı! .env dosyasını kontrol edin.")

# Namespace oluştur
weather_ns = api.namespace('weather', description='Hava durumu işlemleri')

# Response modelleri tanımla
weather_details = api.model('WeatherDetails', {
    'temperature': fields.Integer(description='Sıcaklık (°C)', example=18),
    'feels_like': fields.Integer(description='Hissedilen sıcaklık (°C)', example=17),
    'humidity': fields.Integer(description='Nem oranı (%)', example=63),
    'wind_speed_kmh': fields.Float(description='Rüzgar hızı (km/h)', example=18.5),
    'description': fields.String(description='Hava durumu açıklaması', example='Parçalı Az Bulutlu'),
    'icon': fields.String(description='Hava durumu ikonu kodu', example='03d')
})

weather_response = api.model('WeatherResponse', {
    'success': fields.Boolean(description='İşlem başarı durumu', example=True),
    'city': fields.String(description='Şehir adı', example='İstanbul'),
    'country': fields.String(description='Ülke kodu', example='TR'),
    'message': fields.String(description='Türkçe hava durumu mesajı'),
    'details': fields.Nested(weather_details, description='Detaylı hava durumu bilgileri')
})

error_response = api.model('ErrorResponse', {
    'error': fields.String(description='Hata mesajı', example='Lütfen geçerli bir şehir ismi giriniz.')
})

# Parser tanımla
weather_parser = reqparse.RequestParser()
weather_parser.add_argument('city', type=str, required=True, help='Şehir adı (örn: Istanbul, Ankara)', location='args')

# Ana sayfa endpoint'i
@api.route('/')
class Home(Resource):
    def get(self):
        """API ana sayfası ve kullanım bilgileri"""
        return {
            'message': 'Hava Durumu API\'sine hoş geldiniz!',
            'swagger_ui': '/swagger/',
            'endpoints': {
                '/api/v1/weather': 'GET - Hava durumu sorgulama',
                '/swagger/': 'GET - API dokümantasyonu'
            }
        }

# Hava durumu endpoint'i
@weather_ns.route('')
class Weather(Resource):
    @api.expect(weather_parser)
    @api.marshal_with(weather_response, code=200)
    @api.response(400, 'Geçersiz parametre', error_response)
    @api.response(404, 'Şehir bulunamadı', error_response)
    @api.response(500, 'Sunucu hatası', error_response)
    def get(self):
        """Şehir için güncel hava durumu bilgilerini getir

        Bu endpoint, belirtilen şehir için OpenWeather API'den güncel hava durumu bilgilerini alır.
        Türkçe açıklamalar ve metrik birimler (°C, km/h) kullanır.
        """
        args = weather_parser.parse_args()
        city = args['city']

        # Şehir ismini temizle
        if not city or len(city.strip()) < 2:
            api.abort(400, 'Lütfen geçerli bir şehir ismi giriniz.')

        city = city.strip()

        try:
            # OpenWeather API'ye istek gönder
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': city,
                'appid': API_KEY,
                'units': 'metric',
                'lang': 'tr'
            }

            response = requests.get(url, params=params, timeout=10)

            # API yanıt kontrolü
            if response.status_code == 404:
                api.abort(404, f"'{city}' şehri bulunamadı. Lütfen şehir ismini kontrol edin.")
            elif response.status_code == 401:
                api.abort(500, "API anahtarı geçersiz.")
            elif response.status_code != 200:
                api.abort(500, f"Hava durumu servisi hatası: {response.status_code}")

            # JSON verisini çözümle
            data = response.json()

            # Hava durumu bilgilerini çıkar
            weather_desc = data['weather'][0]['description'].title()
            temp = round(data['main']['temp'])
            humidity = data['main']['humidity']
            wind_speed = round(data['wind']['speed'] * 3.6, 1)
            feels_like = round(data['main']['feels_like'])

            # Şehir ismini düzelt
            city_name = data['name']
            country = data['sys']['country']

            # Türkçe yanıt oluştur
            message = (f"{city_name} ({country})'da hava sıcaklığı {temp}°C "
                      f"(hissedilen {feels_like}°C), nem oranı %{humidity}, "
                      f"rüzgar hızı {wind_speed} km/h ve hava durumu: {weather_desc}.")

            return {
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

        except requests.exceptions.Timeout:
            api.abort(504, "Hava durumu servisi yanıt vermiyor. Lütfen daha sonra tekrar deneyin.")
        except requests.exceptions.ConnectionError:
            api.abort(503, "İnternet bağlantısı sorunu. Lütfen bağlantınızı kontrol edin.")
        except Exception as e:
            api.abort(500, f"Beklenmeyen bir hata oluştu: {str(e)}")

# Şehir adı ile direkt erişim endpoint'i
@weather_ns.route('/<string:city>')
class WeatherByCity(Resource):
    @api.marshal_with(weather_response, code=200)
    @api.response(404, 'Şehir bulunamadı', error_response)
    @api.response(500, 'Sunucu hatası', error_response)
    def get(self, city):
        """URL path'i ile şehir hava durumu

        Alternatif endpoint: Şehir adını URL'de parametre olarak geçirin.
        """
        # Şehir ismini temizle
        if not city or len(city.strip()) < 2:
            api.abort(400, 'Lütfen geçerli bir şehir ismi giriniz.')

        city = city.strip()

        try:
            # OpenWeather API'ye istek gönder
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': city,
                'appid': API_KEY,
                'units': 'metric',
                'lang': 'tr'
            }

            response = requests.get(url, params=params, timeout=10)

            # API yanıt kontrolü
            if response.status_code == 404:
                api.abort(404, f"'{city}' şehri bulunamadı. Lütfen şehir ismini kontrol edin.")
            elif response.status_code == 401:
                api.abort(500, "API anahtarı geçersiz.")
            elif response.status_code != 200:
                api.abort(500, f"Hava durumu servisi hatası: {response.status_code}")

            # JSON verisini çözümle
            data = response.json()

            # Hava durumu bilgilerini çıkar
            weather_desc = data['weather'][0]['description'].title()
            temp = round(data['main']['temp'])
            humidity = data['main']['humidity']
            wind_speed = round(data['wind']['speed'] * 3.6, 1)
            feels_like = round(data['main']['feels_like'])

            # Şehir ismini düzelt
            city_name = data['name']
            country = data['sys']['country']

            # Türkçe yanıt oluştur
            message = (f"{city_name} ({country})'da hava sıcaklığı {temp}°C "
                      f"(hissedilen {feels_like}°C), nem oranı %{humidity}, "
                      f"rüzgar hızı {wind_speed} km/h ve hava durumu: {weather_desc}.")

            return {
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

        except requests.exceptions.Timeout:
            api.abort(504, "Hava durumu servisi yanıt vermiyor. Lütfen daha sonra tekrar deneyin.")
        except requests.exceptions.ConnectionError:
            api.abort(503, "İnternet bağlantısı sorunu. Lütfen bağlantınızı kontrol edin.")
        except Exception as e:
            api.abort(500, f"Beklenmeyen bir hata oluştu: {str(e)}")

if __name__ == '__main__':
    # Smithery için port konfigürasyonu
    port = int(os.getenv('PORT', 5001))

    print("🌤️  Hava Durumu API'si (Düzeltilmiş Swagger UI ile) başlatılıyor...")
    print(f"📍 Ana sayfa: http://localhost:{port}/api/v1/")
    print(f"📚 Swagger UI: http://localhost:{port}/swagger/")
    print(f"🌡️  Hava durumu: http://localhost:{port}/api/v1/weather?city=Istanbul")
    print("🔄 Çıkmak için Ctrl+C")

    app.run(
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true',
        host='0.0.0.0',
        port=port
    )
