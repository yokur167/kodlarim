"""Add daily direction fields for Widgy without altering existing price keys.

Comparison: the last successfully recorded sample of the previous run day,
which is normally the previous weekday (not an exchange-certified close).
The state and prices are committed by GitHub Actions together.
"""

import json
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from zoneinfo import ZoneInfo


PRICE_FILES = (
    ("usd_fiyati.json", "USD", "USD_CHANGE"),
    ("eur_fiyati.json", "EUR", "EUR_CHANGE"),
    ("eur_usd_paritesii.json", "EUR_USD", "EUR_USD_CHANGE"),
    ("gold_price.json", "Gold", "GOLD_CHANGE"),
    ("bilezik_fiyati.json", "Bracelet", "BRACELET_CHANGE"),
    ("ceyrek_altin_price.json", "Quarter Gold", "QUARTER_GOLD_CHANGE"),
    ("ons_altin_fiyati.json", "Ons Gold", "ONS_GOLD_CHANGE"),
    ("cumhuriyet_altin_price.json", "Republic Gold", "REPUBLIC_GOLD_CHANGE"),
)

STATE_FILE = Path("widgy_daily_reference.json")


def parse_price(value):
    """Parse localized Bigpara ('6.360,02') and API ('1.11') values."""
    if isinstance(value, bool):
        raise ValueError(f"Invalid price: {value!r}")
    raw = str(value).strip()
    if not raw:
        raise ValueError("Empty price")
    if "," in raw:
        raw = raw.replace(".", "").replace(",", ".")
    try:
        price = Decimal(raw)
    except InvalidOperation as exc:
        raise ValueError(f"Invalid price: {value!r}") from exc
    if not price.is_finite() or price <= 0:
        raise ValueError(f"Invalid positive price: {value!r}")
    return price


def get_reference(state, today, current):
    """Keep a fixed reference through the day; roll it at day change."""
    if not state:
        return current.copy(), None
    prior_day = state["session_date"]
    if today < prior_day:
        raise ValueError(f"State is dated in the future: {prior_day}")
    if today > prior_day:
        return {k: parse_price(v) for k, v in state["last_prices"].items()}, prior_day
    return (
        {k: parse_price(v) for k, v in state["reference_prices"].items()},
        state.get("reference_date"),
    )


def run(today=None, root=Path(".")):
    today = today or datetime.now(ZoneInfo("Europe/Istanbul")).date().isoformat()
    root = Path(root)
    files = {}
    current = {}
    for filename, field, change_key in PRICE_FILES:
        path = root / filename
        data = json.loads(path.read_text(encoding="utf-8"))
        if field not in data:
            raise KeyError(f"Missing key {field!r} in {filename}")
        current[field] = parse_price(data[field])
        files[path] = (data, field, change_key)

    state_path = root / STATE_FILE
    state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else None
    reference, reference_date = get_reference(state, today, current)
    for path, (data, field, change_key) in files.items():
        baseline = reference.get(field, current[field])
        data[change_key] = (current[field] > baseline) - (current[field] < baseline)
        path.write_text(json.dumps(data, ensure_ascii=False) + "\n", encoding="utf-8")

    new_state = {
        "session_date": today,
        "last_prices": {k: str(v) for k, v in current.items()},
        "reference_prices": {k: str(v) for k, v in reference.items()},
        "reference_date": reference_date,
    }
    state_path.write_text(json.dumps(new_state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Widgy direction data refreshed. Reference date: {reference_date or 'initial baseline'}")


if __name__ == "__main__":
    run()
