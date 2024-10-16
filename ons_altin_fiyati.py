import requests
from bs4 import BeautifulSoup
import json
import os

# Bigpara sayfasından ons altın fiyatını çekeceğimiz URL
url = 'https://bigpara.hurriyet.com.tr/altin/altin-ons-fiyati/'

# Web sayfasını çekiyoruz
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Ons altın fiyatını bul (sayfadaki 'span' elementinden 'value' class'ını seçiyoruz)
ons_gold_price_element = soup.find('span', {'class': 'value'})
ons_gold_price_str = ons_gold_price_element.text.strip() if ons_gold_price_element else None

# Binlik ayracı olan noktayı kaldırıyoruz ve virgülü noktaya çeviriyoruz
ons_gold_price_cleaned = ons_gold_price_str.replace('.', '').replace(',', '.') if ons_gold_price_str else None

# Ons altın fiyatını iki ondalık hane ile gösteriyoruz
ons_gold_price = round(float(ons_gold_price_cleaned), 2) if ons_gold_price_cleaned else None

# Fiyatı binlik basamakta nokta, ondalık basamakta virgül olacak şekilde formatlıyoruz
formatted_ons_gold_price = f"{ons_gold_price:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Sonucu ekrana yazdırıyoruz
print(f"Ons Altın Fiyatı: {formatted_ons_gold_price} USD")

# Veriyi JSON formatında oluşturuyoruz
data = {
    "Ons Gold": formatted_ons_gold_price
}

# JSON dosyasını proje dizinine kaydediyoruz
file_path = os.path.join(os.getcwd(), 'ons_altin_fiyati.json')

# Veriyi JSON dosyasına kaydetme işlemi (try-except bloğuyla)
try:
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)
    print(f"Ons altın fiyatı JSON dosyasına ({file_path}) olarak kaydedildi.")
except Exception as e:
    print(f"Dosya oluşturulurken bir hata oluştu: {e}")
