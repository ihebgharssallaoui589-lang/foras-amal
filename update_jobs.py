
import json
from datetime import datetime, timezone

sources = [
    {
        "title": "عروض الشغل الدولية",
        "country": "دولي",
        "company": "ANETI International",
        "url": "https://www.aneti-international.tn/en"
    },
    {
        "title": "عروض الشغل في أوروبا",
        "country": "أوروبا",
        "company": "EURES",
        "url": "https://eures.europa.eu/index_en"
    },
    {
        "title": "عروض الشغل في فرنسا",
        "country": "فرنسا",
        "company": "France Travail",
        "url": "https://www.francetravail.fr/"
    },
    {
        "title": "عروض الشغل في ألمانيا",
        "country": "ألمانيا",
        "company": "Bundesagentur für Arbeit",
        "url": "https://www.arbeitsagentur.de/"
    }
]

data = {
    "updated_at": datetime.now(timezone.utc).isoformat(),
    "jobs": sources
}

with open("jobs.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

print(f"تم تحديث {len(sources)} روابط مصادر الشغل.")
