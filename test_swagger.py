#!/usr/bin/env python3
"""
Swagger UI'lı Hava Durumu API Test Scripti
Bu script yeni API endpoint'lerini test eder.
"""

import requests
import json
import time

BASE_URL = "http://localhost:5001"
API_BASE = f"{BASE_URL}/api/v1"

def test_swagger_api():
    """Swagger UI'lı API testlerini çalıştır"""
    print("🧪 Swagger UI'lı Hava Durumu API Testleri Başlatılıyor...\n")
    
    # Test 1: Ana sayfa
    print("1️⃣ Ana sayfa testi...")
    try:
        response = requests.get(f"{API_BASE}/")
        if response.status_code == 200:
            print("✅ Ana sayfa çalışıyor")
            data = response.json()
            print(f"📄 Yanıt: {data['message']}")
            print(f"📚 Swagger UI: {BASE_URL}{data['swagger_ui']}\n")
        else:
            print(f"❌ Ana sayfa hatası: {response.status_code}\n")
    except Exception as e:
        print(f"❌ Ana sayfa bağlantı hatası: {e}\n")
    
    # Test 2: Swagger UI erişimi
    print("2️⃣ Swagger UI erişim testi...")
    try:
        response = requests.get(f"{BASE_URL}/swagger/")
        if response.status_code == 200:
            print("✅ Swagger UI erişilebilir")
            print(f"📚 Swagger UI: {BASE_URL}/swagger/\n")
        else:
            print(f"❌ Swagger UI hatası: {response.status_code}\n")
    except Exception as e:
        print(f"❌ Swagger UI bağlantı hatası: {e}\n")
    
    # Test 3: Geçerli şehir (İstanbul)
    print("3️⃣ İstanbul hava durumu testi...")
    try:
        response = requests.get(f"{API_BASE}/weather?city=Istanbul")
        if response.status_code == 200:
            data = response.json()
            print("✅ İstanbul verisi alındı")
            print(f"🌡️ {data['message']}")
            print(f"📊 Sıcaklık: {data['details']['temperature']}°C")
            print(f"💨 Rüzgar: {data['details']['wind_speed_kmh']} km/h\n")
        else:
            print(f"❌ İstanbul testi hatası: {response.status_code}")
            print(f"📄 Hata: {response.json()}\n")
    except Exception as e:
        print(f"❌ İstanbul testi bağlantı hatası: {e}\n")
    
    # Test 4: Başka bir şehir (Ankara)
    print("4️⃣ Ankara hava durumu testi...")
    try:
        response = requests.get(f"{API_BASE}/weather?city=Ankara")
        if response.status_code == 200:
            data = response.json()
            print("✅ Ankara verisi alındı")
            print(f"🌡️ {data['message']}\n")
        else:
            print(f"❌ Ankara testi hatası: {response.status_code}")
            print(f"📄 Hata: {response.json()}\n")
    except Exception as e:
        print(f"❌ Ankara testi bağlantı hatası: {e}\n")
    
    # Test 5: Path parametresi ile şehir
    print("5️⃣ Path parametresi testi (İzmir)...")
    try:
        response = requests.get(f"{API_BASE}/weather/Izmir")
        if response.status_code == 200:
            data = response.json()
            print("✅ Path parametresi çalışıyor")
            print(f"🌡️ {data['message']}\n")
        else:
            print(f"❌ Path parametresi testi hatası: {response.status_code}")
            print(f"📄 Hata: {response.json()}\n")
    except Exception as e:
        print(f"❌ Path parametresi testi bağlantı hatası: {e}\n")
    
    # Test 6: Geçersiz şehir
    print("6️⃣ Geçersiz şehir testi...")
    try:
        response = requests.get(f"{API_BASE}/weather?city=GeçersizŞehirİsmi123")
        if response.status_code == 404:
            print("✅ Geçersiz şehir doğru şekilde reddedildi")
            data = response.json()
            print(f"📄 Hata mesajı: {data['message']}\n")
        else:
            print(f"❌ Geçersiz şehir testi beklenmeyen sonuç: {response.status_code}\n")
    except Exception as e:
        print(f"❌ Geçersiz şehir testi bağlantı hatası: {e}\n")
    
    # Test 7: Boş parametre
    print("7️⃣ Boş parametre testi...")
    try:
        response = requests.get(f"{API_BASE}/weather")
        if response.status_code == 400:
            print("✅ Boş parametre doğru şekilde reddedildi")
            data = response.json()
            print(f"📄 Hata mesajı: {data['message']}\n")
        else:
            print(f"❌ Boş parametre testi beklenmeyen sonuç: {response.status_code}\n")
    except Exception as e:
        print(f"❌ Boş parametre testi bağlantı hatası: {e}\n")
    
    # Test 8: Uluslararası şehir
    print("8️⃣ Uluslararası şehir testi (London)...")
    try:
        response = requests.get(f"{API_BASE}/weather?city=London")
        if response.status_code == 200:
            data = response.json()
            print("✅ Uluslararası şehir verisi alındı")
            print(f"🌡️ {data['message']}\n")
        else:
            print(f"❌ London testi hatası: {response.status_code}")
            print(f"📄 Hata: {response.json()}\n")
    except Exception as e:
        print(f"❌ London testi bağlantı hatası: {e}\n")
    
    print("🏁 Swagger API testleri tamamlandı!")
    print(f"📚 Swagger UI'yi tarayıcıda görüntülemek için: {BASE_URL}/swagger/")

def interactive_swagger_test():
    """İnteraktif test modu"""
    print("🎮 İnteraktif Swagger API Test Modu")
    print("Çıkmak için 'quit' yazın")
    print(f"📚 Swagger UI: {BASE_URL}/swagger/\n")
    
    while True:
        city = input("🏙️ Şehir ismi girin: ").strip()
        
        if city.lower() in ['quit', 'exit', 'q']:
            print("👋 Test modu sonlandırıldı!")
            break
        
        if not city:
            print("❌ Lütfen bir şehir ismi girin!\n")
            continue
        
        try:
            print(f"🔍 {city} için hava durumu sorgulanıyor...")
            
            # Query parametresi ile test
            response = requests.get(f"{API_BASE}/weather?city={city}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {data['message']}")
                print(f"📊 Detaylar:")
                print(f"   🌡️  Sıcaklık: {data['details']['temperature']}°C")
                print(f"   🤗 Hissedilen: {data['details']['feels_like']}°C")
                print(f"   💧 Nem: %{data['details']['humidity']}")
                print(f"   💨 Rüzgar: {data['details']['wind_speed_kmh']} km/h")
                print(f"   ☁️  Durum: {data['details']['description']}")
                print(f"   🏙️  Şehir: {data['city']} ({data['country']})")
                
                # Path parametresi ile de test et
                print(f"\n🔄 Path parametresi ile test ediliyor...")
                path_response = requests.get(f"{API_BASE}/weather/{city}")
                if path_response.status_code == 200:
                    print(f"✅ Path parametresi de çalışıyor!")
                else:
                    print(f"⚠️ Path parametresi hatası: {path_response.status_code}")
                
            else:
                error_data = response.json()
                print(f"❌ Hata ({response.status_code}): {error_data.get('message', 'Bilinmeyen hata')}")
                
        except Exception as e:
            print(f"❌ Bağlantı hatası: {e}")
        
        print()  # Boş satır

def show_api_info():
    """API bilgilerini göster"""
    print("📚 Swagger UI'lı Hava Durumu API Bilgileri")
    print("=" * 50)
    print(f"🌐 Ana URL: {BASE_URL}")
    print(f"📚 Swagger UI: {BASE_URL}/swagger/")
    print(f"🔗 API Base: {API_BASE}")
    print()
    print("📋 Endpoint'ler:")
    print(f"   GET {API_BASE}/                     - Ana sayfa")
    print(f"   GET {API_BASE}/weather?city=<şehir> - Hava durumu (query)")
    print(f"   GET {API_BASE}/weather/<şehir>      - Hava durumu (path)")
    print(f"   GET {BASE_URL}/swagger/             - API dokümantasyonu")
    print()
    print("💡 Örnek kullanım:")
    print(f"   curl \"{API_BASE}/weather?city=Istanbul\"")
    print(f"   curl \"{API_BASE}/weather/Ankara\"")
    print()

if __name__ == "__main__":
    show_api_info()
    
    print("Seçenekler:")
    print("1. Otomatik testleri çalıştır")
    print("2. İnteraktif test modu")
    print("3. Sadece bilgileri göster")
    
    choice = input("\nSeçiminiz (1/2/3): ").strip()
    
    if choice == "1":
        test_swagger_api()
    elif choice == "2":
        interactive_swagger_test()
    elif choice == "3":
        print("ℹ️ API bilgileri yukarıda gösterildi.")
    else:
        print("❌ Geçersiz seçim!")
