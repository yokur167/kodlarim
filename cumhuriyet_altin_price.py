import requests
from bs4 import BeautifulSoup
import json
import os

# Bigpara sayfasından Cumhuriyet altını fiyatını çekeceğimiz URL
url = 'https://bigpara.hurriyet.com.tr/altin/cumhuriyet-altini-fiyati/'

# Web sayfasını çekiyoruz
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Cumhuriyet altını fiyatını bul (sayfadaki 'span' elementinden 'value' class'ını seçiyoruz)
republic_gold_price_element = soup.find('span', {'class': 'value'})
republic_gold_price_str = republic_gold_price_element.text.strip() if republic_gold_price_element else None

# Binlik ayracı olan noktayı kaldırıyoruz ve virgülü noktaya çeviriyoruz
republic_gold_price_cleaned = republic_gold_price_str.replace('.', '').replace(',', '.') if republic_gold_price_str else None

# Cumhuriyet altını fiyatını iki ondalık hane ile gösteriyoruz
republic_gold_price = round(float(republic_gold_price_cleaned), 2) if republic_gold_price_cleaned else None

# Fiyatı binlik basamakta nokta, ondalık basamakta virgül olacak şekilde formatlıyoruz
formatted_republic_gold_price = f"{republic_gold_price:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Sonucu ekrana yazdırıyoruz
print(f"Cumhuriyet Altını Fiyatı: {formatted_republic_gold_price} TRY")

# Veriyi JSON formatında oluşturuyoruz
data = {
    "Republic Gold": formatted_republic_gold_price
}

# JSON dosyasını proje dizinine kaydediyoruz
file_path = os.path.join(os.getcwd(), 'cumhuriyet_altin_price.json')

# Veriyi JSON dosyasına kaydetme işlemi (try-except bloğuyla)
try:
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)
    print(f"Cumhuriyet altını fiyatı JSON dosyasına ({file_path}) olarak kaydedildi.")
except Exception as e:
    print(f"Dosya oluşturulurken bir hata oluştu: {e}")
