import requests
from bs4 import BeautifulSoup
import json

# Bigpara sayfasından 22 ayar bilezik fiyatını çekeceğimiz URL
url = 'https://bigpara.hurriyet.com.tr/altin/22-ayar-bilezik-fiyati/'

# Web sayfasını çekiyoruz
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# 22 ayar bilezik fiyatını bul (sayfadaki 'span' elementinden 'value' class'ını seçiyoruz)
bilezik_fiyati_element = soup.find('span', {'class': 'value'})
bilezik_fiyati_price = bilezik_fiyati_element.text.strip() if bilezik_fiyati_element else 'N/A'

# Sonucu ekrana yazdırıyoruz
print(f"22 Ayar Bilezik Fiyatı: {bilezik_fiyati_price} TRY")

# Veriyi JSON formatında oluşturuyoruz
data = {
    "22 Ayar Bilezik": bilezik_fiyati_price
}

# Veriyi JSON dosyasına kaydediyoruz
with open('bilezik_fiyati.json', 'w') as json_file:
    json.dump(data, json_file)

print("22 Ayar Bilezik fiyatı JSON dosyasına kaydedildi.")

