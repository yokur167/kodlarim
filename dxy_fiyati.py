import requests
from bs4 import BeautifulSoup
import json

# Bigpara sayfasından DXY Endeksini çekeceğimiz URL
url = 'https://bigpara.hurriyet.com.tr/borsa/dunya-borsa-endeks-detay-bilgileri/DXY/'

# Web sayfasını çekiyoruz
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# DXY Endeksini bul (sayfadaki 'span' elementinden 'value' class'ını seçiyoruz)
dxy_element = soup.find('span', {'class': 'value'})
dxy_str = dxy_element.text.strip() if dxy_element else None

# Binlik ayracı olan noktayı kaldırıyoruz ve virgülü noktaya çeviriyoruz
dxy_cleaned = dxy_str.replace('.', '').replace(',', '.') if dxy_str else None

# DXY Endeksini iki ondalık hane ile gösteriyoruz
dxy = round(float(dxy_cleaned), 2) if dxy_cleaned else None

# Fiyatı binlik basamakta nokta, ondalık basamakta virgül olacak şekilde formatlıyoruz
formatted_dxy = f"{dxy:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Sonucu ekrana yazdırıyoruz
print(f"DXY Endeksi: {formatted_dxy}")

# Veriyi JSON formatında oluşturuyoruz
data = {
    "DXY": formatted_dxy
}

# Veriyi JSON dosyasına kaydediyoruz
with open('dxy_fiyati.json', 'w') as json_file:
    json.dump(data, json_file)

print("DXY Endeksi JSON dosyasına kaydedildi.")
