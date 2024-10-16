import requests
from bs4 import BeautifulSoup
import json
import os

# Bigpara sayfasından gram altın fiyatını çekeceğimiz URL
url = 'https://bigpara.hurriyet.com.tr/altin/gram-altin-fiyati/'

# Web sayfasını çekiyoruz
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Gram altın fiyatını bul (sayfadaki 'span' elementinden 'value' class'ını seçiyoruz)
gold_price_element = soup.find('span', {'class': 'value'})
gold_price_str = gold_price_element.text.strip() if gold_price_element else None

# Binlik ayracı olan noktayı kaldırıyoruz ve virgülü noktaya çeviriyoruz
gold_price_cleaned = gold_price_str.replace('.', '').replace(',', '.') if gold_price_str else None

# Gram altın fiyatını iki ondalık hane ile gösteriyoruz
gold_price = round(float(gold_price_cleaned), 2) if gold_price_cleaned else None

# Fiyatı binlik basamakta nokta, ondalık basamakta virgül olacak şekilde formatlıyoruz
formatted_gold_price = f"{gold_price:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Sonucu ekrana yazdırıyoruz
print(f"Gram Altın Fiyatı: {formatted_gold_price} TRY")

# Veriyi JSON formatında oluşturuyoruz
data = {
    "Gold": formatted_gold_price
}

# JSON dosyasını proje dizinine kaydediyoruz
file_path = os.path.join(os.getcwd(), 'gold_price.json')

# Veriyi JSON dosyasına kaydetme işlemi (try-except bloğuyla)
try:
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)
    print(f"Gram altın fiyatı JSON dosyasına ({file_path}) olarak kaydedildi.")
except Exception as e:
    print(f"Dosya oluşturulurken bir hata oluştu: {e}")
