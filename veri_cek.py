import csv
import json
import re
from datetime import datetime
from urllib.request import Request, urlopen

URL = "https://www.albaraka.com.tr/tr/doviz-kurlari"

req = Request(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

with urlopen(req, timeout=30) as response:
    html = response.read().decode("utf-8", errors="ignore")

def kur_bul(kod):
    pattern = rf'"Code":"{kod}".*?"ForexBuying":"([^"]+)".*?"ForexSelling":"([^"]+)"'

    match = re.search(pattern, html)

    if not match:
        raise Exception(f"{kod} kuru bulunamadı.")

    return match.group(1), match.group(2)

usd_alis, usd_satis = kur_bul("USD")
eur_alis, eur_satis = kur_bul("EUR")
xau_alis, xau_satis = kur_bul("XAU")

guncelleme = datetime.now().strftime("%d.%m.%Y %H:%M")

rows = [
    {
        "Döviz cinsi": "USD",
        "Alış": usd_alis,
        "Satış": usd_satis,
        "Güncellenen Tarih ve Saat": guncelleme
    },
    {
        "Döviz cinsi": "EUR",
        "Alış": eur_alis,
        "Satış": eur_satis,
        "Güncellenen Tarih ve Saat": guncelleme
    },
    {
        "Döviz cinsi": "ALTIN",
        "Alış": xau_alis,
        "Satış": xau_satis,
        "Güncellenen Tarih ve Saat": guncelleme
    }
]

with open("albaraka_kurlar.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "Döviz cinsi",
            "Alış",
            "Satış",
            "Güncellenen Tarih ve Saat"
        ],
        delimiter=";"
    )

    writer.writeheader()
    writer.writerows(rows)

with open("albaraka_kurlar.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)

print("Veriler başarıyla güncellendi.")