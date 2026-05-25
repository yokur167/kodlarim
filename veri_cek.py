import csv
import json
import re
from datetime import datetime
from urllib.request import Request, urlopen

URL = "https://www.albaraka.com.tr/tr/doviz-kurlari"

TARGETS = {
    "USD": r"Amerikan Doları\(USD\)",
    "EUR": r"Avrupa Para Birimi\(EUR\)",
    "ALTIN": r"Altın\(XAU\)",
}

req = Request(URL, headers={"User-Agent": "Mozilla/5.0"})

with urlopen(req, timeout=30) as response:
    html = response.read().decode("utf-8", errors="ignore")

update_match = re.search(r"Son Güncelleme:\s*([0-9.:-]+)", html)
updated_at = update_match.group(1) if update_match else datetime.now().strftime("%d.%m.%Y-%H:%M")

rows = []

for name, pattern in TARGETS.items():
    match = re.search(pattern + r"\s*([0-9,]+)\s*([0-9,]+)", html)

    if not match:
        raise Exception(f"{name} kuru bulunamadı.")

    rows.append({
        "Döviz cinsi": name,
        "Alış": match.group(1),
        "Satış": match.group(2),
        "Güncellenen Tarih ve Saat": updated_at
    })

with open("albaraka_kurlar.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["Döviz cinsi", "Alış", "Satış", "Güncellenen Tarih ve Saat"],
        delimiter=";"
    )
    writer.writeheader()
    writer.writerows(rows)

with open("albaraka_kurlar.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)

print("Veriler güncellendi.")