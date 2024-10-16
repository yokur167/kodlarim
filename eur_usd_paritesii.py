import requests
import json
import os

# API'den EUR/USD paritesini çekmek için URL
url = 'https://api.frankfurter.app/latest?base=EUR&symbols=USD'

# Web sayfasını çekiyoruz
response = requests.get(url)

# Veriyi JSON formatında alıyoruz
data = response.json()

# EUR/USD paritesi verisini alıyoruz
eur_usd_rate = data['rates']['USD']

# Pariteyi iki ondalık hane ile gösteriyoruz
formatted_eur_usd_rate = f"{eur_usd_rate:.2f}"

# Sonucu ekrana yazdırıyoruz
print(f"EUR/USD Paritesi: {formatted_eur_usd_rate}")

# Veriyi JSON formatında oluşturuyoruz
data_to_save = {
    "EUR_USD": formatted_eur_usd_rate
}

# JSON dosyasını proje dizinine kaydediyoruz
file_path = os.path.join(os.getcwd(), 'eur_usd_paritesii.json')

# Veriyi JSON dosyasına kaydetme işlemi (try-except bloğuyla)
try:
    with open(file_path, 'w') as json_file:
        json.dump(data_to_save, json_file)
    print(f"EUR/USD paritesi JSON dosyasına ({file_path}) olarak kaydedildi.")
except Exception as e:
    print(f"Dosya oluşturulurken bir hata oluştu: {e}")
