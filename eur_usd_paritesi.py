import requests
import json

# Frankfurter API'den EUR/USD paritesini çekiyoruz
url = 'https://api.frankfurter.app/latest?base=EUR&symbols=USD'
response = requests.get(url)
data = response.json()

# EUR/USD paritesini alıyoruz
eur_usd = data['rates']['USD']

# Ondalık basamakları 2 hane yapıyoruz ve virgül ile gösteriyoruz
formatted_eur_usd = f"{eur_usd:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Sonucu ekrana yazdırıyoruz
print(f"EUR/USD Paritesi: {formatted_eur_usd}")

# Veriyi JSON formatında oluşturuyoruz
data_formatted = {
    "EUR/USD": formatted_eur_usd
}

# Veriyi JSON dosyasına kaydediyoruz
with open('eur_usd_paritesii.json', 'w') as json_file:
    json.dump(data_formatted, json_file)

print("EUR/USD paritesi JSON dosyasına kaydedildi.")
