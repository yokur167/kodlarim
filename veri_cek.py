import csv
import json
import re
from datetime import datetime
from urllib.request import Request, urlopen

URL = "https://kur.doviz.com/albaraka-turk"

req = Request(URL, headers={"User-Agent": "Mozilla/5.0"})

with urlopen(req, timeout=30) as response:
    html = response.read().decode("utf-8", errors="ignore")

html = re.sub(r"\s+", " ", html)

def bul(kod):
    pattern = rf"Albaraka Türk .*?{kod}.*?([0-9]+,[0-9]+).*?([0-9]+,[0-9]+).*?([0-9]{{2}}:[0-9]{{2}})"
    match = re.search(pattern, html, re.IGNORECASE)

    if not match:
        raise Exception(f"{kod} kuru bulunamadı.")

    return match.group(1), match.group(2), match.group(3)

usd_alis, usd_satis, usd_saat = bul("USD")
eur_alis, eur_satis, eur_saat = bul("EUR")

# Doviz.com Albaraka listesinde XAU her zaman bulunmayabilir.
# Bulunamazsa boş bırakır; workflow patlamaz.
try:
    xau_alis, xau_satis, xau_saat = bul("XAU")
except Exception:
    xau_alis, xau_satis, xau_saat = "", "", ""

bugun = datetime.now().strftime("%d.%m.%Y")

rows = [
    ["USD", usd_alis, usd_satis, f"{bugun} {usd_saat}"],
    ["EUR", eur_alis, eur_satis, f"{bugun} {eur_saat}"],
    ["ALTIN", xau_alis, xau_satis, f"{bugun} {xau_saat}" if xau_saat else ""],
]

with open("albaraka_kurlar.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["Döviz cinsi", "Alış", "Satış", "Güncellenen Tarih ve Saat"])
    writer.writerows(rows)

with open("albaraka_kurlar.json", "w", encoding="utf-8") as f:
    json.dump(
        [
            {
                "Döviz cinsi": r[0],
                "Alış": r[1],
                "Satış": r[2],
                "Güncellenen Tarih ve Saat": r[3],
            }
            for r in rows
        ],
        f,
        ensure_ascii=False,
        indent=2,
    )

print("Veriler başarıyla güncellendi.")