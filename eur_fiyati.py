import requests
from bs4 import BeautifulSoup
import json

# Bigpara sayfasından Euro fiyatını çekeceğimiz URL
url = 'https://bigpara.hurriyet.com.tr/doviz/euro/'

# Web sayfasını çekiyoruz
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Euro fiyatını bul (sayfadaki 'span' elementinden 'value' class'ını seçiyoruz)
eur_price_element = soup.find('span', {'class': 'value'})
eur_price_str = eur_price_element.text.strip() if eur_price_element else None

# Binlik ayracı olan noktayı kaldırıyoruz ve virgülü noktaya çeviriyoruz
eur_price_cleaned = eur_price_str.replace('.', '').replace(',', '.') if eur_price_str else None

# Euro fiyatını iki ondalık hane ile gösteriyoruz
eur_price = round(float(eur_price_cleaned), 2) if eur_price_cleaned else None

# Fiyatı binlik basamakta nokta, ondalık basamakta virgül olacak şekilde formatlıyoruz
formatted_eur_price = f"{eur_price:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Sonucu ekrana yazdırıyoruz
print(f"Euro Fiyatı: {formatted_eur_price} TRY")

# Veriyi JSON formatında oluşturuyoruz
data = {
    "EUR": formatted_eur_price
}

# Veriyi JSON dosyasına kaydediyoruz
with open('eur_fiyati.json', 'w') as json_file:
    json.dump(data, json_file)

print("Euro fiyatı JSON dosyasına kaydedildi.")

