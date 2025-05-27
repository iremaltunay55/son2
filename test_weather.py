#!/usr/bin/env python3
"""
Hava Durumu API Test Scripti
Bu script API'nin doğru çalışıp çalışmadığını test eder.
"""

import requests
import json
import time

BASE_URL = "http://localhost:5001"

def test_api():
    """API testlerini çalıştır"""
    print("🧪 Hava Durumu API Testleri Başlatılıyor...\n")

    # Test 1: Ana sayfa
    print("1️⃣ Ana sayfa testi...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Ana sayfa çalışıyor")
            print(f"📄 Yanıt: {response.json()['message']}\n")
        else:
            print(f"❌ Ana sayfa hatası: {response.status_code}\n")
    except Exception as e:
        print(f"❌ Ana sayfa bağlantı hatası: {e}\n")

    # Test 2: Geçerli şehir (İstanbul)
    print("2️⃣ İstanbul hava durumu testi...")
    try:
        response = requests.get(f"{BASE_URL}/weather?city=Istanbul")
        if response.status_code == 200:
            data = response.json()
            print("✅ İstanbul verisi alındı")
            print(f"🌡️ {data['message']}\n")
        else:
            print(f"❌ İstanbul testi hatası: {response.status_code}")
            print(f"📄 Hata: {response.json()}\n")
    except Exception as e:
        print(f"❌ İstanbul testi bağlantı hatası: {e}\n")

    # Test 3: Başka bir şehir (Ankara)
    print("3️⃣ Ankara hava durumu testi...")
    try:
        response = requests.get(f"{BASE_URL}/weather?city=Ankara")
        if response.status_code == 200:
            data = response.json()
            print("✅ Ankara verisi alındı")
            print(f"🌡️ {data['message']}\n")
        else:
            print(f"❌ Ankara testi hatası: {response.status_code}")
            print(f"📄 Hata: {response.json()}\n")
    except Exception as e:
        print(f"❌ Ankara testi bağlantı hatası: {e}\n")

    # Test 4: Geçersiz şehir
    print("4️⃣ Geçersiz şehir testi...")
    try:
        response = requests.get(f"{BASE_URL}/weather?city=GeçersizŞehirİsmi123")
        if response.status_code == 404:
            print("✅ Geçersiz şehir doğru şekilde reddedildi")
            print(f"📄 Hata mesajı: {response.json()['error']}\n")
        else:
            print(f"❌ Geçersiz şehir testi beklenmeyen sonuç: {response.status_code}\n")
    except Exception as e:
        print(f"❌ Geçersiz şehir testi bağlantı hatası: {e}\n")

    # Test 5: Boş parametre
    print("5️⃣ Boş parametre testi...")
    try:
        response = requests.get(f"{BASE_URL}/weather")
        if response.status_code == 400:
            print("✅ Boş parametre doğru şekilde reddedildi")
            print(f"📄 Hata mesajı: {response.json()['error']}\n")
        else:
            print(f"❌ Boş parametre testi beklenmeyen sonuç: {response.status_code}\n")
    except Exception as e:
        print(f"❌ Boş parametre testi bağlantı hatası: {e}\n")

    # Test 6: Alternatif URL formatı
    print("6️⃣ Alternatif URL formatı testi...")
    try:
        response = requests.get(f"{BASE_URL}/weather/Izmir")
        if response.status_code == 200:
            data = response.json()
            print("✅ Alternatif URL formatı çalışıyor")
            print(f"🌡️ {data['message']}\n")
        else:
            print(f"❌ Alternatif URL testi hatası: {response.status_code}")
            print(f"📄 Hata: {response.json()}\n")
    except Exception as e:
        print(f"❌ Alternatif URL testi bağlantı hatası: {e}\n")

    print("🏁 Testler tamamlandı!")

def interactive_test():
    """Interaktif test modu"""
    print("🎮 İnteraktif Test Modu")
    print("Çıkmak için 'quit' yazın\n")

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
            response = requests.get(f"{BASE_URL}/weather?city={city}")

            if response.status_code == 200:
                data = response.json()
                print(f"✅ {data['message']}")
                print(f"📊 Detaylar: {json.dumps(data['details'], indent=2, ensure_ascii=False)}\n")
            else:
                error_data = response.json()
                print(f"❌ Hata ({response.status_code}): {error_data['error']}\n")

        except Exception as e:
            print(f"❌ Bağlantı hatası: {e}\n")

if __name__ == "__main__":
    print("🌤️ Hava Durumu API Test Aracı\n")
    print("Seçenekler:")
    print("1. Otomatik testleri çalıştır")
    print("2. İnteraktif test modu")

    choice = input("\nSeçiminiz (1/2): ").strip()

    if choice == "1":
        test_api()
    elif choice == "2":
        interactive_test()
    else:
        print("❌ Geçersiz seçim!")
