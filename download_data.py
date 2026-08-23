import csv
from pathlib import Path

import requests

API_URL = "https://api.nobelprize.org/2.1/laureates"


def english(value: dict | None) -> str:
    return "" if not value else str(value.get("en", ""))


def download(output_path: Path, limit: int = 200) -> int:
    response = requests.get(API_URL, params={"limit": limit}, timeout=30)
    response.raise_for_status()
    laureates = response.json().get("laureates", [])
    rows = []
    for laureate in laureates:
        name = english(laureate.get("fullName")) or english(laureate.get("orgName"))
        gender = laureate.get("gender", "Organization")
        country = english((laureate.get("birth", {}).get("place") or {}).get("country"))
        # one person can appear for more than one award
        for prize in laureate.get("nobelPrizes", []):
            rows.append(
                {
                    "year": prize.get("awardYear", ""),
                    "category": english(prize.get("category")),
                    "laureate": name,
                    "gender": gender,
                    "country": country,
                }
            )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["year", "category", "laureate", "gender", "country"])
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    count = download(Path("data/nobel_download.csv"))
    print(f"Saved {count} award rows")
