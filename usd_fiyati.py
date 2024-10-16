import requests
from bs4 import BeautifulSoup
import json

# Bigpara sayfasından USD fiyatını çekeceğimiz URL
url = 'https://bigpara.hurriyet.com.tr/doviz/dolar/'

# Web sayfasını çekiyoruz
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# USD fiyatını bul (sayfadaki 'span' elementinden 'value' class'ını seçiyoruz)
usd_price_element = soup.find('span', {'class': 'value'})
usd_price_str = usd_price_element.text.strip() if usd_price_element else None

# Binlik ayracı olan noktayı kaldırıyoruz ve virgülü noktaya çeviriyoruz
usd_price_cleaned = usd_price_str.replace('.', '').replace(',', '.') if usd_price_str else None

# USD fiyatını iki ondalık hane ile gösteriyoruz
usd_price = round(float(usd_price_cleaned), 2) if usd_price_cleaned else None

# Fiyatı binlik basamakta nokta, ondalık basamakta virgül olacak şekilde formatlıyoruz
formatted_usd_price = f"{usd_price:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Sonucu ekrana yazdırıyoruz
print(f"Dolar Fiyatı: {formatted_usd_price} TRY")

# Veriyi JSON formatında oluşturuyoruz
data = {
    "USD": formatted_usd_price
}

# Veriyi JSON dosyasına kaydediyoruz
with open('usd_fiyati.json', 'w') as json_file:
    json.dump(data, json_file)

print("USD fiyatı JSON dosyasına kaydedildi.")
