import requests
from bs4 import BeautifulSoup
import json

# Bigpara sayfasından çeyrek altın fiyatını çekeceğimiz URL
url = 'https://bigpara.hurriyet.com.tr/altin/ceyrek-altin-fiyati/'

# Web sayfasını çekiyoruz
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Çeyrek altın fiyatını bul (sayfadaki 'span' elementinden 'value' class'ını seçiyoruz)
ceyrek_altin_element = soup.find('span', {'class': 'value'})
ceyrek_altin_price = ceyrek_altin_element.text.strip() if ceyrek_altin_element else 'N/A'

# Sonucu ekrana yazdırıyoruz
print(f"Çeyrek Altın Fiyatı: {ceyrek_altin_price} TRY")

# Veriyi JSON formatında oluşturuyoruz
data = {
    "Ceyrek Altin": ceyrek_altin_price
}

# Veriyi JSON dosyasına kaydediyoruz
with open('ceyrek_altin_price.json', 'w') as json_file:
    json.dump(data, json_file)

print("Çeyrek altın fiyatı JSON dosyasına kaydedildi.")
