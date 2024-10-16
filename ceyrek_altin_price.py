import requests
from bs4 import BeautifulSoup
import json
import os

# Bigpara sayfasından çeyrek altın fiyatını çekeceğimiz URL
url = 'https://bigpara.hurriyet.com.tr/altin/ceyrek-altin-fiyati/'

# Web sayfasını çekiyoruz
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Çeyrek altın fiyatını bul (sayfadaki 'span' elementinden 'value' class'ını seçiyoruz)
quarter_gold_price_element = soup.find('span', {'class': 'value'})
quarter_gold_price_str = quarter_gold_price_element.text.strip() if quarter_gold_price_element else None

# Binlik ayracı olan noktayı kaldırıyoruz ve virgülü noktaya çeviriyoruz
quarter_gold_price_cleaned = quarter_gold_price_str.replace('.', '').replace(',', '.') if quarter_gold_price_str else None

# Çeyrek altın fiyatını iki ondalık hane ile gösteriyoruz
quarter_gold_price = round(float(quarter_gold_price_cleaned), 2) if quarter_gold_price_cleaned else None

# Fiyatı binlik basamakta nokta, ondalık basamakta virgül olacak şekilde formatlıyoruz
formatted_quarter_gold_price = f"{quarter_gold_price:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Sonucu ekrana yazdırıyoruz
print(f"Çeyrek Altın Fiyatı: {formatted_quarter_gold_price} TRY")

# Veriyi JSON formatında oluşturuyoruz
data = {
    "Quarter Gold": formatted_quarter_gold_price
}

# JSON dosyasını proje dizinine kaydediyoruz
file_path = os.path.join(os.getcwd(), 'ceyrek_altin_price.json')

# Veriyi JSON dosyasına kaydetme işlemi (try-except bloğuyla)
try:
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)
    print(f"Çeyrek altın fiyatı JSON dosyasına ({file_path}) olarak kaydedildi.")
except Exception as e:
    print(f"Dosya oluşturulurken bir hata oluştu: {e}")
