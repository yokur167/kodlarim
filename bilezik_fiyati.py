import requests
from bs4 import BeautifulSoup
import json
import os

# Bigpara sayfasından 22 ayar bilezik fiyatını çekeceğimiz URL
url = 'https://bigpara.hurriyet.com.tr/altin/22-ayar-bilezik-fiyati/'

# Web sayfasını çekiyoruz
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# 22 ayar bilezik fiyatını bul (sayfadaki 'span' elementinden 'value' class'ını seçiyoruz)
bracelet_price_element = soup.find('span', {'class': 'value'})
bracelet_price_str = bracelet_price_element.text.strip() if bracelet_price_element else None

# Binlik ayracı olan noktayı kaldırıyoruz ve virgülü noktaya çeviriyoruz
bracelet_price_cleaned = bracelet_price_str.replace('.', '').replace(',', '.') if bracelet_price_str else None

# Bilezik fiyatını iki ondalık hane ile gösteriyoruz
bracelet_price = round(float(bracelet_price_cleaned), 2) if bracelet_price_cleaned else None

# Fiyatı binlik basamakta nokta, ondalık basamakta virgül olacak şekilde formatlıyoruz
formatted_bracelet_price = f"{bracelet_price:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Sonucu ekrana yazdırıyoruz
print(f"22 Ayar Bilezik Fiyatı: {formatted_bracelet_price} TRY")

# Veriyi JSON formatında oluşturuyoruz
data = {
    "Bracelet": formatted_bracelet_price
}

# JSON dosyasını proje dizinine kaydediyoruz
file_path = os.path.join(os.getcwd(), 'bilezik_fiyati.json')

# Veriyi JSON dosyasına kaydetme işlemi (try-except bloğuyla)
try:
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)
    print(f"22 Ayar bilezik fiyatı JSON dosyasına ({file_path}) olarak kaydedildi.")
except Exception as e:
    print(f"Dosya oluşturulurken bir hata oluştu: {e}")
