import requests
from bs4 import BeautifulSoup
import json
import os

# Bigpara sayfasından DXY fiyatını çekeceğimiz URL
url = 'https://bigpara.hurriyet.com.tr/borsa/dunya-borsa-endeks-detay-bilgileri/DXY/'

# Web sayfasını çekiyoruz
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# DXY fiyatını bul (sayfadaki 'span' elementinden 'value' class'ını seçiyoruz)
dxy_price_element = soup.find('span', {'class': 'value'})
dxy_price_str = dxy_price_element.text.strip() if dxy_price_element else None

# Binlik ayracı olan noktayı kaldırıyoruz ve virgülü noktaya çeviriyoruz
dxy_price_cleaned = dxy_price_str.replace('.', '').replace(',', '.') if dxy_price_str else None

# DXY fiyatını iki ondalık hane ile gösteriyoruz
dxy_price = round(float(dxy_price_cleaned), 2) if dxy_price_cleaned else None

# Fiyatı binlik basamakta nokta, ondalık basamakta virgül olacak şekilde formatlıyoruz
formatted_dxy_price = f"{dxy_price:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Sonucu ekrana yazdırıyoruz
print(f"DXY Fiyatı: {formatted_dxy_price} USD")

# Veriyi JSON formatında oluşturuyoruz
data = {
    "DXY": formatted_dxy_price
}

# JSON dosyasını proje dizinine kaydediyoruz
file_path = os.path.join(os.getcwd(), 'dxy_fiyati.json')

# Veriyi JSON dosyasına kaydetme işlemi (try-except bloğuyla)
try:
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)
    print(f"DXY fiyatı JSON dosyasına ({file_path}) olarak kaydedildi.")
except Exception as e:
    print(f"Dosya oluşturulurken bir hata oluştu: {e}")
