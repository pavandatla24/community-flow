import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

BASE_URL = "https://www.eventbrite.com/d/il--chicago/wellness/"

def scrape_eventbrite():
    print("Scraping Eventbrite...")

    response = requests.get(BASE_URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")

    events = soup.select("div.search-event-card-wrapper")

    results = []

    for e in events:
        try:
            title = e.select_one("div.eds-event-card-content__primary-content > a").get_text(strip=True)
        except:
            title = None

        try:
            link = "https://eventbrite.com" + e.select_one("a")["href"]
        except:
            link = None

        try:
            date = e.select_one("div.eds-text-bs--fixed").get_text(strip=True)
        except:
            date = None

        try:
            description = e.select_one("div.eds-event-card-content__sub-title").get_text(strip=True)
        except:
            description = None

        results.append({
            "title": title,
            "text": description,
            "date": date,
            "link": link,
            "source": "Eventbrite",
            "neighborhood": "Chicago"  # we refine later
        })

    # Save file
    os.makedirs("data/raw", exist_ok=True)
    filename = f"data/raw/eventbrite_{datetime.now().strftime('%Y-%m-%d')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"Saved {len(results)} events → {filename}")
    return results


if __name__ == "__main__":
    scrape_eventbrite()
