import os
import requests
from flask import Flask
from flask_restx import Api, Resource, fields
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
    doc='/swagger/',  # Swagger UI endpoint'i
    prefix='/api/v1'
)

# API anahtarını güvenli şekilde al
API_KEY = os.getenv('OPENWEATHER_API_KEY')

if not API_KEY:
    raise ValueError("OPENWEATHER_API_KEY ortam değişkeni bulunamadı! .env dosyasını kontrol edin.")

# Namespace oluştur
weather_ns = api.namespace('weather', description='Hava durumu işlemleri')

# Response modelleri tanımla
weather_details_model = api.model('WeatherDetails', {
    'temperature': fields.Integer(description='Sıcaklık (°C)', example=18),
    'feels_like': fields.Integer(description='Hissedilen sıcaklık (°C)', example=17),
    'humidity': fields.Integer(description='Nem oranı (%)', example=63),
    'wind_speed_kmh': fields.Float(description='Rüzgar hızı (km/h)', example=18.5),
    'description': fields.String(description='Hava durumu açıklaması', example='Parçalı Az Bulutlu'),
    'icon': fields.String(description='Hava durumu ikonu kodu', example='03d')
})

weather_response_model = api.model('WeatherResponse', {
    'success': fields.Boolean(description='İşlem başarı durumu', example=True),
    'city': fields.String(description='Şehir adı', example='İstanbul'),
    'country': fields.String(description='Ülke kodu', example='TR'),
    'message': fields.String(description='Türkçe hava durumu mesajı', 
                           example='İstanbul (TR)\'da hava sıcaklığı 18°C (hissedilen 17°C), nem oranı %63, rüzgar hızı 18.5 km/h ve hava durumu: Parçalı Az Bulutlu.'),
    'details': fields.Nested(weather_details_model, description='Detaylı hava durumu bilgileri')
})

error_model = api.model('Error', {
    'error': fields.String(description='Hata mesajı', example='Lütfen geçerli bir şehir ismi giriniz.')
})

# Ana sayfa endpoint'i
@api.route('/')
class Home(Resource):
    @api.doc('home')
    @api.response(200, 'Başarılı', fields.Raw({
        'message': fields.String(example='Hava Durumu API\'sine hoş geldiniz!'),
        'swagger_ui': fields.String(example='/swagger/'),
        'endpoints': fields.Raw({
            '/api/v1/weather': fields.String(example='GET - Hava durumu sorgulama'),
            '/swagger/': fields.String(example='GET - API dokümantasyonu')
        })
    }))
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
    @api.doc('get_weather')
    @api.param('city', 'Şehir adı (örn: Istanbul, Ankara, Izmir)', required=True, type='string')
    @api.response(200, 'Başarılı', weather_response_model)
    @api.response(400, 'Geçersiz parametre', error_model)
    @api.response(404, 'Şehir bulunamadı', error_model)
    @api.response(500, 'Sunucu hatası', error_model)
    def get(self):
        """Şehir için güncel hava durumu bilgilerini getir
        
        Bu endpoint, belirtilen şehir için OpenWeather API'den güncel hava durumu bilgilerini alır.
        Türkçe açıklamalar ve metrik birimler (°C, km/h) kullanır.
        
        Örnek kullanım:
        - /api/v1/weather?city=Istanbul
        - /api/v1/weather?city=Ankara
        - /api/v1/weather?city=London
        """
        from flask import request
        
        city = request.args.get('city')
        
        # Şehir ismi kontrolü
        if not city:
            api.abort(400, 'Lütfen geçerli bir şehir ismi giriniz.')
        
        # Şehir ismini temizle
        city = city.strip()
        if len(city) < 2:
            api.abort(400, 'Şehir ismi en az 2 karakter olmalıdır.')
        
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
            
            return result
            
        except requests.exceptions.Timeout:
            api.abort(504, "Hava durumu servisi yanıt vermiyor. Lütfen daha sonra tekrar deneyin.")
        except requests.exceptions.ConnectionError:
            api.abort(503, "İnternet bağlantısı sorunu. Lütfen bağlantınızı kontrol edin.")
        except Exception as e:
            api.abort(500, f"Beklenmeyen bir hata oluştu: {str(e)}")

# Şehir adı ile direkt erişim endpoint'i
@weather_ns.route('/<string:city>')
class WeatherByCity(Resource):
    @api.doc('get_weather_by_city')
    @api.param('city', 'Şehir adı', _in='path', required=True)
    @api.response(200, 'Başarılı', weather_response_model)
    @api.response(404, 'Şehir bulunamadı', error_model)
    @api.response(500, 'Sunucu hatası', error_model)
    def get(self, city):
        """URL path'i ile şehir hava durumu
        
        Alternatif endpoint: Şehir adını URL'de parametre olarak geçirin.
        
        Örnek kullanım:
        - /api/v1/weather/Istanbul
        - /api/v1/weather/Ankara
        - /api/v1/weather/London
        """
        from flask import request
        
        # Query parametresi olarak işle
        request.args = request.args.copy()
        if hasattr(request.args, 'to_dict'):
            args_dict = request.args.to_dict()
        else:
            args_dict = dict(request.args)
        args_dict['city'] = city
        
        # Mock request args
        class MockArgs:
            def __init__(self, args_dict):
                self._args = args_dict
            def get(self, key, default=None):
                return self._args.get(key, default)
        
        # Geçici olarak args'ı değiştir
        original_args = request.args
        request.args = MockArgs(args_dict)
        
        try:
            # Weather endpoint'ini çağır
            weather_resource = Weather()
            return weather_resource.get()
        finally:
            # Args'ı geri yükle
            request.args = original_args

if __name__ == '__main__':
    port = 5001
    print("🌤️  Hava Durumu API'si (Swagger UI ile) başlatılıyor...")
    print(f"📍 Ana sayfa: http://localhost:{port}/api/v1/")
    print(f"📚 Swagger UI: http://localhost:{port}/swagger/")
    print(f"🌡️  Hava durumu: http://localhost:{port}/api/v1/weather?city=Istanbul")
    print("🔄 Çıkmak için Ctrl+C")
    
    app.run(
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true',
        host='0.0.0.0',
        port=port
    )
