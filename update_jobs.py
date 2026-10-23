import json
import re
from datetime import datetime, timezone
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://international.emploi.nat.tn"
OFFERS_URL = BASE_URL + "/offres"

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; ForasAmal/1.0)"
}

jobs = []
seen = set()

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()

retries = Retry(
    total=4,
    connect=4,
    backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)

session.mount("https://", HTTPAdapter(max_retries=retries))

response = session.get(
    OFFERS_URL,
    headers=headers,
    timeout=45
)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

for link in soup.find_all("a", href=True):
    href = link["href"]

    if not re.search(r"/node/\d+", href):
        continue

    url = urljoin(BASE_URL, href)

    if url in seen:
        continue

    title = link.get_text(" ", strip=True)

    if not title:
        continue

    seen.add(url)

    container = link
    for _ in range(5):
        if container.parent:
            container = container.parent

    text = container.get_text(" ", strip=True)

    date_match = re.search(
        r"Publié\s*:\s*"
        r"(.{0,50}?\d{1,2}/\d{1,2}/\d{4}"
        r"(?:\s*-\s*\d{1,2}:\d{2})?)",
        text,
        re.IGNORECASE
    )

    country_match = re.search(
        r"\b(FRANCE|ITALIE|ALLEMAGNE|"
        r"CANADA|ARABIE SAOUDITE|ESPAGNE)\b",
        text,
        re.IGNORECASE
    )

    jobs.append({
        "title": title,
        "country": (
            country_match.group(1)
            if country_match else "غير محدد"
        ),
        "company": "ANETI International",
        "date": (
            date_match.group(1).strip()
            if date_match else ""
        ),
        "url": url,
        "source": "ANETI International"
    })

data = {
    "updated_at": datetime.now(timezone.utc).isoformat(),
    "jobs": jobs
}

with open("jobs.json", "w", encoding="utf-8") as file:
    json.dump(
        data,
        file,
        ensure_ascii=False,
        indent=2
    )

print(f"تم العثور على {len(jobs)} رابط عرض في صفحة ANETI.")
