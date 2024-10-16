import requests
from bs4 import BeautifulSoup
import json

# Bigpara gram altın sayfası URL'si
url = 'https://bigpara.hurriyet.com.tr/altin/gram-altin-fiyati/'

# Web sayfasını çekiyoruz
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Gram altın fiyatını buluyoruz (sayfadaki 'value' class'ına göre)
gold_price_element = soup.find('span', {'class': 'value'})
gold_price_try = gold_price_element.text.strip()

# Sonucu ekrana yazdırıyoruz
print(f"Gram Altın Fiyatı: {gold_price_try} TRY")

# Veriyi JSON formatında oluşturuyoruz
data = {
    "metal": "XAU",
    "currency": "TRY",
    "price": gold_price_try
}

# Veriyi JSON dosyasına kaydediyoruz
with open('gold_price.json', 'w') as json_file:
    json.dump(data, json_file)

print("Altın fiyatı JSON dosyasına kaydedildi.")


