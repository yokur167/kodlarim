import requests
from bs4 import BeautifulSoup
import json

# Bigpara sayfasından Altın Ons fiyatını çekeceğimiz URL
url = 'https://bigpara.hurriyet.com.tr/altin/altin-ons-fiyati/'

# Web sayfasını çekiyoruz
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Altın ons fiyatını bul (sayfadaki 'span' elementinden 'value' class'ını seçiyoruz)
ons_altin_element = soup.find('span', {'class': 'value'})
ons_altin_str = ons_altin_element.text.strip() if ons_altin_element else None

# Binlik ayracı olan noktayı kaldırıyoruz ve virgülü noktaya çeviriyoruz
ons_altin_cleaned = ons_altin_str.replace('.', '').replace(',', '.') if ons_altin_str else None

# Altın ons fiyatını iki ondalık hane ile gösteriyoruz
ons_altin = round(float(ons_altin_cleaned), 2) if ons_altin_cleaned else None

# Fiyatı binlik basamakta nokta, ondalık basamakta virgül olacak şekilde formatlıyoruz
formatted_ons_altin = f"{ons_altin:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Sonucu ekrana yazdırıyoruz
print(f"Altın Ons Fiyatı: {formatted_ons_altin} USD")

# Veriyi JSON formatında oluşturuyoruz
data = {
    "Altin Ons": formatted_ons_altin
}

# Veriyi JSON dosyasına kaydediyoruz
with open('ons_altin_fiyati.json', 'w') as json_file:
    json.dump(data, json_file)

print("Altın ons fiyatı JSON dosyasına kaydedildi.")

